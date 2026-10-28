"""Dependency-free structural checks, not a substitute for browser inspection."""
import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Deck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.slides = []
        self.notes = 0
        self.headings = []
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "section" and "slide" in attrs.get("class", "").split():
            self.slides.append((attrs["id"], attrs["data-segment"]))
            self.references.append(attrs["aria-labelledby"])
        if tag == "template" and "speaker-notes" in attrs.get("class", "").split():
            self.notes += 1
        assert not (tag == "aside" and "notes" in attrs.get("class", "").split()), "Audience must not contain inline notes"
        if tag in ("h1", "h2"):
            self.headings.append(attrs.get("id"))
        for field in ("href", "src"):
            if field in attrs:
                self.links.append(attrs[field])


deck = Deck()
deck.feed((ROOT / "index.html").read_text(encoding="utf-8"))
assert len(deck.ids) == len(set(deck.ids)), "Duplicate element IDs"
assert len(deck.slides) == 48 and deck.notes == 48, "Missing slides or inert presenter notes"
assert deck.headings == deck.references, "Slide headings/accessible names differ"
assert [sid for sid, _ in deck.slides] == (
    [f"slide-{n}" for n in range(1, 18)]
    + [f"slide-lab-{n}" for n in range(1, 9)]
    + [f"slide-{n}" for n in range(18, 41)]
), "Existing slide anchors and inserted lab order must stay stable"


def check_link(link, ids):
    parts = urlsplit(link)
    if parts.scheme == "https":
        assert parts.netloc == "learn.microsoft.com", f"Unexpected reference host: {link}"
        return
    assert not parts.scheme and not parts.netloc, f"External dependency: {link}"
    if parts.path:
        target = (ROOT / unquote(parts.path)).resolve()
        assert target.is_relative_to(ROOT), f"Out-of-scope link: {link}"
        assert target.is_file(), f"Broken local link: {link}"
    elif parts.fragment:
        assert parts.fragment in ids, f"Broken anchor: {link}"


for link in deck.links:
    check_link(link, deck.ids)
documents = {"index.html": deck}
html_files = list(ROOT.rglob("*.html"))
assert len(html_files) == 3 and {path.name for path in html_files} == {"index.html", "attendee-guide.html", "presenter.html"}, "Only slides, one attendee guide and the private presenter console are allowed"
for name in ("attendee-guide.html",):
    page = Deck()
    page.feed((ROOT / name).read_text(encoding="utf-8"))
    assert len(page.ids) == len(set(page.ids)), f"Duplicate anchors in {name}"
    documents[name] = page
for name, page in documents.items():
    for link in page.links:
        check_link(link, page.ids)
        parts = urlsplit(link)
        if parts.path in documents and parts.fragment:
            assert parts.fragment in documents[parts.path].ids, f"Missing linked section: {name}: {link}"
guide = documents["attendee-guide.html"]
assert {"lifecycle", "studio", "foundry"}.issubset(set(guide.ids))
guide_text = (ROOT / "attendee-guide.html").read_text(encoding="utf-8")
studio = re.search(r'<section id="studio">(.*?)</section>', guide_text, re.S)[1]
for required in ("Retail Launch Request", "GitHub Copilot harness",
                 "register-retail-launch-draft", "General quality", "5 MB",
                 "PreOperation", "CreateRecord", "GetItem", "ListRecords",
                 "fixtures/studio-evaluation.csv", "fixtures/studio-tests.json",
                 "S01-S11", "verification incomplete"):
    assert required in studio, f"Missing Studio exercise detail: {required}"
foundry = re.search(r'<section id="foundry">(.*?)</section>', guide_text, re.S)[1]
model_recipe = next(block for block in re.findall(r"<pre><code>(.*?)</code></pre>", foundry, re.S)
                    if "from openai import OpenAI" in block)
from html import unescape
compile(unescape(model_recipe), "embedded-foundry-recipe", "exec")
for required in ("not unique", "Activity", "Add Foundry agent", "GitHub Copilot harness", "fixtures/policy-tests.json",
                 "contracts/policy-answer.schema.json", "max_retries=0", "--allow-paid-calls"):
    assert required in foundry, f"Missing Foundry boundary: {required}"
assert "Flows &gt; New flow" not in studio and "Topic.Sku" not in studio
assert "Compare meaning &ge;85" not in studio and "standard-harness Foundry connected-agent" not in foundry
deck_js = (ROOT / "deck.js").read_text(encoding="utf-8")
assert "toggleNotes" not in deck_js and "notes-visible" not in deck_js
assert "presenter.html" in deck_js and "event.source !== presenterWindow" in deck_js
assert "aria-pressed" not in (ROOT / "index.html").read_text(encoding="utf-8"), "No audience notes toggle is allowed"
presenter = Deck()
presenter.feed((ROOT / "presenter.html").read_text(encoding="utf-8"))
for link in presenter.links:
    check_link(link, presenter.ids)
assert "Share only the audience window" in (ROOT / "presenter.html").read_text(encoding="utf-8")

schedule = json.loads((ROOT / "data" / "run-of-show.json").read_text(encoding="utf-8"))
elapsed = 0
covered = []
notes = re.findall(r'<template class="speaker-notes">(.*?)</template>', (ROOT / "index.html").read_text(encoding="utf-8"), re.S)
durations = [int(re.search(r", (\d+) minutes?\.", note)[1]) for note in notes]
for segment in schedule["segments"]:
    assert segment["startMinute"] == elapsed, "Timing gap or overlap"
    assert segment["minutes"] > 0
    elapsed += segment["minutes"]
    actual = [n for n, (_, name) in enumerate(deck.slides, 1) if name == segment["id"]]
    assert actual == segment["slides"], f"Chapter mapping differs: {segment['id']}"
    assert sum(durations[n - 1] for n in actual) == segment["minutes"], f"Presenter pacing differs: {segment['id']}"
    covered.extend(actual)
    start = segment["startMinute"]
    label = f"{start // 60:02}:{start % 60:02}-{elapsed // 60:02}:{elapsed % 60:02}"
    assert label in (ROOT / "deck.js").read_text(encoding="utf-8"), f"Toolbar timing differs: {label}"
    assert label in (ROOT / "index.html").read_text(encoding="utf-8"), f"Agenda timing differs: {label}"
    assert label in (ROOT / "attendee-guide.html").read_text(encoding="utf-8"), f"Guide timing differs: {label}"
    assert label in (ROOT / "README.md").read_text(encoding="utf-8"), f"Setup timing differs: {label}"
assert elapsed == schedule["durationMinutes"] == 120
assert covered == list(range(1, 49)), "Unscheduled or duplicate slide"
lab = re.search(r'<section id="lifecycle">(.*?)</section>', guide_text, re.S)[1]
for required in (
    "ms auth status", "ms auth login --device-code", "ms app clone",
    "ms app dev", "git push -u origin", "ms app play --mode preview --commit",
    "ms app build-status", "ms app deploy --commit", "ms app play --mode live",
    "src\\index.css", "bun run --parallel typecheck build:check lint",
    "oklch(0.45 0.12 150)", "oklch(0.64 0.13 150)",
    "709ff27e-269a-46b8-843a-c4eae1d9fe83", "71ea881b-016d-ec46-bde0-6d4b574f6012",
):
    assert required in lab, f"Missing lifecycle recipe detail: {required}"

fixture = json.loads((ROOT / "fixtures" / "expected-facts.json").read_text(encoding="utf-8"))
for product in fixture["products"]:
    folder = ROOT / "examples" / product["productId"]
    with (folder / "retailer-listing.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 1 and None not in rows[0], "CSV quoting or row shape failed"
    row = rows[0]
    expected = product["listing"]
    assert row["sku"] == expected["sku"] and row["title"] == expected["title"]
    assert row["manufacturer_msrp"] == f'{expected["msrp"]:.2f}'
    assert [row[f"bullet_{n}"] for n in range(1, 6)] == expected["bullets"]
    assert row["status"] == "needs_review" and row["synthetic"] == "true"
    assert row["gtin"] == row["image_assets"] == row["warranty_terms"] == ""
print("Deck: exactly three HTML files, 48 slides, 48 inert notes, one consolidated attendee guide with valid deep links, 120 contiguous minutes with matching note pacing, model-recipe syntax and two CSVs checked.")
