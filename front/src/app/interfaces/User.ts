import { Contact } from './Contact';

export interface User {
  first_name?: string;
  last_name?: string;
  position?: string;
  attributes?: {
    fonction?: string
  };
  location: string;
  fullname?: string;
  contacts: Contact[];
}
