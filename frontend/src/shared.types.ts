export enum UserRole {
  Admin = 'admin',
  User = 'user',
}

export interface Profile {
  id: number,
  username: string,
  email: string,
  role: UserRole
}

export interface Game {
  id: number,
  name: string,
  image: string,
  participantCount: number[]
}
