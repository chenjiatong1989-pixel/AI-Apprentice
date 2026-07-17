"""Small offline primitives for an evidence-driven AI apprentice."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Iterable


@dataclass(frozen=True)
class Skill:
    """A reusable, replaceable lesson rather than a permanent truth."""

    name: str
    trigger: str
    instruction: str
    source: str = "unknown"
    confidence: float = 0.5
    evidence: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()
    version: int = 1
    status: str = "active"

    def matches(self, task: str) -> bool:
        return self.status == "active" and self.trigger.lower() in task.lower()


@dataclass(frozen=True)
class ExperienceRecord:
    """The difference between what was expected and what reality showed."""

    task: str
    prediction: str
    actual_outcome: str
    evidence: tuple[str, ...] = ()
    matched: bool | None = None
    lesson: str = ""
    applicable_when: str = ""
    counterexamples: tuple[str, ...] = ()

    @property
    def delta(self) -> str:
        if self.matched is True:
            return "prediction confirmed"
        if self.matched is False:
            return f"expected: {self.prediction}; observed: {self.actual_outcome}"
        return "unknown: no verified comparison"


@dataclass
class SkillMemory:
    """Local prototype memory for skills and the experiences behind them."""

    skills: list[Skill] = field(default_factory=list)
    experiences: list[ExperienceRecord] = field(default_factory=list)

    def add(self, skill: Skill) -> None:
        for index, existing in enumerate(self.skills):
            if existing.name == skill.name:
                if skill.version >= existing.version:
                    self.skills[index] = skill
                return
        self.skills.append(skill)

    def find(self, task: str) -> list[Skill]:
        return [skill for skill in self.skills if skill.matches(task)]

    def get(self, name: str) -> Skill | None:
        return next((skill for skill in self.skills if skill.name == name), None)


@dataclass(frozen=True)
class Perspective:
    """One useful viewpoint and the question it asks."""

    name: str
    question: str


DEFAULT_PERSPECTIVES = (
    Perspective("user", "What outcome does the user actually need?"),
    Perspective("executor", "What is the shortest safe action that can work?"),
    Perspective("system", "Which constraints and dependencies shape the result?"),
    Perspective("designer", "Can the problem be reframed or removed?"),
    Perspective("opposite", "What if the obvious assumption is backwards?"),
    Perspective("attacker", "How could this fail, mislead, or be abused?"),
    Perspective("future", "What will this decision teach or cost next time?"),
    Perspective("outsider", "What would a person without our assumptions notice?"),
)


@dataclass(frozen=True)
class PerspectiveView:
    name: str
    question: str
    task: str


@dataclass(frozen=True)
class PerspectiveEngine:
    """Makes blind spots visible; it does not pretend to answer the questions."""

    perspectives: tuple[Perspective, ...] = DEFAULT_PERSPECTIVES

    def inspect(self, task: str) -> tuple[PerspectiveView, ...]:
        return tuple(PerspectiveView(item.name, item.question, task) for item in self.perspectives)


@dataclass(frozen=True)
class ProblemFrame:
    """An inspectable result of decomposing and reversing a problem."""

    original_task: str
    goal: str
    parts: tuple[str, ...]
    assumptions: tuple[str, ...]
    constraints: tuple[str, ...]
    inversions: tuple[str, ...]
    recombinations: tuple[str, ...]
    backsolved_steps: tuple[str, ...]


@dataclass(frozen=True)
class ProblemTransformer:
    """Turns reverse thinking into explicit prompts and verifiable next steps."""

    def transform(
        self,
        task: str,
        *,
        goal: str | None = None,
        parts: Iterable[str] = (),
        assumptions: Iterable[str] = (),
        constraints: Iterable[str] = (),
        recombinations: Iterable[str] = (),
    ) -> ProblemFrame:
        real_goal = (goal or task).strip()
        pieces = tuple(parts) or (real_goal,)
        return ProblemFrame(
            original_task=task,
            goal=real_goal,
            parts=pieces,
            assumptions=tuple(assumptions),
            constraints=tuple(constraints),
            inversions=(
                f"What would guarantee failure: {real_goal}?",
                "What remains possible if the assumed route is forbidden?",
            ),
            recombinations=tuple(recombinations) or pieces,
            backsolved_steps=(
                f"Define evidence that would prove: {real_goal}",
                "Choose the shortest safe action that can produce that evidence.",
                "Act, observe reality, and compare it with the prediction.",
            ),
        )


@dataclass(frozen=True)
class LearningPlan:
    views: tuple[PerspectiveView, ...]
    frame: ProblemFrame


@dataclass(frozen=True)
class MemoryUpdater:
    """Updates confidence only when reality provides evidence."""

    success_step: float = 0.1
    failure_step: float = 0.2
    quarantine_below: float = 0.2

    def update(self, skill: Skill, experience: ExperienceRecord) -> Skill:
        if not experience.evidence or experience.matched is None:
            return skill

        if experience.matched:
            confidence = round(min(1.0, skill.confidence + self.success_step), 10)
            evidence = tuple(dict.fromkeys((*skill.evidence, *experience.evidence)))
            failures = skill.failures
        else:
            confidence = round(max(0.0, skill.confidence - self.failure_step), 10)
            evidence = skill.evidence
            failure = experience.delta
            if experience.lesson:
                failure = f"{failure}; lesson: {experience.lesson}"
            failures = (*skill.failures, failure, *experience.counterexamples)

        status = "quarantined" if confidence < self.quarantine_below else "active"
        return replace(
            skill,
            confidence=confidence,
            evidence=evidence,
            failures=failures,
            version=skill.version + 1,
            status=status,
        )


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
    """Runs a perspective, transform, act, verify, remember loop."""

    memory: SkillMemory
    teachers: Iterable[Teacher]
    challenger: AssumptionChallenger | None = None
    verifier: Verifier | None = None
    perspective_engine: PerspectiveEngine = field(default_factory=PerspectiveEngine)
    transformer: ProblemTransformer = field(default_factory=ProblemTransformer)
    memory_updater: MemoryUpdater = field(default_factory=MemoryUpdater)

    def plan(self, task: str, **frame_inputs: object) -> LearningPlan:
        working_task = self._question_assumptions(task)
        frame = self.transformer.transform(working_task, **frame_inputs)
        return LearningPlan(self.perspective_engine.inspect(working_task), frame)

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

    def learn_from_reality(self, skill_name: str, experience: ExperienceRecord) -> Skill:
        skill = self.memory.get(skill_name)
        if skill is None:
            raise KeyError(f"Unknown skill: {skill_name}")
        self.memory.experiences.append(experience)
        updated = self.memory_updater.update(skill, experience)
        self.memory.add(updated)
        return updated

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
