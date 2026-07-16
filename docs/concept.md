# Concept

AI-Apprentice is a framework for personal AI systems that learn through use.

The central claim is simple:

> The next useful personal AI is not the one that knows everything. It is the one that learns from every useful interaction.

## The Apprentice Pattern

An apprentice does not start as a master. It improves by repeatedly doing five things:

1. Try the work.
2. Notice the gap.
3. Ask a teacher or inspect a better example.
4. Practice and verify.
5. Write down the reusable lesson.

AI-Apprentice applies that pattern to AI agents.

## Teacher Sources

A teacher can be:

- a stronger model
- a specialist model
- a local document
- a browser session
- a human correction
- a tool result
- a previous successful task

The teacher is not blindly copied. Its output is compared, verified, and compressed into a reusable skill.

## Skill Memory

A skill is a small reusable unit of behavior:

- when to use it
- what it teaches
- examples that prove it works
- where it came from
- when it should be reviewed

The first prototype uses an in-memory list. Future versions should store skills as portable local files.

## Local First

Personal learning should belong to the user. The framework should work locally where possible, with optional adapters for API models and online tools.
