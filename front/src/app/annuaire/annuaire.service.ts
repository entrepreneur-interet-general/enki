import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { CONTACTS, ANNUAIRE } from '../mocks/contacts-mocks';
import { Contact } from '../interfaces/Contact';

@Injectable({
  providedIn: 'root'
})
export class AnnuaireService {
  contacts: Contact[] = CONTACTS;
  annuaire: Contact[] = ANNUAIRE;

  constructor() { }

  // GET /annuaire/search?q=queryString
  searchInAnnuaire(queryString: string): Observable<Contact[]> {
    return of(this.annuaire)
  }
  // POST /annuaire/add
  addContactToAnnuaire(contact: Contact): Observable<Contact> {
    return of(contact)
  }
  // GET /annuaire/{uuid}
  getContactDetails(contactId: string): Observable<Contact> {
    return of(this.annuaire.filter(contact => contact.uuid === contactId)[0]);
  }
  // PUT /annuaire/{uuid}
  updateContactDetails(contact: Contact): Observable<Contact> {
    return of(contact)
  }
  // DELETE /annuaire/{uuid}
  removeContactFromAnnuaire(contactId: string): Observable<string> {
    return of(contactId)
  }

}
