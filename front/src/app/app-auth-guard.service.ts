import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  Router,
  RouterStateSnapshot,
} from '@angular/router';
import { KeycloakAuthGuard, KeycloakService } from 'keycloak-angular';
import { UserService } from './user/user.service';

 
@Injectable({
  providedIn: 'root',
})
export class AuthGuard extends KeycloakAuthGuard {
  constructor(
    protected readonly router: Router,
    protected readonly keycloak: KeycloakService,
    private userService: UserService
  ) {
    super(router, keycloak);
  }
 
  public async isAccessAllowed(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    // Force the user to log in if currently unauthenticated.
    if (!this.authenticated) {
      await this.keycloak.login({
        redirectUri: window.location.origin + state.url,
      });
    }
    if (Object.keys(this.userService.user).length === 0) {
      this.userService.loadUserProfile()
    }
 
    // Get the roles required from the route.
    const requiredRoles = route.data.roles;
    // Allow the user to to proceed if no additional roles are required to access the route.
    if (!(requiredRoles instanceof Array) || requiredRoles.length === 0) {
      return true;
    }
 
    // Allow the user to proceed if all the required roles are present.
    return requiredRoles.every((role) => this.roles.includes(role)) ? true : this.router.parseUrl('/register/step1');
  }
}