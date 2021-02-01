export interface Contact {
  uuid?: string;
  first_name: string;
  last_name: string;
  group_name: string;
  position: string;
  tel: {
    mobile: string;
  };
  email: string;
  address: string;
} 