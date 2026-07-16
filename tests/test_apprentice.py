import unittest

from ai_apprentice import Apprentice, SkillMemory, Teacher


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

    def test_handles_missing_teacher(self) -> None:
        apprentice = Apprentice(memory=SkillMemory(), teachers=[])

        result = apprentice.solve("Summarize this document")

        self.assertIn("do not have a teacher yet", result)


if __name__ == "__main__":
    unittest.main()
