import { Contact } from './Contact'

export interface User {
  attributes?: {
    code_insee?: string,
    fonction?: string
  },
  fullname?: string;
  contacts: Contact[]
}