import { Injectable } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';

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

  userIsValid(): boolean {
    return Object.keys(this.user).length > 0 && this.user.attributes.code_insee !== '' && this.user.attributes.fonction !== ''
  }

  loadUserProfile(): void {
    this.keycloakService.loadUserProfile().then((response: any) => {
      this.user = {
        attributes: {
          code_insee: response.attributes.code_insee[0] ? response.attributes.code_insee[0] : '',
          fonction: response.attributes.fonction[0] ? response.attributes.fonction[0] : ''
        },
        fullname: response.lastName && response.firstName ? `${response.firstName} ${response.lastName}` : ''
      }
    })
  }
}
