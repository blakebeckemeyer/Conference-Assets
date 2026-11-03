"""Dependency-free checks for the two-talk deck and its local evidence fixtures."""
import csv
import json
import re
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


class HtmlPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.slides = []
        self.notes = 0
        self.heading_refs = []
        self._slide = None
        self._note = None
        self._capture_heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "section" and "slide" in attrs.get("class", "").split():
            self._slide = {
                "id": attrs.get("id"),
                "talk": attrs.get("data-talk"),
                "segment": attrs.get("data-segment"),
                "label": attrs.get("aria-labelledby"),
                "headingId": None,
                "title": "",
                "minutes": None,
                "noteCount": 0,
                "images": [],
            }
            self.heading_refs.append(attrs.get("aria-labelledby"))
        if tag == "template" and "speaker-notes" in attrs.get("class", "").split():
            self.notes += 1
            if self._slide is not None:
                self._slide["noteCount"] += 1
            self._note = []
        if tag == "aside" and "notes" in attrs.get("class", "").split():
            raise AssertionError("Private notes must not be inline audience content")
        if self._slide and self._note is None:
            assert "status" not in attrs.get("class", "").split(), "Presenter status asides must not be on slides"
            if tag == "img":
                assert attrs.get("alt"), "Teaching visuals need meaningful alternate text"
                assert "display:none" not in attrs.get("style", "").replace(" ", ""), "Do not hide visuals to pass coverage"
                self._slide["images"].append(attrs["src"])
        if self._slide and tag in ("h1", "h2") and not self._slide["title"]:
            self._capture_heading = True
            self._slide["headingId"] = attrs.get("id")
        for field in ("href", "src"):
            if field in attrs:
                self.links.append(attrs[field])

    def handle_endtag(self, tag):
        if tag in ("h1", "h2") and self._capture_heading:
            self._capture_heading = False
        if tag == "template" and self._note is not None:
            note = " ".join(self._note)
            match = re.search(r"\b(\d+)\s+minutes?\.", note)
            self._slide["minutes"] = int(match.group(1)) if match else None
            self._note = None
        if tag == "section" and self._slide:
            self.slides.append(self._slide)
            self._slide = None

    def handle_data(self, data):
        if self._capture_heading and self._slide is not None:
            self._slide["title"] += data
        if self._note is not None:
            self._note.append(data)


def parse_page(filename):
    page = HtmlPage()
    page.feed((ROOT / filename).read_text(encoding="utf-8"))
    assert len(page.ids) == len(set(page.ids)), f"Duplicate IDs in {filename}"
    return page


def check_link(source, link, all_pages):
    parts = urlsplit(link)
    if parts.scheme == "https":
        assert parts.hostname == "learn.microsoft.com", f"Unexpected external host in {source}: {link}"
        return
    assert not parts.scheme and not parts.netloc, f"Unexpected external dependency in {source}: {link}"
    if parts.path:
        target = (ROOT / unquote(parts.path)).resolve()
        assert target.is_relative_to(ROOT.resolve()), f"Out-of-scope link in {source}: {link}"
        assert target.is_file(), f"Broken local link in {source}: {link}"
        if target in all_pages and parts.fragment:
            assert parts.fragment in all_pages[target].ids, f"Missing page anchor in {source}: {link}"
    elif parts.fragment:
        assert parts.fragment in all_pages[(ROOT / source).resolve()].ids, f"Broken anchor in {source}: {link}"


deck = parse_page("index.html")
assert len(deck.slides) == deck.notes == 32, "Expected 32 slides with one inert private note template each"
assert all(item["label"] == item["headingId"] and item["noteCount"] == 1 for item in deck.slides), (
    "Each slide needs an accessible title and one private note template"
)
assert all(item["title"] and item["minutes"] for item in deck.slides), "A slide title or note duration is missing"
assert sum(bool(item["images"]) for item in deck.slides) >= 28, "Keep the deck visual-led"
svg_assets = set()
for slide in deck.slides:
    for image in slide["images"]:
        if image.endswith(".svg"):
            svg_assets.add(ROOT / image)
for asset in svg_assets:
    svg = ElementTree.parse(asset).getroot()
    assert svg.attrib.get("viewBox"), f"Scalable viewBox missing from {asset.name}"
    assert svg.find("{http://www.w3.org/2000/svg}title") is not None, f"Visual title missing: {asset.name}"
    assert not list(svg.iter("{http://www.w3.org/2000/svg}script")), "Visual assets must be inert"

schedule = json.loads((ROOT / "data" / "run-of-show.json").read_text(encoding="utf-8"))
presentations = schedule["presentations"]
assert schedule["totalPresentationMinutes"] == 90
assert [(item["id"], item["durationMinutes"]) for item in presentations] == [
    ("talk-a", 60), ("talk-b", 30)
]
scheduled_slides = []
for presentation in presentations:
    first, last = presentation["firstSlide"], presentation["lastSlide"]
    talk_slides = list(range(first, last + 1))
    actual = [index for index, slide in enumerate(deck.slides, 1)
              if slide["talk"] == presentation["id"]]
    assert actual == talk_slides, f"Unexpected slide range for {presentation['id']}"
    assert deck.slides[first - 1]["id"] == presentation["startAnchor"]
    assert sum(deck.slides[index - 1]["minutes"] for index in talk_slides) == presentation["durationMinutes"]
    segment_coverage = []
    elapsed = 0
    for segment in presentation["segments"]:
        slides = segment["slides"]
        assert slides and slides == list(range(slides[0], slides[-1] + 1)), "Segment slides must be contiguous"
        assert all(deck.slides[index - 1]["talk"] == presentation["id"] and
                   deck.slides[index - 1]["segment"] == segment["id"] for index in slides), (
            f"Slide mapping differs for {segment['id']}"
        )
        assert sum(deck.slides[index - 1]["minutes"] for index in slides) == segment["minutes"], (
            f"Presenter note pacing differs for {segment['id']}"
        )
        segment_coverage.extend(slides)
        end = elapsed + segment["minutes"]
        label = f"{elapsed // 60:02}:{elapsed % 60:02}-{end // 60:02}:{end % 60:02}"
        for filename in ("index.html", "attendee-guide.html", "deck.js"):
            assert label in (ROOT / filename).read_text(encoding="utf-8"), (
                f"Talk-relative timing {label} missing from {filename}"
            )
        elapsed = end
    assert elapsed == presentation["durationMinutes"]
    assert segment_coverage == talk_slides, f"Unscheduled/duplicate slides in {presentation['id']}"
    scheduled_slides.extend(talk_slides)
assert scheduled_slides == list(range(1, 33)), "Talks must cover each slide exactly once"

html_files = list(ROOT.rglob("*.html"))
assert len(html_files) == 3 and {path.name for path in html_files} == {
    "index.html", "attendee-guide.html", "presenter.html"
}, "Only the audience deck, consolidated attendee guide and private presenter console are allowed"
guide = parse_page("attendee-guide.html")
for section in ("start", "local", "m365", "cowork", "lifecycle", "studio", "foundry", "checks", "references"):
    assert section in guide.ids, f"Missing attendee guide section #{section}"
presenter = parse_page("presenter.html")
all_pages = {
    (ROOT / "index.html").resolve(): deck,
    (ROOT / "attendee-guide.html").resolve(): guide,
    (ROOT / "presenter.html").resolve(): presenter,
}
for filename, page in (("index.html", deck), ("attendee-guide.html", guide), ("presenter.html", presenter)):
    for link in page.links:
        check_link(filename, link, all_pages)

deck_js = (ROOT / "deck.js").read_text(encoding="utf-8")
presenter_js = (ROOT / "presenter.js").read_text(encoding="utf-8")
presenter_html = (ROOT / "presenter.html").read_text(encoding="utf-8")
assert "jump-talk-a" in deck_js and "jump-talk-b" in deck_js
assert "talk-a" in presenter_js and "talk-b" in presenter_js and "talkDuration" in presenter_js
assert "Start Talk A" in presenter_html and "Start Talk B" in presenter_html
assert "resets when you switch talks" in presenter_html
assert "aria-pressed" not in (ROOT / "index.html").read_text(encoding="utf-8")

visuals = json.loads((ROOT / "assets" / "conference-visual-sources.json").read_text(encoding="utf-8"))
assert visuals["sources"]
for source in visuals["sources"]:
    assert source["title"] and source["pages"] and source["adaptation"]
    assert set(source["usedOnSlides"]).issubset({slide["id"] for slide in deck.slides})
    assert source["authors"] and source["filename"] and re.fullmatch(r"[A-F0-9]{64}", source["sha256"])
    for asset in source["assets"]:
        assert (ROOT / "assets" / asset).is_file(), f"Missing attributed visual {asset}"
brand = json.loads((ROOT / "assets" / "brand-sources.json").read_text(encoding="utf-8"))
assert "19 Talk A slides and 13 independent Talk B slides" in brand["surfaceRecord"]["contentBoundary"]

expected = json.loads((ROOT / "fixtures" / "expected-facts.json").read_text(encoding="utf-8"))
for product in expected["products"]:
    folder = ROOT / "examples" / product["productId"]
    with (folder / "retailer-listing.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    listing = product["listing"]
    assert len(rows) == 1 and None not in rows[0], f"Invalid listing CSV for {product['productId']}"
    row = rows[0]
    assert row["sku"] == listing["sku"] and row["title"] == listing["title"]
    assert row["manufacturer_msrp"] == f'{listing["msrp"]:.2f}'
    assert [row[f"bullet_{n}"] for n in range(1, 6)] == listing["bullets"]
    assert row["status"] == "needs_review" and row["synthetic"] == "true"
    assert row["gtin"] == row["image_assets"] == row["warranty_terms"] == ""

foundry = json.loads((ROOT / "fixtures" / "foundry-catalog-processing.json").read_text(encoding="utf-8"))
assert foundry["status"] == "design-only-not-a-model-or-foundry-run"
assert foundry["scenario"]["independentOfTalkA"] is True
assert foundry["scenario"]["publishActionEnabled"] is False
assert foundry["scenario"]["sourceDocumentsBuilt"] is False and foundry["scenario"]["pipelineBuilt"] is False
cases = foundry["cases"]
assert [case["caseId"] for case in cases] == [f"FC-{n:02}" for n in range(1, 6)]
for case in cases:
    inputs, result = case["plannedInputs"], case["expected"]
    assert set(inputs) == {"specPdf", "supplierSpreadsheet", "packagingImage"}
    assert all(inputs.values())
    # This checks the design oracle, not extraction accuracy or a deployed validator.
    for source in ("specPdf", "supplierSpreadsheet"):
        measurement = re.search(r"(\d+(?:\.\d+)?) (mm|cm)", inputs[source])
        assert measurement, f"Missing designed measurement for {case['caseId']}"
        normalized = Decimal(measurement[1]) / (10 if measurement[2] == "mm" else 1)
        assert Decimal(result["width_cm"]) == normalized
    expected_status = "needs_review" if result["issues"] else "validated_draft"
    assert result["status"] == expected_status
    assert {"sku", "color", "width_cm", "warranty_months", "issues", "status"} <= set(result)
assert cases[1]["expected"]["sku"] is None
assert cases[1]["expected"]["candidates"]["sku"] == ["NL-200", "NL-201"]
assert cases[2]["expected"]["color"] is None
assert cases[2]["expected"]["candidates"]["color"] == ["black", "red"]
assert cases[3]["expected"]["warranty_months"] is None
assert [case["caseId"] for case in cases if case["expected"]["status"] == "validated_draft"] == ["FC-01", "FC-05"]
assert foundry["comparisonPlan"]["results"] is None and foundry["comparisonPlan"]["winner"] is None

guide_text = (ROOT / "attendee-guide.html").read_text(encoding="utf-8")
for required in ("studio-models", "studio-scorecard", "studio-alm", "studio-publish",
                 "428fc189-ef8f-e8ff-bfc1-ac1aadb32905", "authoring-select-agent-model",
                 "publication-channels-overview", "fixtures/foundry-catalog-processing.json",
                 "foundry-prepare", "foundry-input", "foundry-run", "foundry-result",
                 "foundry-trace", "foundry-tests"):
    assert required in guide_text, f"Missing current two-talk setup detail: {required}"
for removed in ("studio-dataverse", "register-retail-launch-draft", "ms app deploy",
                "ms app clone", "Copy to Copilot Studio", "PreValidation",
                "foundry-quote-comparison", "DockLink-R2", "FQ-01"):
    assert removed not in guide_text, f"Unused demo reintroduced into attendee guide: {removed}"
for case in cases:
    assert case["caseId"] in guide_text, f"Missing Foundry walkthrough case {case['caseId']}"
print("Deck check passed: 32 slides, two independent 60/30-minute schedules, private notes, three HTML endpoints, valid local links, source attribution and synthetic fixtures.")
