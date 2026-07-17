import unittest

from ai_apprentice import (
    Apprentice,
    AssumptionChallenger,
    ExperienceRecord,
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

    def test_handles_missing_teacher(self) -> None:
        apprentice = Apprentice(memory=SkillMemory(), teachers=[])
        self.assertIn("do not have a teacher yet", apprentice.solve("Summarize this document"))

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
        self.assertIn("rejected skill", apprentice.solve("Translate a slogan"))
        self.assertEqual(memory.skills, [])

    def test_newer_skill_can_replace_old_rule(self) -> None:
        memory = SkillMemory()
        memory.add(Skill("style", "translate", "old", version=1))
        memory.add(Skill("style", "translate", "new", version=2))
        self.assertEqual(memory.skills[0].instruction, "new")

    def test_plan_uses_multiple_perspectives_and_reverse_thinking(self) -> None:
        apprentice = Apprentice(SkillMemory(), [])
        plan = apprentice.plan(
            "Build a monitoring plugin",
            goal="Know whether an AI task really succeeded",
            parts=("collect evidence", "judge outcome"),
            assumptions=("more logs create more trust",),
        )

        self.assertEqual(len(plan.views), 8)
        self.assertIn("opposite", {view.name for view in plan.views})
        self.assertEqual(plan.frame.parts, ("collect evidence", "judge outcome"))
        self.assertIn("forbidden", plan.frame.inversions[1])
        self.assertIn("Define evidence", plan.frame.backsolved_steps[0])

    def test_failed_prediction_becomes_memory(self) -> None:
        memory = SkillMemory([Skill("style", "translate", "Be literal", confidence=0.6)])
        apprentice = Apprentice(memory, [])
        updated = apprentice.learn_from_reality(
            "style",
            ExperienceRecord(
                task="Translate a slogan",
                prediction="Literal translation will sound natural",
                actual_outcome="Native readers found it awkward",
                evidence=("review: three native readers",),
                matched=False,
                lesson="Preserve intent before wording",
                counterexamples=("Marketing slogans need rhythm",),
            ),
        )

        self.assertAlmostEqual(updated.confidence, 0.4)
        self.assertEqual(updated.version, 2)
        self.assertIn("Preserve intent", updated.failures[0])
        self.assertEqual(len(memory.experiences), 1)

    def test_successful_evidence_raises_confidence(self) -> None:
        memory = SkillMemory([Skill("style", "translate", "Be concise", confidence=0.5)])
        apprentice = Apprentice(memory, [])
        updated = apprentice.learn_from_reality(
            "style",
            ExperienceRecord(
                task="Translate a slogan",
                prediction="Readers will preserve the intended meaning",
                actual_outcome="Readers preserved the intended meaning",
                evidence=("blind review passed",),
                matched=True,
            ),
        )
        self.assertAlmostEqual(updated.confidence, 0.6)
        self.assertIn("blind review passed", updated.evidence)

    def test_no_evidence_does_not_fake_growth(self) -> None:
        memory = SkillMemory([Skill("style", "translate", "Be concise", confidence=0.5)])
        apprentice = Apprentice(memory, [])
        updated = apprentice.learn_from_reality(
            "style",
            ExperienceRecord(
                task="Translate a slogan",
                prediction="It works",
                actual_outcome="It seems fine",
                matched=True,
            ),
        )
        self.assertEqual(updated.confidence, 0.5)
        self.assertEqual(updated.version, 1)

    def test_repeated_failure_quarantines_skill(self) -> None:
        memory = SkillMemory([Skill("style", "translate", "Be literal", confidence=0.3)])
        apprentice = Apprentice(memory, [])
        updated = apprentice.learn_from_reality(
            "style",
            ExperienceRecord("task", "works", "failed", ("test failed",), False),
        )
        self.assertEqual(updated.status, "quarantined")
        self.assertEqual(memory.find("translate this"), [])


if __name__ == "__main__":
    unittest.main()
