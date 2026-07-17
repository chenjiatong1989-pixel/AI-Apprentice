"""See a prediction become a revisable memory after reality answers back."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_apprentice import Apprentice, ExperienceRecord, Skill, SkillMemory


def main() -> None:
    memory = SkillMemory([Skill("launch-rule", "launch", "Add more features", confidence=0.6)])
    apprentice = Apprentice(memory, [])

    plan = apprentice.plan(
        "Launch an open-source AI tool",
        goal="Help a new visitor understand the value in 30 seconds",
        parts=("show one outcome", "show its evidence", "offer one command"),
        assumptions=("more features make the project easier to trust",),
    )

    print("Perspectives:", ", ".join(view.name for view in plan.views))
    print("Inversion:", plan.frame.inversions[1])
    print("Backsolve:", plan.frame.backsolved_steps[0])

    updated = apprentice.learn_from_reality(
        "launch-rule",
        ExperienceRecord(
            task=plan.frame.original_task,
            prediction="More features will improve first-time understanding",
            actual_outcome="Testers could not explain the core value",
            evidence=("3/3 tester summaries missed the core value",),
            matched=False,
            lesson="Show one verified outcome before adding breadth",
        ),
    )

    print("Reality:", memory.experiences[-1].delta)
    print("Updated confidence:", updated.confidence)
    print("Remembered lesson:", updated.failures[-1])


if __name__ == "__main__":
    main()
