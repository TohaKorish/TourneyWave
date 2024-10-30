export enum UserRole {
  Admin = 'admin',
  User = 'user',
}

export type Profile = {
  id: number;
  username: string;
  email: string;
  role: UserRole;
}

export type Game = {
  id: number;
  name: string;
  image: string;
  participantCount: number[];
}

export type Match = {
  id: number;
  status: string;
  datetime: Date;
  playersNumber: number;
  totalTeamsMembers: number;
  totalPlayers: number;
  game: Game;
}
