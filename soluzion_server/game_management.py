from __future__ import annotations

from typing import Collection

from flask import request
from flask_socketio import emit, SocketIO

from soluzion_server.globals import *
from soluzion_server.soluzion_expanded import ExpandedOperator
from soluzion_server.soluzion_types import *
from soluzion_server.soluzion_types import OperatorElement


def serialize_state(state: ExpandedState) -> str | None:
    """
    Gets a serialized representation of the state, if .serialize is implemented
    :return: serialized string, or None
    """

    # noinspection PyArgumentList
    if hasattr(state, "serialize") and callable(state.serialize):
        return state.serialize()
    return None


def apply_operator(game: GameSession, op_no: int, args: Optional[list[Any]]):
    """
    Applies the effects of an operator on the game, transforming the state
    """
    operator: ExpandedOperator = PROBLEM.OPERATORS[op_no]

    old_state = game.current_state
    new_state: ExpandedState
    if operator.params is None or args is None:
        new_state = operator.apply(old_state)
    else:  # TODO make this distinction more clear
        new_state = operator.transf(old_state, args)

    game.state_stack.append(old_state)
    game.current_state = new_state
    game.depth += 1
    game.step += 1

    handle_transitions(old_state, new_state, operator, game.room)

    emit(
        ServerToClient.OPERATOR_APPLIED.value,
        OperatorApplied(
            f"{new_state}",
            OperatorAppliedOperator(operator_name(operator, old_state), op_no, args),
            serialize_state(new_state),
        ).to_dict(),
        to=game.room,
    )

    if new_state.is_goal():
        emit(
            ServerToClient.GAME_ENDED.value,
            GameEnded(new_state.goal_message()).to_dict(),
            to=game.room,
        )

        # TODO end game session

    else:
        send_operators_available(game)


def handle_transitions(
    old_state: ExpandedState,
    new_state: ExpandedState,
    operator: ExpandedOperator,
    room: str,
):
    """
    Handles clients that have defined Transition Messages
    """
    if not hasattr(PROBLEM, "TRANSITIONS") or PROBLEM.TRANSITIONS is None:
        return

    for condition, action in PROBLEM.TRANSITIONS:
        if condition(old_state, new_state, operator):
            text: str
            if callable(action):
                text = action(old_state, new_state, operator)
            else:
                text = str(action)
            emit(ServerToClient.TRANSITION.value, Transition(text).to_dict(), to=room)

        # TODO document this as not default behavior, normally only 1 transition happens
        # break


def validate_roles(room: RoomSession):
    """
    Verifies whether the role assignments for the current players in the room are valid for the problem
    :return: None if roles are valid, or a string error reason why they're invalid
    """

    if not hasattr(PROBLEM, "ROLES") or PROBLEM.ROLES is None:
        return None

    # List of all player roles
    player_roles = [
        role for sid in room.player_sids for role in connected_players[sid].roles
    ]

    for i, ROLE in enumerate(PROBLEM.ROLES):
        role = Role.from_dict(ROLE)
        count = player_roles.count(i)
        if role.min is not None and count < role.min:
            return f"Not enough players for role {role.name}"
        if role.max is not None and count > role.max:
            return f"Too many players for role {role.name}"

    return None


def is_operator_applicable(
    op: ExpandedOperator, state: ExpandedState, roles: Collection[int] | None
):
    """
    Check if operator is applicable, working whether roles are defined or not
    """
    if roles is None or len(roles) == 0:
        return op.is_applicable(state)

    for role in roles:
        if op.is_applicable(state, role):
            return True

    return False


def get_applicable_operators(
    state: ExpandedState, roles: Collection[int] | None
) -> list[ExpandedOperator]:
    """
    Gets all applicable operators, possibly only for a specific role
    """
    return [op for op in PROBLEM.OPERATORS if is_operator_applicable(op, state, roles)]


def operator_name(operator: ExpandedOperator, state: ExpandedState):
    """
    Gets the display name of an operator, supporting dynamic names
    """
    # noinspection PyArgumentList
    return (
        operator.get_name(state)
        if hasattr(operator, "get_name") and callable(operator.get_name)
        else operator.name
    )


def send_operators_available(game: GameSession):
    """
    Sends each player the operators that are available to them. If roles and turns are implemented,
    this may send empty arrays if it's not a player's turn
    """
    state = game.current_state
    for sid, roles in game.players.items():
        operators = get_applicable_operators(state, roles)
        emit(
            ServerToClient.OPERATORS_AVAILABLE.value,
            OperatorsAvailable(
                [
                    OperatorElement(
                        operator_name(op, state),
                        PROBLEM.OPERATORS.index(op),
                        [Param.from_dict(param) for param in (op.params or [])],
                    )
                    for op in operators
                ]
            ).to_dict(),
            to=sid,
        )


def configure_game_handlers(socketio: SocketIO):
    """
    Add the handlers for processing game events
    """

    @socketio.on(ClientToServer.START_GAME.value)
    def start_game(data):
        room = current_room(request.sid)
        if room is None:
            return error_response(ServerError.NOT_IN_A_ROOM)

        if room.game is not None:
            return error_response(ServerError.GAME_ALREADY_STARTED)

        roles_error = validate_roles(room)
        if roles_error is not None:
            return error_response(ServerError.INVALID_ROLES, roles_error)

        roles = dict(
            (player, connected_players[player].roles) for player in room.player_sids
        )

        state = (
            PROBLEM.INITIAL_STATE
            if hasattr(PROBLEM, "INITIAL_STATE") and PROBLEM.INITIAL_STATE is not None
            else PROBLEM.State()
        )

        # Start the game session

        game = room.game = GameSession(state, [], room.owner_sid, room.id, roles)

        emit(
            ServerToClient.GAME_STARTED.value,
            GameStarted(f"{state}", serialize_state(state)).to_dict(),
            to=room.id,
        )
        emit(ServerToClient.ROOM_CHANGED.value, room.to_dict(), broadcast=True)

        send_operators_available(game)

    @socketio.on(ClientToServer.OPERATOR_CHOSEN.value)
    def operator_chosen(data):
        event = OperatorChosen.from_dict(data)

        player = current_player(request.sid)
        room = current_room(request.sid)
        game = current_game(request.sid)

        if room is None:
            return error_response(ServerError.NOT_IN_A_ROOM)
        if game is None:
            return error_response(ServerError.GAME_NOT_STARTED)
        if event.op_no < 0 or event.op_no >= len(PROBLEM.OPERATORS):
            return error_response(ServerError.INVALID_OPERATOR, "Out of Bounds")

        state = game.current_state
        operator: ExpandedOperator = PROBLEM.OPERATORS[int(event.op_no)]

        if not is_operator_applicable(operator, state, player.roles):
            return error_response(ServerError.INVALID_OPERATOR, "Not Applicable")

        apply_operator(game, int(event.op_no), event.params)
