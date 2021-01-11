import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { KeycloakService } from 'keycloak-angular';
import { UserService } from '../user/user.service'
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GuardRegisterGuard implements CanActivate {
  constructor(
    private keycloakService: KeycloakService,
    private userService: UserService,
    private router: Router
  ) {

  }
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      if (this.userService.userIsValid()) return this.router.parseUrl('/dashboard')
      return true;

  }
  
}
