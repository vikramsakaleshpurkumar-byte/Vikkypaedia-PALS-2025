# Test suites

Six Playwright suites that check the built `index.html` and `verify.html`. They open the files
directly from disk — no server, no network — and resolve paths relative to this folder, so they
run wherever the repository is cloned.

## Running them

```bash
pip install playwright
playwright install chromium

python build.py          # regenerate index.html from build/ first
python tests/test_full.py
python tests/test_ui.py
python tests/test_enrol.py
python tests/contrast.py
python tests/offline_test.py
python tests/print_test.py
python tests/test_loops.py
python tests/test_mega.py
```

Each prints `OK` / `FAIL` per check and ends with `FAILURES: none` when the build is sound.
`build.py` itself must print no `ERROR:` lines before any of these are worth running.

## What each one proves

| Suite | Checks |
|---|---|
| `test_full.py` | Part gating and lock enforcement (click, expand-all, hash), mastery reversal, tier/level/track filters, themes, the exam runner and scoring, the remediation plan, item review, the certificate canvas and print sheet, the configured-copy export, and a clean reload of that export in a fresh browser context |
| `test_ui.py` | Hints hidden on load and revealed one at a time, the progress ring and `--progress` and stat tiles and bar all agreeing, sticky topbar, styled mobile drawer, no horizontal scroll at 390 px, `scroll-behavior:auto` under reduced motion |
| `test_enrol.py` | The four-step first run and its required fields, plan recomputation, the profile bar and its persistence, Edit and Escape, the completion-record download and contents, and `verify.html` accepting a genuine record, rejecting a tampered score and surviving malformed JSON |
| `test_search.py` | The search palette: Ctrl+K and `/` opening, focus, result ranking and highlighting, that rationales and hints are **never** indexed (they would leak answers), that locked units appear but show no content, keyboard navigation, jumping into a unit or appendix, and the SVG figures rendering once with a text version and a working full-screen viewer |
| `contrast.py` | Computed foreground/background ratio on every text element that matters, in light **and** dark. Everything must read `ok` (≥4.5:1) |
| `offline_test.py` | Zero non-`file://` requests on load, on opening a unit and on switching theme |
| `test_sig.py` | The faculty signature upload: downscaling to 600 px, matting the paper out to transparency while keeping the ink, the preview and its stored size, the image drawn on the certificate canvas and into the print sheet, removal, and an exported copy that carries the signature in its seed without duplicating it in the DOM |
| `test_loops.py` | Standard v2 loops: one confidence bar per item, the confident-and-wrong flag, calibration, study days, the next-step card, the due badge and review runner (keys, Escape, scroll lock), unit and Part unlock notices, the Passport write and prefill, print-any-appendix, options flowing as text on mobile, and export hygiene |
| `print_test.py` | The certificate renders and the printed PDF is exactly one A4 page |

## Three things that will bite you

**Seed `onboarded` before loading.** The first-run overlay is modal and blocks every click.
Each suite already does this with `ctx.add_init_script(SKIP_ONB)`; any new test must too.

**Use `reduced_motion="reduce"` for screenshots.** Smooth scrolling otherwise produces
half-painted captures that look like layout bugs and are not.

**Never write `localStorage` and reload in one breath.** Chromium commits `file://` local
storage asynchronously, so a reload issued straight after a write can start the next document
before the write has landed — the page then boots from an empty store and the test fails
perhaps one run in six. Use the `seed_and_reload` helper, which writes, lets it settle,
reloads, checks the state actually took, and retries. This is a browser behaviour, not a
defect in the module: the module reads what is there and behaves correctly either way.
| `test_mega.py` | Megacode locking by Part; every case along its correct path (100%, no critical errors, key times met); wrong and critical calls; personal best kept over a worse run; option shuffling; keyboard play; live-region announcements; the strip description; contrast in both themes; the completion record and `verify.html` (including a tampered megacode score); 390 px width; no errors or network requests |
