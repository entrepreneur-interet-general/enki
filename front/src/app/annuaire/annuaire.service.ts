import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { CONTACTS } from '../mocks/contacts-mocks';

export interface Contact {
  uuid: string;
  name: string;
  group: string;
  function: string;
  phone: string;
  address: string;
} 
@Injectable({
  providedIn: 'root'
})
export class AnnuaireService {
  contacts: Contact[] = CONTACTS;

  constructor() { }

  getUserFavoriteContacts(): Observable<Contact[]> {
    return of(this.contacts);
  }

  getContactDetail(uuid: string): Observable<Contact> {
    return of(this.contacts.filter(contact => contact.uuid === uuid)[0]);
  }

  
}
