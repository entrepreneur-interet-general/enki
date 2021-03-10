import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Contact } from '../interfaces/Contact';
import { map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AnnuaireService {
  contacts: Contact[] = [];
  annuaire: Contact[] = [];

  constructor(
    private http: HttpClient
  ) { }

  // GET /annuaire/search?q=queryString
  searchInAnnuaire(query: string): Observable<Contact[]> {
    return this.http.get<any>(`${environment.backendUrl}/contacts?query=${query}`)
      .pipe(
        map(contacts => {
          this.annuaire = contacts.data
          return contacts.data
        })
      )
  }
  // POST /annuaire/add
  addContactToAnnuaire(contact: Contact): Observable<Contact> {
    return this.http.post<any>(`${environment.backendUrl}/contacts`, contact)
      .pipe(
        tap(contact => {
          this.annuaire = this.annuaire.concat(contact)
          
        })
      )
  }
  // GET /annuaire/{uuid}
  getContactDetails(contactId: string): Observable<Contact> {
    return this.http.get<any>(`${environment.backendUrl}/contacts/${contactId}`)
      .pipe(
        map(contact => {
          return contact.data
        })
      )
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
