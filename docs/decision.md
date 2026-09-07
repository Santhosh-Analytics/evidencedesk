# ADR-001: EvidenceDesk research workflow and evidence contracts

Date: 2026-09-07
Status: Design agreed; implementation incomplete

## Context

EvidenceDesk researches AI/ML hiring and career transitions from accounts/BPO backgrounds. It also serves as a learning project for implementing LangGraph state, nodes, structured outputs, and bounded execution.

## Decision

Use Python 3.13, uv, Pydantic, pydantic-settings, LangGraph, and local Ollama inference.

Accept multiple research questions and shared research scope in `ResearchRequest`.

Create graph state before the first model call. State holds the request, query expansion, sources, findings, counters, summaries, and caveats.

Use a separate query-expansion model to associate each original question with two or three search phrases. Store its result in state, initially `None`.

The intended initial graph is:

1. Expand questions into search phrases.
2. Search and fetch public sources.
3. Extract evidence from each source.
4. Compose a cited report.
5. Validate and save.

Automatic additional research rounds are deferred.

## Evidence handling

Sources record URLs, fetch status, timestamps, content, and content hash. Failed fetches retain known metadata; unavailable content and retrieval timestamps remain absent. Publication dates may be unknown.

Findings contain a claim, source ID, category, evidence kind, verbatim excerpt, and limitation.

Python assigns IDs, verifies references and excerpts, enforces budgets, and resolves citation links. A matching excerpt establishes traceability, not truth.

## Logging and exceptions

Use application-specific exceptions and configurable logging. Configure handlers once. Log caught exceptions with traceback information when needed; logging does not itself determine retry or recovery behavior.

## Consequences

Explicit contracts make intermediate results inspectable. They require additional validation and failure handling. Individual accounts, employer requirements, and aggregate evidence must remain distinguishable.

## Outstanding implementation work

- Add query expansion to state.
- Make `published_at` nullable.
- Validate successful-fetch completeness and nonblank text.
- Record actionable failure details in state.
- Define what counts toward `max_calls` and enforce it before operations.
- Define confidence criteria or defer confidence.
- Review import-time exception settings initialization.
- Repair examples and verify logging with the actual settings.
- Implement and test graph nodes.

## Reference

[LangGraph graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
