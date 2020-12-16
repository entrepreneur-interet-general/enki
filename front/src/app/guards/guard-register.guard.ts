import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { KeycloakService } from 'keycloak-angular';
import { Observable } from 'rxjs';
import { UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class GuardRegisterGuard implements CanActivate {
  constructor(
    private keycloakService: KeycloakService,
    private router: Router,
    private userService: UserService
  ) {

  }
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      return true
      // if (this.keycloakService.isUserInRole('watchEvents')) return this.router.parseUrl('/dashboard')
      // return true;

  }
  
}
