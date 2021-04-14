import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Contact } from '../interfaces/Contact';
import { User } from '../interfaces/User';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;
  userExist: boolean;

  constructor(
    private http: HttpClient
  ) {
    this.user = {
      attributes: {
        fonction: ''
      },
      location: '',
      location_id: '',
      contacts: [],
      uuid: ''
    };

  }

  getUserInfo(): Observable<any> {
    return this.http.get(`${environment.backendUrl}/users/me`)
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
    return this.user.contacts.some(contact => contact.uuid === contactId);
  }
  // PUT /user/me/favoriteContacts/{uuid}
  addContactToUserFavs(contactId: string): Observable<Contact[]> {
    return this.http.put<any>(`${environment.backendUrl}/users/me/contact/favorites/${contactId}`, '')
      .pipe(
        tap(response => {
          this.user.contacts = response.data;
        })
      );
  }
  // DELETE /user/{uuid}/favoriteContacts/{uuid}
  removeContactFromUserFavs(contactId: string): Observable<Contact[]> {
    return this.http.delete<any>(`${environment.backendUrl}/users/me/contact/favorites/${contactId}`)
      .pipe(
        tap(response => {
          this.user.contacts = response.data
        })
      )
  }

  userIsValid(): boolean {
    return Object.keys(this.user).length > 0 && this.user.location !== '' && this.user.attributes.fonction !== '';
  }

}
