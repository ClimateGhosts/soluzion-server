"""solution4a.py
 (EXPERIMENTAL VERSION OF soluzion.py that will
support operators with integer parameters.)
Jan. 20, 2024

soluzion.py
This file provides base classes for states and
operators.
This serves as part of the SOLUTION version 4
system of problem representation.

S.T., Nov. 1, 2023.
"""


class Basic_State:
    Initial_State = None

    def __init__(self, old=None):
        if old == None:
            self.desc = "initial State"
            # Save the initial state for possible use
            # in reporting, analytics, etc.
            Basic_State.Initial_State = self
        else:
            self.desc = "another state"
            # Normally, a subclass should do a deep copy here.

    def __str__(self):
        return self.desc

    def __eq__(self, other):
        if self.desc != other.desc:
            return False
        return True

    def __hash__(self):
        return str(self).__hash__()

    def is_goal(self):
        return False


class Invalid_State_Exception(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Invalid state because: " + self.msg


class Basic_Operator:
    def __init__(
        self,
        name,
        precond=(lambda s: True),
        transf=(lambda s: Basic_State(s)),
        params=[],
    ):
        self.name = name
        self.precond = precond
        self.transf = transf
        self.params = params

    def is_applicable(self, s, role_number=0):
        return self.precond(s)

    def apply(self, s):
        if self.params:
            args = GET_ARGS(self)
            return self.transf(s, args)
        else:
            return self.transf(s)


def GET_ARGS(op):
    pass  # The client will implement and overwrite this.
