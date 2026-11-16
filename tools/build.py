from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "plan/chapters.json").read_text(encoding="utf-8-sig"))
ESC = html.escape


def read_lectures():
    with (ROOT / "lecture-inventory.csv").open(encoding="utf-8-sig", newline="") as file:
        return {int(row["lecture"]): row for row in csv.DictReader(file)}


def render_markdown(text):
    fragments = []
    pattern = re.compile(
        r"(?ms)^\x60{3,}.*?^\x60{3,}[^\S\n]*$|\x60[^\x60\n]+\x60|"
        r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<![\\$])\$([^$\n]+?)(?<!\\)\$(?!\$)"
    )

    def protect(match):
        expression = match.group()
        if expression.startswith(chr(96)):
            return expression
        is_display = expression.startswith("$$")
        tex = expression[2:-2].strip() if is_display else expression[1:-1]
        left, right = (r"\[", r"\]") if is_display else (r"\(", r"\)")
        if is_display:
            fragment = f'<div class="equation">{left}{ESC(tex)}{right}</div>'
            token = f"\n\n<div data-equation=\"{len(fragments)}\"></div>\n\n"
        else:
            fragment = f'<span class="math">{left}{ESC(tex)}{right}</span>'
            token = f'<span data-equation="{len(fragments)}"></span>'
        fragments.append(fragment)
        return token

    protected = pattern.sub(protect, text)
    rendered = markdown.markdown(
        protected,
        extensions=["extra", "toc"],
        extension_configs={"toc": {"toc_depth": "2"}}
    )

    def restore(match):
        return fragments[int(match.group(1))]

    rendered = rendered.replace("<table>", '<div class="table-wrap"><table>').replace(
        "</table>", "</table></div>"
    )
    return re.sub(r'<(?:span|div) data-equation="(\d+)"></(?:span|div)>', restore, rendered)


def page(title, body, *, prefix="", class_name="reading", math=False, search=False):
    if math:
        scripts = (
            f'<script defer src="{prefix}assets/math-config.js"></script>'
            f'<script defer src="{prefix}assets/mathjax-tex-svg.js"></script>'
        )
    else:
        scripts = ""
    if search:
        scripts += f'<script defer src="{prefix}assets/search.js"></script>'
    nav = "".join(
        f'<a href="{prefix}{url}">{label}</a>'
        for url, label in [
            ("index.html", "Chapters"), ("study-guide.html", "Study guide"),
            ("source-map.html", "Lectures"), ("laboratory.html", "Labs"),
        ]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light">
<title>{ESC(title)} · Matrix Theory</title>
<link rel="stylesheet" href="{prefix}assets/reader.css">
{scripts}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <a class="brand" href="{prefix}index.html">Matrix Theory</a>
  <nav aria-label="Reader">{nav}</nav>
</header>
<main id="main" class="{class_name}">{body}</main>
<footer>Independent study edition · <a href="{ESC(PLAN["course"])}">NPTEL course</a></footer>
</body>
</html>
"""


def write(relative, text):
    (ROOT / relative).write_text(text, encoding="utf-8", newline="\n")


def chapter_link(chapter, label, prefix=""):
    return f'<a href="{prefix}chapters/ch{chapter:02}.html">{ESC(label)}</a>'


def lecture_link(lecture, item, *, title=False):
    label = f'{lecture}. {item["title"]}' if title else f"L{lecture}"
    return f'<a href="https://www.youtube.com/watch?v={item["video_id"]}">{ESC(label)}</a>'


def build(*, preview=False):
    lectures = read_lectures()
    chapter_plan = PLAN["chapters"]
    ready = {
        number for number in range(1, len(chapter_plan) + 1)
        if all((ROOT / path).exists() for path in [
            f"chapters/ch{number:02}.md", f"code/ch{number:02}.py"
        ])
    }
    if not preview and len(ready) != len(chapter_plan):
        raise ValueError(f"Missing chapter/lab pairs: {sorted(set(range(1, 21)) - ready)}")

    cards, source_rows, labs = [], [], []
    for number, (first, last, name) in enumerate(chapter_plan, 1):
        if number not in ready:
            continue
        draft = (ROOT / f"chapters/ch{number:02}.md").read_text(encoding="utf-8-sig")
        title_line, _, manuscript = draft.partition("\n")
        if not title_line.startswith("# "):
            raise ValueError(f"Chapter {number} must start with a level-one title")
        chapter_title = title_line[2:].strip()
        sources = " ".join(lecture_link(i, lectures[i]) for i in range(first, last + 1))
        previous = (
            chapter_link(number - 1, "← Previous chapter", "../")
            if number - 1 in ready else ""
        )
        following = (
            chapter_link(number + 1, "Next chapter →", "../")
            if number + 1 in ready else ""
        )
        end_nav = f'<nav class="chapter-nav" aria-label="Chapter order">{previous}{following}</nav>'
        opening, separator, sections = manuscript.partition("\n## ")
        with_toc = opening + "\n\n[TOC]\n\n" + separator + sections
        content = render_markdown(with_toc)
        heading = (
            f'<p class="context">Chapter {number} · <a href="../source-map.html#l{first:02}">'
            f'Lectures {first}–{last}</a></p><h1>{ESC(chapter_title)}</h1>'
            f'<nav class="recordings" aria-label="Source recordings">{sources}</nav>'
        )
        write(f"chapters/ch{number:02}.html",
              page(chapter_title, heading + content + end_nav, prefix="../", math=True))
        topics = " · ".join(ESC(lectures[i]["title"]) for i in range(first, last + 1))
        cards.append(
            f'<li value="{number}"><h3>{chapter_link(number, name)}</h3>'
            f'<p class="context">Lectures {first}–{last}</p><p>{topics}</p></li>'
        )
        labs.append(
            f'<li>{chapter_link(number, name)}'
            f'<a href="code/ch{number:02}.py" download>Python source</a></li>'
        )
        for i in range(first, last + 1):
            item = lectures[i]
            source_rows.append(
                f'<tr id="l{i:02}"><td>{lecture_link(i, item, title=True)}</td>'
                f'<td>{chapter_link(number, f"Chapter {number}")}</td>'
                f'<td>{ESC(item["source_basis"])}</td></tr>'
            )

    groups = [("Foundations", 0, 8), ("Spectra and factorization", 8, 14),
              ("Hermitian spectra and inverse problems", 14, 20)]
    if preview:
        contents = '<ol class="chapters">' + "".join(cards) + '</ol>'
    else:
        contents = "".join(
            f'<section><h2>{title}</h2><ol class="chapters" start="{start + 1}">'
            + "".join(cards[start:stop]) + "</ol></section>"
            for title, start, stop in groups
        )
    index = (
        '<div class="intro"><p class="context">Independent notes for NPTEL course 111108157</p>'
        '<h1>Matrix Theory</h1><p class="summary">Learn when a matrix model determines '
        'a state, how its spectrum controls behavior, and what survives small changes '
        'in the data. Follow proofs with worked problems and numerical experiments.</p>'
        f'<p class="context">Chandra R. Murthy · IISc Bangalore · {len(lectures)} recordings · '
        f'{len(ready)} chapters</p></div>'
        '<div class="search" role="search" hidden><label for="chapter-query">Filter by topic</label>'
        '<input id="chapter-query" type="search" autocomplete="off">'
        '<p id="chapter-count" aria-live="polite"></p></div>' + contents
    )
    write("index.html", page("Course reader", index, class_name="catalog", search=True))
    source_intro = (
        '<h1>Lecture map</h1><p>Each recording is linked in playlist order. '
        'The notes include independent examples, proofs, and computational experiments. '
        'Section links use caption cues when confirmed. '
        'Caption checks provide text evidence for the topics and timing. Coverage is based on playlist metadata, English captions, and the linked companion material. The project did not perform a full audio or frame review.</p>'
        f'<p><a href="{ESC(PLAN["playlist"])}">Watch the NPTEL playlist</a> · '
        '<a href="https://ece.iisc.ac.in/~cmurthy/index.php/e2-212-matrix-theory-video-lectures-and-notes-2/">'
        'IISc companion notes</a> · '
        '<a href="lecture-inventory.csv">Download the lecture inventory</a></p>'
    )
    write("source-map.html", page("Lecture map", source_intro +
          '<div class="table-wrap"><table><thead><tr><th>Recording</th><th>Notes</th>'
          '<th>Source</th></tr></thead><tbody>' + "".join(source_rows) +
          '</tbody></table></div>', class_name="catalog"))
    write("laboratory.html", page("Laboratories", '<h1>Laboratories</h1><p>Install '
          '<code>requirements.txt</code>. Run a lab with <code>python code/ch01.py</code> '
          'or change the chapter number. Each script checks its results with assertions.'
          '</p><ol class="lab-list">' + "".join(labs) + '</ol>'))
    guide = (ROOT / "plan/study-guide.md").read_text(encoding="utf-8-sig")
    write("study-guide.html", page("Study guide", render_markdown(guide), math=True))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build the Matrix Theory reader.")
    parser.add_argument("--preview", action="store_true", help="Render available chapters.")
    build(preview=parser.parse_args().preview)
