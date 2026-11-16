from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from build import PLAN, ROOT, build, read_lectures


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.refs = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        anchor = attributes.get("id")
        if anchor:
            if anchor in self.ids:
                raise ValueError(f"Duplicate id {anchor}: {self.path}")
            self.ids.add(anchor)
        for name in ("href", "src"):
            if attributes.get(name):
                self.refs.append(attributes[name])


def digest(*paths):
    return hashlib.sha256(b"\0".join(path.read_bytes() for path in paths)).hexdigest()


def main():
    lectures = read_lectures()
    assert set(lectures) == set(range(1, 81)), "Expected all 80 playlist positions"
    assert len({item["video_id"] for item in lectures.values()}) == len(lectures)
    covered = []
    for first, last, _ in PLAN["chapters"]:
        covered.extend(range(first, last + 1))
    assert covered == list(lectures), "Chapters must map the playlist once in order"
    video_durations = {
        item["video_id"]: float(item["duration_seconds"]) for item in lectures.values()
    }

    html_paths = sorted(ROOT.glob("*.html")) + sorted((ROOT / "chapters").glob("*.html"))
    baseline = {path: digest(path) for path in html_paths}
    build()
    assert baseline == {path: digest(path) for path in html_paths}, "Rebuild changed output"

    pages = {path.resolve(): Page(path) for path in html_paths}
    timestamp_count = 0
    chapter_cues = {}
    for path, page in pages.items():
        for reference in page.refs:
            url = urlsplit(reference)
            if url.hostname == "www.youtube.com" and url.path == "/watch":
                query = parse_qs(url.query)
                video = query["v"][0]
                assert video in video_durations, reference
                if "t" in query:
                    seconds = int(query["t"][0].removesuffix("s"))
                    assert 0 <= seconds < video_durations[video], reference
                    timestamp_count += 1
                    chapter_cues.setdefault(path.name, set()).add(video)
            if url.scheme or url.netloc:
                continue
            link = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert link.is_relative_to(ROOT), (path, reference)
            assert link.exists(), (path, reference)
            if url.fragment and link in pages:
                assert unquote(url.fragment) in pages[link].ids, (path, reference)

    reports = []
    exercise_count = 0
    for number, (first, last, _) in enumerate(PLAN["chapters"], 1):
        cue_videos = {lectures[i]["video_id"] for i in range(first, last + 1)}
        assert chapter_cues.get(f"ch{number:02}.html") == cue_videos, number
        manuscript = ROOT / f"chapters/ch{number:02}.md"
        lab = ROOT / f"code/ch{number:02}.py"
        prose = manuscript.read_text(encoding="utf-8-sig")
        assert re.search(r"(?im)^## .*laboratory", prose), manuscript
        exercises = len(re.findall(r"(?im)^[ \t]*\*\*solution\b", prose))
        exercise_count += exercises
        result = subprocess.run(
            [sys.executable, lab], cwd=ROOT, check=True, capture_output=True,
            text=True, encoding="utf-8", timeout=30,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        reports.append({
            "chapter": number, "lectures": [first, last], "worked_solutions": exercises,
            "chapter_and_lab_sha256": digest(manuscript, lab), "lab_output": result.stdout.strip(),
        })

    summary = {
        "lecture_count": len(lectures), "chapter_count": len(reports),
        "html_pages": len(pages), "timestamped_section_links": timestamp_count,
        "worked_solution_markers": exercise_count, "labs": reports, "rebuild_identical": True,
    }
    (ROOT / "validation/checks.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n",
    )
    print(f"{len(pages)} pages, {len(lectures)} recordings, {timestamp_count} cue links, "
          f"{len(reports)} passing labs, deterministic rebuild")


if __name__ == "__main__":
    main()
