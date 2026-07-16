"""Run a tiny offline AI-Apprentice learning loop demo."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_apprentice import Apprentice, SkillMemory, Teacher


def translation_teacher(task: str) -> str:
    return (
        "For English to Chinese product or idea translation, keep the meaning "
        "natural, short, and direct. Do not translate word by word. Preserve the "
        "main promise first, then polish the rhythm."
    )


def main() -> None:
    memory = SkillMemory()
    apprentice = Apprentice(
        memory=memory,
        teachers=[Teacher(name="translation-teacher", teach=translation_teacher)],
    )

    task = "Translate: Don’t build an AI that knows everything. Build one that never stops learning."

    print("First run:")
    print(apprentice.solve(task))
    print()

    print("Memory:")
    for skill in memory.skills:
        print(f"- {skill.name}: {skill.instruction}")
    print()

    print("Second run:")
    print(apprentice.solve(task))


if __name__ == "__main__":
    main()
