# Concept

AI-Apprentice is a framework for personal AI systems that learn through use.

The central claim is simple:

> The next useful personal AI is not the one that knows everything. It is the one that learns from every useful interaction.

## The Apprentice Pattern

An apprentice does not start as a master. It improves by repeatedly doing seven things:

1. Question the assumed route.
2. Try the work.
3. Notice the gap.
4. Ask a teacher or inspect a better example.
5. Search for counterexamples and verify.
6. Write down the reusable lesson.
7. Replace the lesson when a better one appears.

AI-Apprentice applies that pattern to AI agents.

## Beyond Blind Learning

Learning is not enough. A system that permanently remembers every lesson will also permanently remember mistakes.

AI-Apprentice therefore treats every rule as a temporary, testable strategy:

> No rule is permanent. Every rule must be testable, replaceable, and reversible.

Before following the obvious process, the apprentice should ask:

- What is the real goal?
- Which assumptions are constraints, and which are merely habits?
- Is there a shorter path to the same verified outcome?
- What evidence would prove this lesson wrong?

This is not permission to ignore safety or evidence. It is a method for finding better paths without confusing confidence with truth.

## Teacher Sources

A teacher can be:

- a stronger model
- a specialist model
- a local document
- a browser session
- a human correction
- a tool result
- a previous successful task

The teacher is not blindly copied. Its output is compared, challenged, verified, and compressed into a reusable skill.

## Skill Memory

A skill is a small reusable unit of behavior:

- when to use it
- what it teaches
- where it came from
- evidence and known failures
- confidence and version
- when it should be reviewed

Skills are replaceable. A newer, better-tested version can supersede an older rule, and a failed skill can be rejected or rolled back.

The first prototype uses an in-memory list. Future versions should store skills as portable local Skill Cards that another agent can import and independently verify.

## Facts, Inference, And Uncertainty

The apprentice should preserve the difference between:

- what a source directly established
- what the apprentice inferred
- what remains uncertain

A useful agent should not hide uncertainty behind confident language.

## Local First

Personal learning should belong to the user. The framework should work locally where possible, with optional adapters for API models and online tools.

The long-term goal is not more answers. It is a personal AI that learns enough to complete useful work while keeping its reasoning, evidence, and learned skills inspectable.
