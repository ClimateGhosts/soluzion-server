import json
from typing import Optional, Any, Callable

from soluzion_server.soluzion import Basic_Operator, Basic_State


class ExpandedState(Basic_State):

    def __init__(self, old=None):
        super().__init__(old)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def goal_message(self):
        return ""

    def to_json(self):
        """
        Serializes the state into a json formatted string
        :return:
        """
        try:
            return json.dumps(self)
        except Exception:
            return "{}"


class ExpandedOperator(Basic_Operator):
    params: list[dict[str, Any]]

    def __init__(
        self,
        name,
        precond=(lambda s: True),
        transf=(lambda s: Basic_State(s)),
        params=None,
    ):
        if params is None:
            params = []
        super().__init__(name, precond, transf, params)

    def get_name(self, state: ExpandedState) -> str:
        return self.name


class Problem:
    OPERATORS: list[ExpandedOperator]
    INITIAL_STATE: Optional[ExpandedState]
    ROLES: list[dict[str, Any]]
    TRANSITIONS: list[
        tuple[
            Callable[[ExpandedState, ExpandedState, ExpandedOperator], bool],
            (str | Callable[[ExpandedState, ExpandedState, ExpandedOperator], str]),
        ]
    ]

    # noinspection PyPep8Naming
    def State(self) -> ExpandedState:
        pass

    def GET_ARGS(self, op: ExpandedOperator) -> dict[str, dict[str, Any]]:
        pass
