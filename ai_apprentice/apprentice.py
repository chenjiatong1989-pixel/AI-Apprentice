"""Small offline primitives for an AI apprentice learning loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


@dataclass(frozen=True)
class Skill:
    """A reusable, replaceable lesson extracted from a teacher response."""

    name: str
    trigger: str
    instruction: str
    source: str = "unknown"
    confidence: float = 0.5
    evidence: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()
    version: int = 1

    def matches(self, task: str) -> bool:
        return self.trigger.lower() in task.lower()


@dataclass
class SkillMemory:
    """In-memory skill store used by the first prototype."""

    skills: list[Skill] = field(default_factory=list)

    def add(self, skill: Skill) -> None:
        for index, existing in enumerate(self.skills):
            if existing.name == skill.name:
                if skill.version >= existing.version:
                    self.skills[index] = skill
                return
        self.skills.append(skill)

    def find(self, task: str) -> list[Skill]:
        return [skill for skill in self.skills if skill.matches(task)]


@dataclass(frozen=True)
class Teacher:
    """A teacher adapter for a model, document, tool, or human."""

    name: str
    teach: Callable[[str], str]


@dataclass(frozen=True)
class AssumptionChallenger:
    """Reframes a task before the apprentice commits to the obvious route."""

    name: str
    reframe: Callable[[str], str]


@dataclass(frozen=True)
class Verifier:
    """Tries to reject a proposed skill before it enters memory."""

    name: str
    verify: Callable[[str, Skill], bool]


@dataclass
class Apprentice:
    """Runs a question, try, learn, challenge, remember, retry loop."""

    memory: SkillMemory
    teachers: Iterable[Teacher]
    challenger: AssumptionChallenger | None = None
    verifier: Verifier | None = None

    def solve(self, task: str) -> str:
        working_task = self._question_assumptions(task)
        known_skills = self.memory.find(working_task)
        if known_skills:
            return self._apply_skill(task, working_task, known_skills[0])

        teacher = next(iter(self.teachers), None)
        if teacher is None:
            return f"I tried the task, but I do not have a teacher yet: {task}"

        lesson = teacher.teach(working_task)
        skill = self._extract_skill(working_task, lesson, teacher.name)

        if self.verifier and not self.verifier.verify(working_task, skill):
            return (
                f"Verifier '{self.verifier.name}' rejected skill "
                f"'{skill.name}'. It was not stored."
            )

        self.memory.add(skill)
        return self._apply_skill(task, working_task, skill)

    def _question_assumptions(self, task: str) -> str:
        if self.challenger is None:
            return task
        reframed = self.challenger.reframe(task).strip()
        return reframed or task

    def _extract_skill(self, task: str, lesson: str, teacher_name: str) -> Skill:
        trigger = "translate" if "translate" in task.lower() else task.split()[0]
        return Skill(
            name=f"{teacher_name}:{trigger}:style",
            trigger=trigger,
            instruction=lesson,
            source=teacher_name,
            evidence=(f"Teacher lesson for: {task}",),
        )

    def _apply_skill(self, original_task: str, working_task: str, skill: Skill) -> str:
        assumption_note = ""
        if working_task != original_task:
            assumption_note = f"Reframed task: {working_task}\n"
        return (
            f"{assumption_note}Using skill '{skill.name}': {skill.instruction}\n"
            f"Task: {original_task}"
        )
