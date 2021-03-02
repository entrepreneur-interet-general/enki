export interface Contact {
  uuid?: string;
  first_name: string;
  last_name: string;
  group_id: string;
  group_type: string;
  position_id: string;
  tel: {
    mobile: string;
  };
  email: string;
  address: string;
}
