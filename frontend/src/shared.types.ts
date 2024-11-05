export enum UserRole {
  Admin = 'admin',
  User = 'user',
}

export type User = {
  id: number;
  username: string;
  role: UserRole;
}

export type Profile = {
  id: number;
  username: string;
  email: string;
  role: UserRole;
  userGames: PlayerGame[];
}

export type Game = {
  id: number;
  name: string;
  image: string;
  participantCount: number[];
}
export type PlayerGame = {
  rating: number;
  gameId: number;
  game: Game;
};

export type Player = {
  id: number;
  username: string;
  userGames: PlayerGame[];
};



export type Team = {
  id: number;
  name: string;
  members: Player[];
};


export type Match = {
  id: number;
  status: string;
  datetime: Date;
  playersNumber: number;
  totalTeamsMembers: number;
  totalPlayers: number;
  winnerTeamId: ?number;
  ownerId: number;
  connectionKey: string;
  connectionDescription: string;
  streamUrl: ?string;
  game: Game;
  teams: Team[];
}

export type Status = {
  label: string;
  value: string;
};

