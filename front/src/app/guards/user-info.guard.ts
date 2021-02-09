import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, ActivatedRoute, Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class UserInfoGuard implements CanActivate {
  constructor(
    private userService: UserService,
    private router: Router
  ) {

  }
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      console.log(route)
      return this.userIsAuth(route);
  }

  userIsAuth(routerSnapshot): Observable<boolean | UrlTree> {
    if (this.userService.userExist) {
      return of(this.getUrlTreeFromCurrentSnapshot(routerSnapshot))
    } else {
      return this.userService.getUserInfo().pipe(
        map(res => {
          if (res.answer === 'yes') {
            this.userService.userExist = true
          }
          // let urlTreeToSend = this.userExist && routerSnapshot ? this.router.parseUrl('/dashboard'): this.router.parseUrl('/register/step1')
          // return this.userExist ? true : urlTreeToSend
          return this.getUrlTreeFromCurrentSnapshot(routerSnapshot)
        }
        // return res.answer === 'yes'
        )
      )
    }
  }
    
  getUrlTreeFromCurrentSnapshot(routerSnapshot) {
    const routerSnapshotIsRegister = routerSnapshot.url.length > 0 && routerSnapshot.url[0].path === 'register' ? true : false
    if (this.userService.userExist) {
      if (routerSnapshotIsRegister) {
        return this.router.parseUrl('/dashboard')
      } else {
        return true
      }
    } else {
      if (routerSnapshotIsRegister){
        return true
      } else {
        return this.router.parseUrl('/register/step1')
      }
    }
  }
  
}
