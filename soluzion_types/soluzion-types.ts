/**
 * Primary copy of Soluzion Types; used to generate others for Python, C# etc.
 */

/**
 * Events handled and sent by both client and server
 */
type SharedEvent = "connect" | "disconnect";

/**
 * Events handled by the server (sent by the client)
 */
type ServerEvent = keyof ServerEvents;
type ServerEvents = {
  create_room: {
    room: string;
  };
  join_room: {
    room: string;
    username: string;
    role: number | null; // TODO separate role choice
  };
  leave_room: never;
  start_game: never;
  operator_chosen: {
    op_no: number;
    params: any[] | null;
  };
};

/**
 * Events handled by the client (sent by the server)
 */
type ClientEvent = keyof ClientEvents;
type ClientEvents = {
  room_created: {
    room: string;
  };
  room_joined: {
    username: string;
  };
  room_left: {
    username: string;
  };
  game_started: never;
  game_ended: never;
  state_updated: {
    state: object | null;
    message: string;
  };
  operators_available: {
    operators: {
      name: string;
      op_no: number;
      params: OperatorParam[] | null;
    }[];
  };
  error: {
    event: ServerEvent;
    error: ServerError;
    message: string | null;
  };
};

type OperatorParam = {
  name: string;
  type: "int" | "float" | "str";
  min: number | null;
  max: number | null;
};

type ServerError =
  | "RoomAlreadyExists"
  | "NotInARoom"
  | "CantJoinRoom"
  | "GameAlreadyStarted"
  | "GameNotStarted"
  | "InvalidOperator";
