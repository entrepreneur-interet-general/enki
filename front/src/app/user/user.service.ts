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

  updateUser(user) {
    this.user = {
      attributes: {
        code_insee: user.attributes.code_insee ? user.attributes.code_insee[0] : '',
        fonction: user.attributes.fonction ? user.attributes.fonction[0] : ''
      },
      fullname: user.lastname ? user.lastname : ''
    }
  }

  loadUserProfile(): void {
    this.keycloakService.loadUserProfile(true).then((response: any) => {
      
      this.user = {
        attributes: {
          code_insee: response.attributes.code_insee ? response.attributes.code_insee[0] : '',
          fonction: response.attributes.fonction ? response.attributes.fonction[0] : ''
        },
        fullname: response.lastname ? response.lastname : ''
      }
    })
  }
}
