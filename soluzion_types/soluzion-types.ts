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
  /**
   * Request for the server to create a new room
   */
  create_room: {
    room: string;
  };
  /**
   * Request for the sender to join an existing room, optionally setting a username
   */
  join_room: {
    room: string;
    username: string | null;
  };
  /**
   * Request to set the sender's username
   */
  set_name: {
    name: string;
  };
  /**
   * Request to set the sender's roles
   */
  set_roles: {
    roles: number[];
  };
  /**
   * Request for the sender to leave their current room
   */
  leave_room: {};
  /**
   * Request to start the game for the sender's current room
   */
  start_game: {};
  /**
   * Request for a specific operator to be replied within the sender's game session
   */
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
  /**
   * A room/lobby with the given name has been created
   */
  room_created: {
    room: string;
  };
  /**
   * A user has joined the client's room
   */
  room_joined: {
    username: string;
  };
  /**
   * A user has left the current client's room
   */
  room_left: {
    username: string;
  };
  /**
   * A user in the current room has a changed set of roles
   */
  roles_changed: {
    username: string;
    /**
     * Role numbers are indices within the Soluzion problem's ROLES array
     */
    roles: number[];
  };
  /**
   * The game has been started for the current client's room
   */
  game_started: {
    /**
     * JSON representation of new state
     */
    state: string | null;
    /**
     * new state's __str__ message
     */
    message: string;
  };
  /**
   * The game has ended for the current client's room
   */
  game_ended: {
    message: string;
  };
  /**
   * An operator was applied for the current client's game, transforming the state
   */
  operator_applied: {
    /**
     * JSON representation of new state
     */
    state: string | null;
    /**
     * new state's __str__ output
     */
    message: string;
    operator: {
      name: string;
      op_no: number;
      params: any[] | null;
    };
  };
  /**
   * A new set of operators is available for the current client
   */
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
  /**
   * A transition event has occurred for the current client's game
   */
  transition: {
    message: string;
  };
  /**
   * An error has been caused by one of the ServerEvents this client has sent
   */
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
