__all__ = [
    'RuleType',
    'RuleAction',
    'Restriction',
    'RestrictionV2',
    'SetSkillFromOutputField',
    'ChangeOverlap',
    'SetSkill',
    'RejectAllAssignments',
    'ApproveAllAssignments',
]
import toloka.client.conditions
import toloka.client.primitives.base
import toloka.client.user_restriction
import toloka.util._extendable_enum
import typing


class RuleType(toloka.util._extendable_enum.ExtendableStrEnum):
    """An enumeration.
    """

    RESTRICTION = 'RESTRICTION'
    RESTRICTION_V2 = 'RESTRICTION_V2'
    SET_SKILL_FROM_OUTPUT_FIELD = 'SET_SKILL_FROM_OUTPUT_FIELD'
    CHANGE_OVERLAP = 'CHANGE_OVERLAP'
    SET_SKILL = 'SET_SKILL'
    REJECT_ALL_ASSIGNMENTS = 'REJECT_ALL_ASSIGNMENTS'
    APPROVE_ALL_ASSIGNMENTS = 'APPROVE_ALL_ASSIGNMENTS'


class RuleAction(toloka.client.primitives.base.BaseParameters):
    """Base class for all actions in quality controls configurations
    """

    def __init__(self, *, parameters: typing.Optional[toloka.client.primitives.base.BaseParameters.Parameters] = None) -> None:
        """Method generated by attrs for class RuleAction.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[toloka.client.primitives.base.BaseParameters.Parameters]


class Restriction(RuleAction):
    """Restricts Toloker's access to projects or pools.

    To have better control over restriction period use [RestrictionV2](toloka.client.actions.RestrictionV2.md).

    Attributes:
        parameters.scope:
            * `POOL` — A Toloker can't access the pool if the action is applied.
            * `PROJECT` — A Toloker can't access the entire project containing the pool.
            * `ALL_PROJECTS` — A Toloker can't access any requester's project.
        parameters.duration_days: A blocking period in days. If the `duration_days` is omitted, then the block is permanent.
        parameters.private_comment: A private comment. It is visible only to the requester.
    """

    class Parameters(toloka.client.primitives.base.BaseParameters.Parameters):
        def __init__(
            self,
            *,
            scope: typing.Union[toloka.client.user_restriction.UserRestriction.Scope, str, None] = None,
            duration_days: typing.Optional[int] = None,
            private_comment: typing.Optional[str] = None
        ) -> None:
            """Method generated by attrs for class Restriction.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        scope: typing.Optional[toloka.client.user_restriction.UserRestriction.Scope]
        duration_days: typing.Optional[int]
        private_comment: typing.Optional[str]

    @typing.overload
    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class Restriction.
        """
        ...

    @typing.overload
    def __init__(
        self,
        *,
        scope: typing.Union[toloka.client.user_restriction.UserRestriction.Scope, str, None] = None,
        duration_days: typing.Optional[int] = None,
        private_comment: typing.Optional[str] = None
    ) -> None:
        """Method generated by attrs for class Restriction.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]


class RestrictionV2(RuleAction):
    """Restricts Toloker's access to projects or pools.

    Attributes:
        parameters.scope:
            * `POOL` — A Toloker can't access the pool if the action is applied.
            * `PROJECT` — A Toloker can't access the entire project containing the pool.
            * `ALL_PROJECTS` — A Toloker can't access any requester's project.
        parameters.duration: The duration of the blocking period measured in `duration_unit`.
        parameters.duration_unit:
            * `MINUTES`;
            * `HOURS`;
            * `DAYS`;
            * `PERMANENT` — blocking is permanent. In this case the `duration` is ignored and may be omitted.
        parameters.private_comment: A private comment. It is visible only to the requester.

    Example:
        The following quality control rule blocks access to the project for 10 days, if a Toloker answers too fast.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
        >>>     conditions=[toloka.conditions.FastSubmittedCount > 1],
        >>>     action=toloka.actions.RestrictionV2(
        >>>         scope='PROJECT',
        >>>         duration=10,
        >>>         duration_unit='DAYS',
        >>>         private_comment='Fast responses',
        >>>     )
        >>> )
        ...
    """

    class Parameters(toloka.client.primitives.base.BaseParameters.Parameters):
        def __init__(
            self,
            *,
            scope: typing.Union[toloka.client.user_restriction.UserRestriction.Scope, str, None] = None,
            duration: typing.Optional[int] = None,
            duration_unit: typing.Union[toloka.client.user_restriction.DurationUnit, str, None] = None,
            private_comment: typing.Optional[str] = None
        ) -> None:
            """Method generated by attrs for class RestrictionV2.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        scope: typing.Optional[toloka.client.user_restriction.UserRestriction.Scope]
        duration: typing.Optional[int]
        duration_unit: typing.Optional[toloka.client.user_restriction.DurationUnit]
        private_comment: typing.Optional[str]

    @typing.overload
    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class RestrictionV2.
        """
        ...

    @typing.overload
    def __init__(
        self,
        *,
        scope: typing.Union[toloka.client.user_restriction.UserRestriction.Scope, str, None] = None,
        duration: typing.Optional[int] = None,
        duration_unit: typing.Union[toloka.client.user_restriction.DurationUnit, str, None] = None,
        private_comment: typing.Optional[str] = None
    ) -> None:
        """Method generated by attrs for class RestrictionV2.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]


class SetSkillFromOutputField(RuleAction):
    """Sets Toloker's skill value to the percentage of correct or incorrect answers.

    You can use this action with [MajorityVote](toloka.client.collectors.MajorityVote.md) and [GoldenSet](toloka.client.collectors.GoldenSet.md) collectors.

    Attributes:
        parameters.skill_id: The ID of the skill to update.
        parameters.from_field: The value to assign to the skill:
            * `correct_answers_rate` — Percentage of correct answers.
            * `incorrect_answers_rate` — Percentage of incorrect answers.

    Example:
        In the following example, a `MajorityVote` collector is used to update a skill value.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.MajorityVote(answer_threshold=2, history_size=10),
        >>>     conditions=[
        >>>         toloka.conditions.TotalAnswersCount > 2,
        >>>     ],
        >>>     action=toloka.actions.SetSkillFromOutputField(
        >>>         skill_id=some_skill_id,
        >>>         from_field='correct_answers_rate',
        >>>     ),
        >>> )
        ...
    """

    class Parameters(toloka.client.primitives.base.BaseParameters.Parameters):
        def __init__(
            self,
            *,
            skill_id: typing.Optional[str] = None,
            from_field: typing.Union[toloka.client.conditions.RuleConditionKey, str, None] = None
        ) -> None:
            """Method generated by attrs for class SetSkillFromOutputField.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        skill_id: typing.Optional[str]
        from_field: typing.Optional[toloka.client.conditions.RuleConditionKey]

    @typing.overload
    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class SetSkillFromOutputField.
        """
        ...

    @typing.overload
    def __init__(
        self,
        *,
        skill_id: typing.Optional[str] = None,
        from_field: typing.Union[toloka.client.conditions.RuleConditionKey, str, None] = None
    ) -> None:
        """Method generated by attrs for class SetSkillFromOutputField.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]


class ChangeOverlap(RuleAction):
    """Increases the overlap of a task.

    You can use this rule only with [UsersAssessment](toloka.client.collectors.UsersAssessment) and [AssignmentsAssessment](toloka.client.collectors.AssignmentsAssessment) collectors.

    Attributes:
        parameters.delta: An overlap increment.
        parameters.open_pool:
            * `True` — Open the pool after changing the overlap value.
            * `False` — Don't reopen the pool if it is closed.

    Example:
        The example shows how to increase task overlap when you reject assignments.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentsAssessment(),
        >>>     conditions=[toloka.conditions.AssessmentEvent == toloka.conditions.AssessmentEvent.REJECT],
        >>>     action=toloka.actions.ChangeOverlap(delta=1, open_pool=True),
        >>> )
        ...
    """

    class Parameters(toloka.client.primitives.base.BaseParameters.Parameters):
        def __init__(
            self,
            *,
            delta: typing.Optional[int] = None,
            open_pool: typing.Optional[bool] = None
        ) -> None:
            """Method generated by attrs for class ChangeOverlap.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        delta: typing.Optional[int]
        open_pool: typing.Optional[bool]

    @typing.overload
    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class ChangeOverlap.
        """
        ...

    @typing.overload
    def __init__(
        self,
        *,
        delta: typing.Optional[int] = None,
        open_pool: typing.Optional[bool] = None
    ) -> None:
        """Method generated by attrs for class ChangeOverlap.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]


class SetSkill(RuleAction):
    """Sets Toloker's skill value.

    Attributes:
        parameters.skill_id: The ID of the skill.
        parameters.skill_value: The new value of the skill.

    Example:
        When an answer is accepted, the Toloker gets a skill. Later you can filter Tolokers by that skill.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AnswerCount(),
        >>>     conditions=[toloka.conditions.AssignmentsAcceptedCount > 0],
        >>>     action=toloka.actions.SetSkill(skill_id=some_skill_id, skill_value=1),
        >>> )
        ...
    """

    class Parameters(toloka.client.primitives.base.BaseParameters.Parameters):
        def __init__(
            self,
            *,
            skill_id: typing.Optional[str] = None,
            skill_value: typing.Optional[int] = None
        ) -> None:
            """Method generated by attrs for class SetSkill.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        skill_id: typing.Optional[str]
        skill_value: typing.Optional[int]

    @typing.overload
    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class SetSkill.
        """
        ...

    @typing.overload
    def __init__(
        self,
        *,
        skill_id: typing.Optional[str] = None,
        skill_value: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class SetSkill.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]


class RejectAllAssignments(RuleAction):
    """Rejects all Toloker's assignments in the pool. This action is available for pools with non-automatic acceptance.

    Attributes:
        parameters.public_comment: The reason of the rejection. It is visible both to the requester and to the Toloker.

    Example:
        Reject all assignments if a Toloker sends responses too fast. Note, that the pool must be configured with non-automatic response acceptance.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
        >>>     conditions=[toloka.conditions.FastSubmittedCount > 3],
        >>>     action=toloka.actions.RejectAllAssignments(public_comment='Too fast responses.')
        >>> )
        ...
    """

    class Parameters(toloka.client.primitives.base.BaseParameters.Parameters):
        def __init__(self, *, public_comment: typing.Optional[str] = None) -> None:
            """Method generated by attrs for class RejectAllAssignments.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        public_comment: typing.Optional[str]

    @typing.overload
    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class RejectAllAssignments.
        """
        ...

    @typing.overload
    def __init__(self, *, public_comment: typing.Optional[str] = None) -> None:
        """Method generated by attrs for class RejectAllAssignments.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]


class ApproveAllAssignments(RuleAction):
    """Accepts all Toloker's assignments in the pool.

    Example:
        Accept all assignments if a Toloker gives correct responses for control tasks. Note, that the pool must be configured with non-automatic response acceptance.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.GoldenSet(history_size=5),
        >>>     conditions=[toloka.conditions.GoldenSetCorrectAnswersRate > 90],
        >>>     action=toloka.actions.ApproveAllAssignments()
        >>> )
        ...
    """

    def __init__(self, *, parameters: typing.Optional[toloka.client.primitives.base.BaseParameters.Parameters] = None) -> None:
        """Method generated by attrs for class ApproveAllAssignments.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[toloka.client.primitives.base.BaseParameters.Parameters]
