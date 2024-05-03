import json
from typing import Optional, Any

from soluzion_server.soluzion import Basic_Operator, Basic_State


class AdvancedState(Basic_State):

    def __init__(self, old=None):
        super().__init__(old)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_dict(self):
        return json.dumps(self)


type OperatorParam = dict[str, Any]


class AdvancedOperator(Basic_Operator):
    params: list[OperatorParam]

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

    def get_name(self, state: AdvancedState) -> str:
        return self.name


class Problem:
    OPERATORS: list[AdvancedOperator]
    INITIAL_STATE: Optional[AdvancedState]
    ROLES: list[dict[str, Any]]

    # noinspection PyPep8Naming
    def State(self) -> AdvancedState:
        pass

    def GET_ARGS(self, op: AdvancedOperator) -> dict[str, OperatorParam]:
        pass
