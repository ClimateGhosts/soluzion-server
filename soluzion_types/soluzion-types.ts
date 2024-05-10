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
type ClientToServer = keyof ClientToServerEvents;
type ClientToServerEvents = {
  /**
   * Request for the server to create a new room
   */
  create_room: {
    room: string;
  };
  /**
   * Request for the server to delete an empty room
   */
  delete_room: {
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
  start_game: {
    /**
     * If present, args option to past in as a dict to the State() constructor of the SOLUZION problem
     */
    args: object | null;
  };
  /**
   * Request for a specific operator to be replied within the sender's game session
   */
  operator_chosen: {
    op_no: number;
    params: any[] | null;
  };
  /**
   * Gets information about the roles of the SOLZUION Problem
   */
  list_roles: {};
  /**
   * Lists all active rooms
   */
  list_rooms: {};
  /**
   * Get information about the problem and the server
   */
  info: {};
};

type ClientToServerResponse = {
  list_roles: {
    roles: Role[];
  };
  list_rooms: {
    rooms: Room[];
  };
  info: {
    server_version: string;
    soluzion_version: string;
    problem_name: string;
    problem_version: string;
    problem_authors: string[];
    problem_creation_date: string;
    problem_desc: string;
  };
};

type Room = {
  room: string;
  owner: string;
  in_game: boolean;
  players: Player[];
};

type Player = {
  sid: string;
  name: string;
  roles: number[];
};

/**
 * Events handled by the client (sent by the server)
 */
type ServerToClient = keyof ServerToClientEvents;
type ServerToClientEvents = {
  /**
   * Inform the client of its sid
   */
  your_sid: {
    sid: string;
  };
  /**
   * A room with the given name has been created
   */
  room_created: {
    room: string;
    owner_sid: string;
  };
  /**
   * A room with the given name has been deleted
   */
  room_deleted: {
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
   * Catch all event for when anything about a room state changes
   */
  room_changed: Room;
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
};

type ErrorResponse = {
  error?: {
    type: ServerError;
    message: string | null;
  } | null;
};

type ServerError =
  | "RoomAlreadyExists"
  | "NotInARoom"
  | "CantJoinRoom"
  | "CantDeleteRoom"
  | "GameAlreadyStarted"
  | "GameNotStarted"
  | "InvalidOperator"
  | "InvalidRoles"
  | "ResponseTimeout";

type Role = {
  name: string;
  min: number | null;
  max: number | null;
};

/**
 * For a Typescript client, your Socket can have type
 * ```
 * Socket<SocketTypes<ServerToClientEvents>, SocketTypes<ClientToServerEvents>>
 * ```
 */
type SocketTypes<
  T extends Record<string, any>,
  R extends Record<string, any> = any,
> = {
  [K in keyof T]: (
    event: T[K],
    callback?: (
      response: K extends keyof R
        ? ErrorResponse & R[K]
        : ErrorResponse | undefined,
    ) => void,
  ) => void;
};
