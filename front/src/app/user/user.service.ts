import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { Observable, of } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { AnnuaireService } from '../annuaire/annuaire.service';
import { Contact } from '../interfaces/Contact';
import { User } from '../interfaces/User';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;

  constructor(
    // private keycloakService: KeycloakService,
    private annuaireService: AnnuaireService,
    private http: HttpClient
  ) {
    this.user = {
      attributes: {
        code_insee: "",
        fonction: ""
      },
      contacts: []
    };
  }

  // GET /user/{uuid}/favoriteContacts
  getUserFavoriteContacts(): Observable<Contact[]> {
    return this.http.get<any>(`${environment.backendUrl}/users/me/contact/favorites`)
      .pipe(
        map(contacts => {
          this.user.contacts = contacts.data
          return contacts.data
        })
      )
    // return of(this.user.contacts);
  }
  isUserFav(contactId: string): boolean {
    return this.user.contacts.some(contact => contact.uuid === contactId)
  }
  // PUT /user/me/favoriteContacts/{uuid}
  addContactToUserFavs(contactId: string): Observable<Contact[]> {
    return this.http.put<any>(`${environment.backendUrl}/users/me/contact/favorites/${contactId}`, '')
      .pipe(
        map(
          response => {
            return response.data
          }
        )
      )
    return of(this.user.contacts.concat(this.annuaireService.annuaire.filter(contact => contact.uuid === contactId)[0]))
      .pipe(
        tap(response => {
          this.user.contacts = response
        })
      )
  }
  // DELETE /user/{uuid}/favoriteContacts/{uuid}
  removeContactFromUserFavs(contactId: string): Observable<Contact[]> {
    return of(this.user.contacts.filter(contact => contact.uuid !== contactId))
      .pipe(
        tap(response => {
          this.user.contacts = response
        })
      )
  }

  userIsValid(): boolean {
    return Object.keys(this.user).length > 0 && this.user.attributes.code_insee !== '' && this.user.attributes.fonction !== ''
  }

/*   loadUserProfile(): void {
    this.keycloakService.loadUserProfile().then((response: any) => {
      this.user = {
        attributes: {
          code_insee: response.attributes.code_insee[0] ? response.attributes.code_insee[0] : '',
          fonction: response.attributes.fonction[0] ? response.attributes.fonction[0] : ''
        },
        contacts: response.contacts,
        fullname: response.lastName && response.firstName ? `${response.firstName} ${response.lastName}` : ''
      }
    })
  } */
}
