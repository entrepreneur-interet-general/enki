import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { CONTACTS, ANNUAIRE } from '../mocks/contacts-mocks';

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
  annuaire: Contact[] = ANNUAIRE;

  constructor() { }

  getUserFavoriteContacts(): Observable<Contact[]> {
    return of(this.contacts);
  }


  getContactDetail(uuid: string): Observable<Contact> {
    return of(this.contacts.filter(contact => contact.uuid === uuid)[0]);
  }

  // PUT /user/{uuid}/favoriteContacts/{uuid}
  addContactToUserFavs(contactId: string): Observable<Contact[]> {
    return of(this.contacts.concat(this.annuaire[contactId]))
  }

  // DELETE /user/{uuid}/favoriteContacts/{uuid}

}
