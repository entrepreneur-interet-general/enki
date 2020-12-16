import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { KeycloakService } from 'keycloak-angular';
import { Observable } from 'rxjs';
import { User, UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class GuardTestGuard implements CanActivate {
  constructor(private router: Router,
    private userService: UserService,
    private keycloakService: KeycloakService){

  }
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      return new Observable<boolean>((observer) => {
        console.log("Loading...")
        if (this.userService.userIsComplete()) {
          observer.next(true)
          observer.complete()
        }
        this.keycloakService.loadUserProfile().then((response: any) => {
          console.log(response)
          this.userService.user = {
            attributes: {
              code_insee: response.attributes.code_insee ? response.attributes.code_insee[0] : '',
              fonction: response.attributes.fonction ? response.attributes.fonction[0] : ''
            }
          }
          if (this.userService.userIsComplete()) {
              observer.next(true)
          } else {
            this.router.navigate(['register/step1'])
            observer.next(false)
          }
          observer.complete()
        })
      })
    // return this.userService.userIsComplete() ? true : this.router.navigate(['register/step1']);
  }
  
}
