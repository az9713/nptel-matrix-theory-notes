# Lecture-note production workflow

This edition follows the earlier NPTEL reader workflow. The exact upload
order and video IDs in the supplied playlist determine the source map.
The 38 longer IISc companion sessions use their own numbering.

1. Inventory the 80 recordings and acquire available English subtitle tracks.
   Keep subtitle data and work copies under `work/`. Record track choice,
   endpoint and digest in [the public inventory](lecture-inventory.csv).
2. Group consecutive recordings by mathematical dependency. Use the captions
   for topic checks and section navigation. The original problems, proofs, and
   numerical experiments develop the material independently. Caption text can
   misrecognize notation. The project used caption cues and selected companion
   material. Audio and slide frames were outside the systematic review.
3. Draft chapters in order within each author assignment. State assumptions
   beside results, show proof hinges, and test conclusions through examples
   and deterministic Python labs. Use a common notation and review brief.
4. Run independent editorial and mathematical reviews. Keep judgments and
   repairs in [the review summary](validation/reviews.md).
5. Rebuild the static reader and check chapter pairs, lecture coverage,
   anchors, each lab, and determinism. Render each reader page at desktop
   and mobile widths and exercise the topic filter.
6. Inspect the staged public tree and push the release. The GitHub Actions
   publication workflow checks every chapter at desktop and mobile widths
   and deploys only after those checks pass.

Run `python -m pip install -r requirements.txt`, then `python tools/build.py`
and `python tools/check.py`. To regenerate the original figures, run
`python figures/make_figures.py`. The rebuild uses only checked-in inputs.

The optional browser check uses Playwright. Install it with
`python -m pip install playwright` and `python -m playwright install chromium`,
or pass `--browser` with the path to an existing Chromium executable. Then
run `python tools/browser_check.py`. The `--base-url` option checks a deployment.

## GitHub Pages

The [publication workflow](.github/workflows/publish.yml) runs on pull requests
to `main`, pushes to `main`, and manual runs. It tests the exact staged site
at 1440 px and 390 px. The check fails for visible inline scrollbars, clipped
wide equations, page overflow, or math rendering errors. Successful runs on
`main` publish the tested files.

To run the math check directly, install the browser dependencies above and
pass one or more generated chapter paths to `python tools/check_math_layout.py`.
Use `--chrome` with the path to an installed browser if needed.
