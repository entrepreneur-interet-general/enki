import { Contact } from './Contact'

export interface User {
  attributes?: {
    fonction?: string
  },
  location: string;
  fullname?: string;
  contacts: Contact[]
}