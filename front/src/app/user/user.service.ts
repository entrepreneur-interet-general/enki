import { Injectable, resolveForwardRef } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { Observable, of } from 'rxjs';

export interface User {
  attributes?: {
    code_insee?: string,
    fonction?: string
  },
  fullname?: string
}

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;

  constructor(
    private keycloakService: KeycloakService
  ) {
    this.user = {};
  }

  userIsComplete(): boolean {
    if (Object.keys(this.user).length > 0) {
      return this.user.attributes.code_insee.length > 0 && this.user.attributes.fonction.length > 0
    }
    return false
  }

}
