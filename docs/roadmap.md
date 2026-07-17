# Roadmap

## Phase 1: Inspectable Growth Loop — complete

- Runnable offline apprentice and skill memory.
- Assumption challenger and counterexample verifier.
- Eight-viewpoint `PerspectiveEngine`.
- Decompose, invert, recombine, and backsolve `ProblemTransformer`.
- Evidence-bearing `ExperienceRecord`.
- Confidence update and skill quarantine through `MemoryUpdater`.
- Backwards-compatible translation demo and a new reality-growth demo.

## Phase 2: Durable Local Memory

- Store skills and experiences as local, human-readable files.
- Add timestamps, applicability boundaries, provenance, review dates, and supersession links.
- Rebuild memory state from an append-only experience history.
- Import/export portable Skill Cards.
- Let users inspect, edit, approve, quarantine, restore, or delete memories.

## Phase 3: Evidence Adapters

- Generic JSON evidence interface.
- Optional AfterAI outcome adapter.
- Test, file, command, and human-feedback evidence adapters.
- Preserve raw evidence references without copying secrets into memory.
- Distinguish verified, failed, partial, and unknown outcomes.

## Phase 4: Teacher And Reasoning Adapters

- Local model adapter.
- OpenAI-compatible API adapter.
- Document and example adapters.
- Compare multiple proposed frames or skills.
- Keep source claims, inference, and uncertainty separate.

## Phase 5: Skill Evaluation

- Define repeatable tests for learned skills.
- Rank skills by applicability, evidence quality, recency, and cost.
- Detect contradictions between memories.
- Roll back or quarantine harmful rules.
- Search for counterexamples before reuse, not only before storage.

## Phase 6: Personal Agent Runtime

- Plan multi-step tasks from verifiable outcomes.
- Choose teachers, tools, and existing skills by expected value.
- Compare prediction with real execution evidence.
- Feed the resulting experience back into local memory.

## Phase 7: Skill Exchange

- Share portable Skill Cards between agents.
- Require each receiving agent to verify imported skills locally.
- Preserve provenance, evidence, versions, failures, and applicability.
- Prevent unverified confidence from propagating.

The long-term goal is not an agent that accumulates the most memory. It is one whose memory becomes more accurate because reality is allowed to correct it.
