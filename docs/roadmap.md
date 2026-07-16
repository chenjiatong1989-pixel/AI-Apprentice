# Roadmap

## Phase 1: Clear Prototype

- Define the learning-loop concept.
- Add a runnable offline demo.
- Add a minimal skill memory.
- Add optional assumption-challenger and verifier primitives.
- Document the project philosophy.
- Keep the project easy to understand for first-time GitHub visitors.

## Phase 2: Real Skill Memory

- Store skills as local files.
- Add metadata: source, confidence, evidence, known failures, version, last used, and review date.
- Add import/export support through portable Skill Cards.
- Add skill search and ranking.
- Allow a newer verified skill to replace an older strategy.

## Phase 3: Teacher Adapters

- Add local model adapter.
- Add OpenAI-compatible API adapter.
- Add document teacher adapter.
- Add browser observation adapter.
- Add human feedback adapter.

## Phase 4: Verification And Self-Correction

- Add compare-and-rank strategies.
- Search for counterexamples before accepting a skill.
- Add tests for learned skills.
- Separate facts, inference, and uncertainty.
- Add confidence scoring and failure logs.
- Add rollback and quarantine for bad skills.
- Periodically review whether an old rule still deserves to exist.

## Phase 5: Shortcut Search And Personal Agent Runtime

- Identify the real goal before committing to a process.
- Separate true constraints from inherited assumptions.
- Compare direct completion, tool use, teacher use, and skill reuse by cost and verified outcome.
- Let the apprentice plan multi-step tasks.
- Let it choose teachers and tools.
- Let it reuse skills across sessions.
- Let users inspect, edit, approve, or delete learned skills.

## Phase 6: Eyes And Ears

- Browser observation.
- File observation.
- Voice input.
- Vision input.
- Real-world feedback loops.

## Phase 7: Skill Exchange

- Share portable Skill Cards between agents.
- Require each receiving agent to verify imported skills locally.
- Preserve provenance, evidence, versions, and known failures.
- Prevent unverified skill propagation.

The long-term goal is a personal AI that becomes more useful because it keeps learning from the user's real life and real tasks, questions what it learned, and replaces it when a better path appears.
