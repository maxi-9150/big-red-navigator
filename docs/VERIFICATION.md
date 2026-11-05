# Verification record — 2026-11-05

## Completed
- Python 3.11.5: 12 automated tests pass (`python3 -m unittest discover -s tests -v`). Tests cover evidence citations, Chinese keyword discovery, unsupported queries, personal eligibility limits, instruction-like query safety in the non-generative provider, invalid adapter citations, official source domains, HTTP response headers, input validation, persistent feedback, cross-origin rejection, and path traversal.
- Server started at http://127.0.0.1:8000; homepage and API served successfully.
- Browser showed all four resources and correctly labeled native controls in its accessibility tree.
- Submitted “I need exam accommodations” in browser. Result included the SDS official link, curated summary, next action, review date, unknown publisher update date, and local-mode explanation. Result heading received focus.
- Narrow browser screenshot inspected: stacked layout, wrapped text, and full-width native fields. See `demo-home.png` and `demo-mobile.png`.

## Not established
- Full keyboard-only task completion. A Tab interaction reached the submit button, but browser automation key behavior was inconsistent, so this is not recorded as a full pass.
- VoiceOver/NVDA speech behavior, 400% zoom, every contrast/focus state, forced colors, and comprehensive WCAG 2.2 AA audit.
- Student usability results, real LLM behavior, vector retrieval quality, source refresh automation, production security, and hosting load.

A browser accessibility tree is useful structural evidence but is not a substitute for assistive technology testing. HTTP feedback persistence was tested in an isolated temporary database; no real student feedback was collected.

## Big Red redesign verification
- 14 automated tests pass after adding localized answer and bilingual seed-field checks.
- Browser: switched English → Chinese; headings, summaries, forms, and result controls translated. Language preference survived reload.
- Browser: searched “international visa,” received one relevant official resource, and result heading received focus.
- Browser: added that resource to the kit; navigation and kit count became 1. Entered an example next-step note; both saved resource and note survived reload.
- Browser: export control produced the download-complete status. Export file contents were not separately inspected in the browser test.
- Browser: removed the test resource; count returned to 0. No sample note remains in the demo kit.
- Narrow-window screenshots inspected and adjusted the Chinese headline and header spacing. Desktop DOM structure checked; desktop visual inspection was limited because the embedded browser clipped the wider viewport. Comprehensive desktop visual QA remains open.
- Screenshots: `big-red-home-zh.png`, `big-red-kit.png`. Kit screenshot contains test-only sample text.
- Full keyboard-only and screen reader task testing remains outstanding. No claim of audited WCAG conformance.
