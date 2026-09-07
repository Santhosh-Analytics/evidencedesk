I propose these nodes:

Node Responsibility
plan_search LLM generates focused queries
search_web Search provider returns titles, URLs, snippets
fetch_pages Download and extract article text
extract_findings LLM extracts relevant evidence per article
assess_evidence Identify gaps; propose another search or finish
write_report Summarise findings with citations and limitations

Python should enforce a search limit even when the LLM requests more.

Minimum State fields:

Field Contents
question Original research question
countries Explicit geographic scope
date_range What “current” means
queries Queries awaiting execution
searched_queries Queries already attempted
sources Retrieved article records
findings Evidence linked to source IDs
gaps Unanswered points
search_round Counter for stopping
decision Search again or write
report Final cited summary
errors Retrieval or processing failures

The graph, node by node:

run_seed_queries — walks your fixed query list (you'll write ~6-10 queries split across both threads), calls Tavily once per query, gets back raw results
register_sources — Python, not LLM — takes Tavily's raw results, assigns each a Source ID, dedupes by URL, stores title/URL/content. This is the deterministic layer from the pack's philosophy: the model never invents a source ID.
extract_finding — LLM node, one call per source — reads that source's content, distills it into a finding, tags it as Thread A or B, gives a confidence level. This loops until all sources processed (or budget hit).
synthesize — LLM node, single call over all findings together — produces two separate summaries (market-state, transition-feasibility) plus caveats about weak evidence.

State fields, with why each exists:

Field Type Why
seed_queries list[str] your fixed query list, set once, not model-generated
sources list[Source] each: id (int, Python-assigned), url, title, raw_content
findings list[Finding] each: id, source_id (links back — traceability), category ("market_state" | "transition_feasibility"), text, confidence
calls_used int running counter against your budget
max_calls int the ceiling you set
market_summary str | None filled only at the end by synthesize
transition_summary str | None same
caveats list[str] e.g. "only

One thing to draft yourself before coding anything: the actual 6-10 seed queries, split roughly evenly across both threads (e.g., "AI ML job market India 2026", "BPO to data analyst career switch experience", "non-technical background machine learning engineer transition"). Want to draft that list together, or write it yourself and bring it back for review?

Do experienced BPO professionals move into AI/ML
India BPO to machine learning career transition experienced professionals
