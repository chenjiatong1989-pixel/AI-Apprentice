"""Small offline primitives for an AI apprentice learning loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


@dataclass(frozen=True)
class Skill:
    """A reusable lesson extracted from a teacher response."""

    name: str
    trigger: str
    instruction: str

    def matches(self, task: str) -> bool:
        return self.trigger.lower() in task.lower()


@dataclass
class SkillMemory:
    """In-memory skill store used by the first prototype."""

    skills: list[Skill] = field(default_factory=list)

    def add(self, skill: Skill) -> None:
        if skill.name not in {existing.name for existing in self.skills}:
            self.skills.append(skill)

    def find(self, task: str) -> list[Skill]:
        return [skill for skill in self.skills if skill.matches(task)]


@dataclass(frozen=True)
class Teacher:
    """A simple teacher adapter.

    Future adapters can wrap local models, API models, documents, browser
    sessions, or human feedback. The first version stays offline.
    """

    name: str
    teach: Callable[[str], str]


@dataclass
class Apprentice:
    """Runs a minimal try, learn, remember, retry loop."""

    memory: SkillMemory
    teachers: Iterable[Teacher]

    def solve(self, task: str) -> str:
        known_skills = self.memory.find(task)
        if known_skills:
            return self._apply_skill(task, known_skills[0])

        teacher = next(iter(self.teachers), None)
        if teacher is None:
            return f"I tried the task, but I do not have a teacher yet: {task}"

        lesson = teacher.teach(task)
        skill = self._extract_skill(task, lesson, teacher.name)
        self.memory.add(skill)
        return self._apply_skill(task, skill)

    def _extract_skill(self, task: str, lesson: str, teacher_name: str) -> Skill:
        trigger = "translate" if "translate" in task.lower() else task.split()[0]
        return Skill(
            name=f"{teacher_name}:{trigger}:style",
            trigger=trigger,
            instruction=lesson,
        )

    def _apply_skill(self, task: str, skill: Skill) -> str:
        return f"Using skill '{skill.name}': {skill.instruction}\nTask: {task}"
