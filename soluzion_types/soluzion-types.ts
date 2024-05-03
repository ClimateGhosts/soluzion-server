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
    username: string | null;
  };
  set_name: {
    name: string;
  };
  set_roles: {
    roles: number[];
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
  roles_changed: {
    username: string;
    roles: number[];
  };
  /**
   * This is a comment
   */
  game_started: {
    state: string | null; // JSON representation of state
    message: string; // state's __str__
  };
  game_ended: {
    message: string;
  };
  operator_applied: {
    state: string | null; // JSON representation of state
    message: string; // state's __str__
    operator: {
      name: string;
      op_no: number;
      params: any[] | null;
    };
  };
  operators_available: {
    operators: {
      name: string;
      op_no: number;
      params:
        | {
            name: string;
            type: "int" | "float" | "str";
            min: number | null;
            max: number | null;
          }[]
        | null;
    }[];
  };
  transition: {
    message: string;
  };
  error: {
    event: ServerEvent;
    error: ServerError;
    message: string | null;
  };
};

type ServerError =
  | "RoomAlreadyExists"
  | "NotInARoom"
  | "CantJoinRoom"
  | "GameAlreadyStarted"
  | "GameNotStarted"
  | "InvalidOperator"
  | "InvalidRoles";

type Role = {
  name: string;
  min: number | null;
  max: number | null;
};
