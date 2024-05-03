from flask import request
from flask_socketio import emit, SocketIO

from soluzion_server.globals import *
from soluzion_server.soluzion_expanded import AdvancedOperator
from soluzion_server.soluzion_types import *


def serialize_state(state: AdvancedState):
    """
    Gets a serialized representation of the state, if to_dict is implemented
    :return: state dict, or None
    """

    # noinspection PyArgumentList
    if hasattr(state, "to_dict") and callable(state.to_dict):
        return state.to_dict()
    return None


def apply_operator(game: GameSession, op_no: int, args: list[Any] | None):
    """
    Applies the effects of an operator on the game, transforming the state
    """
    operator: AdvancedOperator = PROBLEM.OPERATORS[op_no]

    old_state = game.current_state
    new_state: AdvancedState
    if operator.params is None or args is None:
        new_state = operator.apply(old_state)
    else:
        new_state = operator.transf(old_state, args)

    game.state_stack.append(old_state)
    game.current_state = new_state


def is_operator_applicable(op: AdvancedOperator, state: AdvancedState, role: int | None):
    """
    Check if operator is applicable, working whether roles are defined or not
    """
    return op.is_applicable(state) if role is None else op.is_applicable(state, int(role))


def get_applicable_operators(state: AdvancedState, role: int | None) -> list[AdvancedOperator]:
    """
    Gets all applicable operators, possibly only for a specific role
    """
    return [op for op in PROBLEM.OPERATORS if is_operator_applicable(op, state, role)]


def operator_name(operator: AdvancedOperator, state: AdvancedState):
    """
    Gets the display name of an operator, supporting dynamic names
    """
    # noinspection PyArgumentList
    return operator.get_name(state) if hasattr(operator, "get_name") and callable(operator.get_name) else operator.name


def encode_operator(operator: AdvancedOperator, op_no: int, state: AdvancedState):
    """
    Encodes an Operator to its serialized type
    """
    return Operator(operator_name(operator, state),
                    op_no,
                    None if operator.params is None else [OperatorParam.from_dict(param) for param in operator.params])


def handle_state_updated(game: GameSession):
    """
    Process the effects that happen when the state is updated
    :param game:
    :return:
    """
    state = game.current_state
    room = game.room

    if state.is_goal():
        emit(ClientEvent.GAME_ENDED.value, {}, to=room)
        # TODO more game end handling
        return

    emit(ClientEvent.STATE_UPDATED.value, StateUpdated(f"{state}", serialize_state(state)).to_dict(), to=room)

    for sid, role in game.players.items():
        operators = get_applicable_operators(state, role)
        encoded_operators = [encode_operator(op, op_no, state) for op_no, op in enumerate(operators)]

        emit(ClientEvent.OPERATORS_AVAILABLE.value, OperatorsAvailable(encoded_operators).to_dict())


def configure_game_handlers(socketio: SocketIO):
    @socketio.on(ServerEvent.START_GAME.value)
    def start_game(data):
        room = current_room(request.sid)
        if room is None:
            emit(
                ClientEvent.ERROR.value,
                Error(ServerError.NOT_IN_A_ROOM, ServerEvent.START_GAME, None).to_dict(),
            )
            return

        if room.game is not None:
            emit(ClientEvent.ERROR.value, Error(ServerError.GAME_ALREADY_STARTED, ServerEvent.START_GAME, None).to_dict())

        # TODO check if roles correct

        roles = dict((player, connected_players[player].role) for player in room.player_sids)

        game = room.game = GameSession(PROBLEM.State(), [], room.owner_sid, room.id, roles)

        emit(ClientEvent.GAME_STARTED.value, {}, to=room.id)

        handle_state_updated(game)

    @socketio.on(ServerEvent.OPERATOR_CHOSEN.value)
    def operator_chosen(data):
        event = OperatorChosen.from_dict(data)

        player = current_player(request.sid)
        room = current_room(request.sid)
        game = current_game(request.sid)

        if room is None:
            emit(
                ClientEvent.ERROR.value,
                Error(ServerError.NOT_IN_A_ROOM, ServerEvent.OPERATOR_CHOSEN, None).to_dict(),
            )
            return
        if game is None:
            emit(
                ClientEvent.ERROR.value,
                Error(ServerError.GAME_NOT_STARTED, ServerEvent.OPERATOR_CHOSEN, None).to_dict(),
            )
            return
        if event.op_no < 0 or event.op_no >= len(PROBLEM.OPERATORS):
            emit(
                ClientEvent.ERROR.value,
                Error(ServerError.INVALID_OPERATOR, ServerEvent.OPERATOR_CHOSEN, "Out of Bounds").to_dict(),
            )
            return

        state = game.current_state
        operator: AdvancedOperator = PROBLEM.OPERATORS[int(event.op_no)]

        if not is_operator_applicable(operator, state, player.role):
            emit(
                ClientEvent.ERROR.value,
                Error(ServerError.INVALID_OPERATOR, ServerEvent.OPERATOR_CHOSEN, "Not applicable").to_dict(),
            )
            return

        apply_operator(game, int(event.op_no), event.params)

        handle_state_updated(game)
