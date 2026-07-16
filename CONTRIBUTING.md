# Contributing

AI-Apprentice is early, so the best contributions make the idea easier to run, test, or understand.

Good first contributions:

- improve the offline demo
- add a new teacher adapter
- improve skill memory
- add verification examples
- write clearer docs
- add tests for learning-loop behavior

## Development

Run the demo:

```bash
python examples/translation_loop.py
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Principles

- Keep examples small and inspectable.
- Prefer local-first behavior.
- Do not add paid API requirements to the core demo.
- Treat teacher output as something to verify, not blindly trust.
- Turn repeated behavior into reusable skills.
