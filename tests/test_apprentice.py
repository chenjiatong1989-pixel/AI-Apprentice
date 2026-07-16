import unittest

from ai_apprentice import (
    Apprentice,
    AssumptionChallenger,
    Skill,
    SkillMemory,
    Teacher,
    Verifier,
)


class ApprenticeTests(unittest.TestCase):
    def test_learns_and_reuses_skill(self) -> None:
        calls = []

        def teacher(task: str) -> str:
            calls.append(task)
            return "Use a natural, concise translation style."

        memory = SkillMemory()
        apprentice = Apprentice(memory=memory, teachers=[Teacher("demo", teacher)])

        first = apprentice.solve("Translate a slogan")
        second = apprentice.solve("Translate another slogan")

        self.assertEqual(len(calls), 1)
        self.assertEqual(len(memory.skills), 1)
        self.assertIn("demo:translate:style", first)
        self.assertIn("demo:translate:style", second)
        self.assertEqual(memory.skills[0].source, "demo")

    def test_handles_missing_teacher(self) -> None:
        apprentice = Apprentice(memory=SkillMemory(), teachers=[])

        result = apprentice.solve("Summarize this document")

        self.assertIn("do not have a teacher yet", result)

    def test_questions_assumptions_before_learning(self) -> None:
        seen_tasks = []
        challenger = AssumptionChallenger(
            "shorter-path",
            lambda task: f"Translate the goal directly instead of following every step: {task}",
        )
        teacher = Teacher("demo", lambda task: seen_tasks.append(task) or "Keep only the goal.")
        apprentice = Apprentice(SkillMemory(), [teacher], challenger=challenger)

        result = apprentice.solve("Rewrite this slogan")

        self.assertIn("Reframed task", result)
        self.assertIn("Translate the goal directly", seen_tasks[0])

    def test_rejected_skill_is_not_remembered(self) -> None:
        memory = SkillMemory()
        verifier = Verifier("counterexample-check", lambda task, skill: False)
        apprentice = Apprentice(
            memory,
            [Teacher("untrusted", lambda task: "Always translate word by word.")],
            verifier=verifier,
        )

        result = apprentice.solve("Translate a slogan")

        self.assertIn("rejected skill", result)
        self.assertEqual(memory.skills, [])

    def test_newer_skill_can_replace_old_rule(self) -> None:
        memory = SkillMemory()
        memory.add(Skill("style", "translate", "old", version=1))
        memory.add(Skill("style", "translate", "new", version=2))

        self.assertEqual(memory.skills[0].instruction, "new")


if __name__ == "__main__":
    unittest.main()
