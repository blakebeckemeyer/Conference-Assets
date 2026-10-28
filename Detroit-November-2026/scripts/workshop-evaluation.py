"""Offline test oracle and context builder. Never authenticates or calls a service."""
import argparse
import csv
import json
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_VERSION = "manufacturer-products-v1 + retailer-requirements-v1"
RULE_VERSION = "retail-launch-rules-v1"


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def retrieve(case, mode):
    docs = load("fixtures/retailer-policy-corpus.json")["documents"]
    if mode == "scoped":
        docs = [d for d in docs if d["retailerId"] == case["retailerId"]
                and d["revision"] == case["revision"] and d["status"] == "approved"]
    # A transparent lexical baseline, not vector/hybrid/semantic search.
    scored = [(sum(token in re.findall(r"\w+", (d["section"] + " " + d["text"]).lower())
                   for token in case["tokens"]), i, d) for i, d in enumerate(docs)]
    return [d for score, _, d in sorted(scored, key=lambda row: (-row[0], row[1]))
            if score > 0][:3]


def package_for(sku):
    folders = {"LM-D1820-K2": "drill-kit", "LM-I1820-K2": "impact-driver-kit"}
    return load(f"examples/{folders[sku]}/package.json") if sku in folders else None


def validate_candidate(sku, retailer_id, package):
    baseline = package_for(sku)
    if retailer_id != "great-lakes-home":
        return "invalid_input", ["UNKNOWN_RETAILER"]
    if baseline is None:
        return "invalid_input", ["UNKNOWN_SKU"]
    policy = load("data/retailer-requirements.json")
    if not isinstance(package, dict) or set(package) != set(baseline):
        return "invalid_package", ["INVALID_PACKAGE_SHAPE"]
    listing = package.get("listing")
    if (not isinstance(listing, dict) or set(listing) != set(baseline["listing"])
            or not isinstance(listing.get("title"), str)
            or not isinstance(listing.get("bullets"), list)
            or any(not isinstance(b, str) for b in listing["bullets"])):
        return "invalid_package", ["INVALID_PACKAGE_SHAPE"]
    issues = []
    if len(listing["title"]) > policy["titleMaxLength"]:
        issues.append("TITLE_TOO_LONG")
    if len(listing["bullets"]) != policy["bulletCount"]:
        issues.append("BULLET_COUNT")
    if any(len(b) > policy["bulletMaxLength"] for b in listing["bullets"]):
        issues.append("BULLET_TOO_LONG")
    if listing["bullets"] != baseline["listing"]["bullets"]:
        issues.append("UNREVIEWED_COPY")
    if listing["category"] != baseline["listing"]["category"]:
        issues.append("CATEGORY_MISMATCH")
    if not issues and package != baseline:
        issues.append("UNREVIEWED_PACKAGE")
    if issues:
        return "invalid_package", issues
    gaps = [rule["code"] for rule in policy["requiredForSubmission"] if not listing[rule["field"]]]
    return "needs_review", gaps


def proposed_row(sku):
    package = package_for(sku)
    if package is None:
        raise ValueError(f"Unknown SKU: {sku}")
    decision, issues = validate_candidate(sku, "great-lakes-home", package)
    if decision != "needs_review":
        raise ValueError(f"Reviewed reference is invalid: {issues}")
    product_id = package["productId"]
    request_key = str(uuid.uuid5(uuid.NAMESPACE_URL, f"detroit-retail-launch:{sku}:great-lakes-home:{SOURCE_VERSION}"))
    return {
        "name": f"{sku} - great-lakes-home",
        "requestkey": request_key,
        "sku": sku,
        "retailerid": "great-lakes-home",
        "sourceversion": SOURCE_VERSION,
        "packagereference": f"Detroit-November-2026/examples/{product_id}/package.json @ manufacturer-products-v1",
        "packagesnapshot": json.dumps(package, ensure_ascii=True, separators=(",", ":")),
        "retailercategory": package["listing"]["category"],
        "validationversion": RULE_VERSION,
        "reviewstate": decision,
        "issuecodes": ";".join(issues),
    }


def business_decision(case):
    if case["mutation"] == "cancel":
        return "cancelled", []
    if case["mutation"] == "approval-request":
        return "out_of_scope", []
    package = package_for(case["sku"])
    if package is not None and case["mutation"] == "unsupported-claim":
        package["listing"]["bullets"][0] += " UL listed."
    if package is not None and case["mutation"] == "long-title":
        package["listing"]["title"] = "x" * 81
    decision, issues = validate_candidate(case["sku"], case["retailerId"], package)
    if decision != "needs_review":
        return decision, issues
    # These are expected action boundaries, never simulated connector results.
    if case["mutation"] == "storage-denied":
        return "save_failed", ["SAVE_FAILED"]
    if case["mutation"] == "reload-denied":
        return "verification_incomplete", ["VERIFY_FAILED"]
    if case["mutation"] == "retry":
        return "already_registered", issues
    return decision, issues


def check():
    tests = load("fixtures/studio-tests.json")["cases"]
    assert len({c["id"] for c in tests}) == len(tests) == 11
    for case in tests:
        assert business_decision(case) == (case["expectedDecision"], case["expectedIssues"]), case["id"]
        assert case["expectedWrites"] == (1 if case["expectedDecision"] in ("needs_review", "verification_incomplete") else 0)
    keys = set()
    for sku in ("LM-D1820-K2", "LM-I1820-K2"):
        row = proposed_row(sku)
        assert row == proposed_row(sku), "Same product/revision must keep its request key"
        assert str(uuid.UUID(row["requestkey"])) == row["requestkey"]
        keys.add(row["requestkey"])
        assert len(row["packagesnapshot"]) <= 10000
        assert json.loads(row["packagesnapshot"]) == package_for(sku)
        assert row["reviewstate"] == "needs_review"
        assert row["issuecodes"] == "MISSING_GTIN;MISSING_IMAGES;MISSING_WARRANTY"
    assert len(keys) == 2, "Different products must not share a request key"
    for field, value, code in (
        ("category", "wrong", "CATEGORY_MISMATCH"),
        ("bullets", [], "BULLET_COUNT"),
        ("bullets", ["x" * 161] * 5, "BULLET_TOO_LONG"),
        ("title", None, "INVALID_PACKAGE_SHAPE"),
        ("gtin", "invented", "UNREVIEWED_PACKAGE"),
    ):
        candidate = package_for("LM-D1820-K2")
        candidate["listing"][field] = value
        decision, issues = validate_candidate("LM-D1820-K2", "great-lakes-home", candidate)
        assert decision == "invalid_package" and code in issues, field
    with (ROOT / "fixtures/studio-evaluation.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ["Question", "Expected response"]
        rows = list(reader)
    assert len(rows) == 5
    assert all(len(r["Question"]) <= 1000 and r["Expected response"] and None not in r for r in rows)
    policy = load("data/retailer-requirements.json")
    docs = {d["id"]: d for d in load("fixtures/retailer-policy-corpus.json")["documents"]}
    assert len(docs) == 8
    assert str(policy["titleMaxLength"]) in docs["gl-v1-title"]["text"]
    assert policy["bulletCount"] == 5 and "exactly five factual bullets." in docs["gl-v1-bullets"]["text"]
    assert str(policy["bulletMaxLength"]) in docs["gl-v1-bullets"]["text"]
    assert all(category in docs["gl-v1-categories"]["text"] for category in policy["categoryMap"].values())
    cases = load("fixtures/policy-tests.json")["cases"]
    schema = load("contracts/policy-answer.schema.json")
    fields = {"caseId", "status", "value", "documentId", "quote"}
    assert schema["type"] == "object" and schema["additionalProperties"] is False
    assert set(schema["properties"]) == set(schema["required"]) == fields
    assert schema["properties"]["status"]["enum"] == ["answered", "insufficient_evidence"]
    assert schema["properties"]["caseId"]["type"] == "string"
    assert all(schema["properties"][key]["type"] == ["string", "null"]
               for key in ("value", "documentId", "quote"))
    assert len({c["id"] for c in cases}) == len(cases) == 8
    for case in cases:
        expected = case["expectedDocument"]
        ids = [d["id"] for d in retrieve(case, "scoped")]
        assert (expected in ids) if expected else not ids, case["id"]
    assert retrieve(cases[0], "broad")[0]["id"] == "gl-v0-title"
    assert retrieve(cases[0], "scoped")[0]["id"] == "gl-v1-title"
    # Reject corrupted results, unsupported extra properties and version leakage.
    valid = [{"caseId": c["id"], "status": "answered" if c["expectedDocument"] else "insufficient_evidence",
              "value": c["expectedValue"], "documentId": c["expectedDocument"],
              "quote": docs[c["expectedDocument"]]["text"] if c["expectedDocument"] else None} for c in cases]
    assert all(r["passed"] for r in score(valid, "scoped"))
    for field, replacement in [("value", "120"), ("documentId", "gl-v0-title"), ("quote", "invented quote"),
                               ("status", "approved"), ("extra", True)]:
        corrupt = json.loads(json.dumps(valid))
        corrupt[0][field] = replacement
        assert not score(corrupt, "scoped")[0]["passed"], field
    print("Offline only: 11 Studio business/action expectations, 2 stable proposed payloads, 5 baseline questions, 8 retrieval cases and scorer/validation negatives checked.")
    print("No Studio/Foundry evaluation, tool execution, Dataverse write or model result is represented by this check.")


def score(responses, mode):
    cases = load("fixtures/policy-tests.json")["cases"]
    if not isinstance(responses, list) or len(responses) != len(cases):
        raise ValueError("Expected exactly one response per policy case.")
    if any(not isinstance(r, dict) or not isinstance(r.get("caseId"), str) for r in responses):
        raise ValueError("Each response must be an object with a caseId string.")
    by_id = {r["caseId"]: r for r in responses}
    if len(by_id) != len(responses) or set(by_id) != {c["id"] for c in cases}:
        raise ValueError("Duplicate, missing or unknown caseId.")
    results = []
    fields = {"caseId", "status", "value", "documentId", "quote"}
    for case in cases:
        response = by_id[case["id"]]
        expected = case["expectedDocument"]
        docs = {d["id"]: d for d in retrieve(case, mode)}
        doc = docs.get(response.get("documentId")) if isinstance(response.get("documentId"), str) else None
        quote = response.get("quote")
        grounded = bool(doc and isinstance(quote, str) and quote.strip() and quote in doc["text"]
                        and doc["revision"] == case["revision"] and doc["status"] == "approved"
                        and doc["retailerId"] == case["retailerId"])
        if expected is None:
            passed = (set(response) == fields and response["status"] == "insufficient_evidence"
                      and response["value"] is None and response["documentId"] is None and quote is None)
        else:
            passed = (set(response) == fields and response["status"] == "answered"
                      and response["value"] == case["expectedValue"] and response["documentId"] == expected
                      and grounded)
        results.append({"caseId": case["id"], "passed": passed, "citedRetrievedApprovedEvidence": grounded})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    prepare = sub.add_parser("prepare", help="Print proposed field suffixes and reviewed payload; never writes a row.")
    prepare.add_argument("--sku", choices=["LM-D1820-K2", "LM-I1820-K2"], required=True)
    context = sub.add_parser("context")
    context.add_argument("--case", required=True)
    context.add_argument("--mode", choices=["broad", "scoped"], required=True)
    scoring = sub.add_parser("score")
    scoring.add_argument("--responses", type=Path, required=True)
    scoring.add_argument("--mode", choices=["broad", "scoped"], required=True)
    args = parser.parse_args()
    if args.command == "check":
        check()
    elif args.command == "prepare":
        print(json.dumps({"executionStatus": "local-proposal-not-saved",
                          "fieldNaming": "Proposed suffixes; bind actual publisher-prefixed columns from metadata.",
                          "row": proposed_row(args.sku)}, indent=2))
    elif args.command == "context":
        cases = load("fixtures/policy-tests.json")["cases"]
        case = next((c for c in cases if c["id"] == args.case), None)
        if case is None:
            parser.error("Unknown case ID.")
        print(json.dumps({"caseId": case["id"], "query": case["query"],
                          "retailerId": case["retailerId"], "revision": case["revision"],
                          "documents": retrieve(case, args.mode)}, indent=2))
    else:
        results = score(json.loads(args.responses.read_text(encoding="utf-8")), args.mode)
        print(json.dumps({"mode": args.mode, "results": results,
                          "passed": sum(r["passed"] for r in results), "total": len(results)}, indent=2))
        if not all(r["passed"] for r in results):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
