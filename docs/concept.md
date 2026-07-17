# Concept

AI-Apprentice is a local-first framework for agents that become more useful through verified experience.

The central claim is simple:

> An answer is not learning. Learning is a prediction changed by reality.

## One Loop, Three Layers

### 1. See

The apprentice changes perspective before committing to a route. The default lenses are user, executor, system, designer, opposite, attacker, future, and outsider.

This “God view” does not mean omniscience. It means admitting that every single viewpoint is incomplete and deliberately moving between them.

### 2. Transform and act

The problem is decomposed, its assumptions are inverted, useful pieces are recombined, and actions are backsolved from evidence of the desired outcome. The apprentice then states a prediction before acting.

The transformation objects do not pretend to solve the problem. They make the frame inspectable so a model, tool, or person can supply the actual judgment.

### 3. Compare and remember

An `ExperienceRecord` preserves:

- situation and task
- prediction
- actual outcome
- evidence
- whether the prediction matched
- the delta between prediction and reality
- lesson and applicability
- counterexamples

`MemoryUpdater` raises confidence after evidenced success, lowers it after evidenced failure, and leaves it unchanged when evidence is missing. A repeatedly failing skill can be quarantined and excluded from reuse.

## Memory Is A Living Model

A useful memory system must preserve both conclusions and corrections. Every skill is therefore versioned, evidence-backed, and reversible.

> No rule is permanent. Every rule must be testable, replaceable, and reversible.

Failed predictions are especially valuable. Deleting them creates a system that remembers confidence but forgets why it was wrong.

## Teachers And Evidence

A teacher can be a model, human, document, example, or tool. A teacher proposes a lesson; reality decides how much confidence it deserves.

Evidence can come from tests, files, exit codes, human review, sensors, or another local tool. AfterAI is one optional source of normalized work evidence, not a required dependency.

## Facts, Inference, And Uncertainty

The apprentice should keep separate what evidence established, what it inferred, and what remains unknown. `matched=None` expresses an unknown comparison; it must never increase confidence.

## Local First

Personal learning should belong to the user. The prototype has no external dependency and keeps its primitives inspectable. Future persistence and adapters should preserve this property.
