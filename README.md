# Big Red — Accessible AI Navigator
An independent Cornell resource discovery MVP for a Human-centered AI / Accessibility / UX portfolio. Not affiliated with Cornell.

## Run in one minute
Requires Python 3.10+; no packages, account, API keys, or external network calls at runtime.

```sh
git clone https://github.com/maxi-9150/big-red-navigator.git
cd big-red-navigator
python3 server.py
```
Open http://127.0.0.1:8000. From this project folder, use `python3 server.py --port 8001` for another port. Stop with Ctrl+C. If you downloaded just this project, `cd` into its folder first.

```sh
python3 -m unittest discover -s tests -v
```

## Big Red update
The product is a bilingual resource discovery and organization workspace: search or browse → review official sources → add resources to a topic-grouped kit → write next steps → export a text plan. English/Chinese switch covers the interface, curated summaries, result messages, and exports. Official source pages remain in their original languages; translations are project paraphrases, not official translations.

Saved resource IDs and notes live in browser localStorage (`bigred-kit`); language preference lives in `bigred-language`. Notes are never sent to the server or an LLM. Remove a resource to delete its note. Clear this site's browser data to erase all saved preferences. Shared-device users should remove saved notes before leaving. Text exports include the user's notes, official URLs, and review dates.

The original roaring bear icon is generated with the built-in imagegen tool, inspired by Cornell collegiate bear imagery. It is not an official Cornell logo. Palette uses red `#b31b1b` with white. Brand inspiration: [Cornell official licensing guide](https://brand.cornell.edu/downloads/merchandising/Cornell_Licensing_Brand_Guide.pdf). Asset and prompt details: `docs/ASSET_PROVENANCE.md`.

## What works
- Natural language keyword retrieval over four reviewed official resource summaries, with limited Chinese aliases.
- Evidence-only response composition, claim-level source links, next steps, review dates, and explicit evidence limitations. This is the no-key demo path, not an LLM or semantic vector search.
- Refuses unsupported questions; routes personal eligibility and volatile details to official offices. Related summaries are discovery aids, not proof that a specific request is answerable.
- Non-chat topic browsing, native forms, keyboard focus, live status announcements, responsive layout, no motion, readable contrast.
- Feedback type, optional resource, and optional note stored in local SQLite. No analytics or saved question history.

## Source provenance
`data/resources.json` holds manually curated paraphrases of official pages reviewed on **2026-11-05**. They are real resource summaries, not fabricated services. Questions shown in the UI are **example inputs**, not student research data. `verified_on` is our review date, **not** the publisher’s update date. Publisher update dates were not established and are null. No live availability, approval rules, pricing, contact hours, or deadlines are claimed. Records older than 90 days are flagged in answer cards. Seed collection is deliberately small and primarily Ithaca-oriented; Cornell Tech and Weill coverage is incomplete.

Sources: [SDS accommodations](https://sds.cornell.edu/accommodations-services), [SDS FAQ](https://sds.cornell.edu/get-started/faqs), [International Services advice](https://international.globallearning.cornell.edu/get-advice), [Cornell Health CAPS](https://health.cornell.edu/services/mental-health-care).

## Architecture and expansion
`static/` → JSON HTTP routes in `server.py` → `Navigator` in `engine.py` → injectable `Retriever` / `AnswerProvider` protocols → curated JSON. The default provider returns only stored summaries. It does not send the query anywhere.

To use real RAG, implement `Retriever.retrieve(question)` returning records with the existing schema and inject it into `Navigator(retriever=...)`. Start with approved official pages, clean headings and chunks, retain canonical URLs, capture fetch dates, record content hashes, and index chunks with embeddings/BM25. The MVP retrieves whole resource cards, not automatically ingested documents.

For a real LLM, implement `AnswerProvider.compose(question, evidence)` and inject it with `Navigator(provider=...)`. Return `{status, message, claims:[{text, source_id, next_step}]}`. Keep keys server-side in environment variables; never in frontend code. Configure your chosen provider’s SDK, timeouts, token budget, and retry policy in that adapter. No provider integration is bundled or silently enabled. Explain remote data transfer and obtain consent before sending student questions externally.

The current citation validator rejects references outside retrieved evidence, but **cannot prove semantic entailment**. A production adapter needs evidence coverage checks, adversarial source/prompt tests, and a fail-closed fallback. Do not enable generated answers based on valid citation IDs alone. Add hybrid retrieval, bilingual content review, chunk-level citations, stale-source suppression, and escalation routing before a broader launch.

## Privacy and operation
Development server binds to loopback only. It does not log request bodies or paths. Feedback notes are stored unencrypted in `data/feedback.sqlite3`; delete this file to reset them. Review with Python’s sqlite3 module or a SQLite viewer. Feedback is not delivered to Cornell and has no urgent-response workflow. Do not collect disability documentation, immigration identifiers, or medical history. Browser extensions and the OS are outside this app’s privacy boundary.

Do not expose this development server publicly. A hosted release needs HTTPS, rate limiting, request timeouts, stricter origin/host checks, authentication for feedback review, storage permissions, retention/deletion controls, and security review. External official links use the same tab so navigation remains predictable.

## Portfolio and evaluation
See [design and evaluation](docs/DESIGN_EVALUATION.md) and [verification record](docs/VERIFICATION.md). Accessibility is a WCAG 2.2 AA **target**, not a certification. No user study or screen reader validation is claimed.
