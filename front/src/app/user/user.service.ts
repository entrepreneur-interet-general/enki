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

  async loadUserProfile(): Promise<boolean> {
    let _this = this
    return new Promise(resolve => {
      this.keycloakService.loadUserProfile().then((response: any) => {
      _this.user = {
        attributes: {
          code_insee: response.attributes.code_insee ? response.attributes.code_insee[0] : '',
          fonction: response.attributes.fonction ? response.attributes.fonction[0] : ''
        }
      }
      resolve(true)
    })
  })
  }

 /*  assignUser(userProfile): void {
    this.user = {
      attributes: {
        code_insee: userProfile.attributes.code_insee ? userProfile.attributes.code_insee[0] : '',
        fonction: userProfile.attributes.fonction ? userProfile.attributes.fonction[0] : ''
      },
      fullname: userProfile.lastname ? userProfile.lastname : ''
    }
    Promise.resolve(this.user)
  } */

/*   async loadUserProfile(): Observable<boolean> {
    let _this = this
    let response = await this.keycloakService.loadUserProfile()
    .then((response: any) => {
      _this.user = {
        attributes: {
          code_insee: response.attributes.code_insee ? response.attributes.code_insee[0] : '',
          fonction: response.attributes.fonction ? response.attributes.fonction[0] : ''
        },
        fullname: response.lastname ? response.lastname : ''
      }
    })
    return of(true)
     return new Promise(resolve => {
      this.keycloakService.loadUserProfile().then((response: any) => {
        debugger;
        _this.user = {
          attributes: {
            code_insee: response.attributes.code_insee ? response.attributes.code_insee[0] : '',
            fonction: response.attributes.fonction ? response.attributes.fonction[0] : ''
          },
          fullname: response.lastname ? response.lastname : ''
        }
        resolve(_this.user)
      })
    })
  } */
}
