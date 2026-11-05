# Design and evaluation case study

## Problem and product hypothesis
Students may know what they need without knowing which office owns the answer. Disability disclosure, unfamiliar institutional vocabulary, language barriers, and scattered pages can make resource discovery difficult. These are design hypotheses, not findings from conducted research.

This MVP explores whether a source-first navigator helps students find a relevant office and a clear next action while recognizing what the tool cannot establish. Success means useful navigation and calibrated reliance, not longer chat sessions.

## Intended users and decisions
- A student seeking exam access can search without entering a diagnosis and reach SDS.
- An international student can discover advising through visa keywords without receiving invented immigration advice.
- A student who dislikes chat can browse every resource using ordinary links and topic filters.

The visual hierarchy begins with a single question field, places the trust boundaries alongside it, and keeps a complete browsing alternative directly below. No identity classification or disability profile is required. The interface, curated summaries, feedback controls, result states, and exports are available in English and Chinese. Retrieval remains limited keyword matching with Chinese aliases; bilingual UI does not establish multilingual retrieval parity.

## Trust design
Each returned summary has its own official citation and next action. We show review date and explicitly unknown publisher update date, avoiding a false “last updated” signal. We expose limited evidence rather than a confidence percentage. Keyword overlap is not factual certainty. Unknown topics produce abstention. Personal eligibility and volatile details trigger a limitation message. The user can report inaccurate, outdated, or inaccessible content without giving contact details.

The main tradeoff is scope versus answer coverage: curated summaries avoid unreviewed generation but cannot answer detailed policy questions. Even a related result may not answer the question. This limitation is visible in the interface and API.

## WCAG 2.2 AA implementation map
| Area | Implementation | Required validation |
|---|---|---|
| 1.3.1 / 4.1.2 | Semantic headings, landmarks, native controls, associated labels | Screen reader landmark and form navigation |
| 1.4.3 | Dark green text, pale backgrounds, underlined links | Contrast measurement for every state |
| 1.4.10 | Single column at narrow widths, wrapping content | 320 CSS px and 400% zoom |
| 2.1.1 / 2.4.3 | Native keyboard controls, DOM reading order | Complete all tasks without a pointer |
| 2.4.1 | Skip to main link | Tab then activate |
| 2.4.7 / 2.4.11 | High visibility purple focus, no sticky overlays | Check every interactive element |
| 2.5.8 | Controls at least 46 px high, spaced links | Target size and inline exceptions review |
| 3.3.1 / 3.3.2 | Required fields, length limits, visible errors | Invalid submit and recovery |
| 4.1.3 | Polite result and feedback status; result heading focus | VoiceOver/NVDA announcements |

No time limits, animation, drag interactions, or custom widgets. No-JS official links remain available. An accessibility audit is still needed; implementation mapping does not establish compliance.

## Proposed research, not completed evidence
Recruit 6–8 consenting students across disability/access needs and international student experience. Include screen reader and keyboard users. Do not require a diagnosis or immigration status disclosure; offer alternative formats and compensation. Ask participants to locate accommodations, international advising, wellbeing support, and an intentionally unsupported resource, then verify a claim against its source.

Measure task success, time to relevant official page, mistaken reliance on unsupported content, recognition of review-date limits, and perceived effort. Compare the question flow with browse-first discovery; avoid claiming causal benefit from a small convenience sample. Invite participants to challenge terminology and identify missing campus/program coverage.

Release gates: every factual answer claim traceable to evidence; all unsupported evaluation prompts abstain; no unresolved critical keyboard/screen reader barriers; participant review of revised flows. These are proposed gates, not reported outcomes. Collect qualitative failure cases alongside counts.

## Portfolio narrative
Position as an **AI Product / Human–AI Interaction prototype**: problem framing → trust and access requirements → evidence-first architecture → working no-key prototype → evaluation plan and documented limits. The contribution is interaction and reliability design, not a claim to have trained an AI model or proven student outcomes. Show a supported answer, an abstention, the browsing path, and a feedback report in a short demo.

## Big Red: resource workspace iteration
The redesign replaces the chat-like answer panel with a continuous resource workspace. Search narrows the same cards used in browsing. Each card has a source, a recommended next step, and a save control. Saved resources are grouped by topic and accept an editable action note. Text export keeps sources and review dates with the plan, supporting handoff to an advisor or personal planning without requiring an account.

The red/white visual system and original roaring bear establish a memorable identity. The independent-project notice remains explicit. Reduced motion, native buttons, clear blue focus, persistent status messages, and translated document language are retained. New local persistence trades convenience for shared-device exposure; the interface explains storage and removal. Notes are user-authored plans, not approved accommodations or eligibility determinations.
