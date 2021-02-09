import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, ActivatedRoute, Router, PRIMARY_OUTLET } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { UserService } from '../user/user.service';
import { REGISTER } from '../constants';

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
      // send the first segment of requested route
      return this.userIsAuth(this.router.parseUrl(state.url).root.children[PRIMARY_OUTLET].segments[0].path);
  }

  userIsAuth(firstSegmentRouterSnapshot): Observable<boolean | UrlTree> {
    if (this.userService.userExist) {
      return of(this.getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot))
    } else {
      return this.userService.getUserInfo().pipe(
        map(res => {
          if (res.answer === 'yes') {
            this.userService.userExist = true
          }
          return this.getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot)
        }
        // return res.answer === 'yes'
        )
      )
    }
  }
    
  getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot) {
    if (this.userService.userExist) {
      if (firstSegmentRouterSnapshot === 'register') {
        return this.router.parseUrl('/dashboard')
      } else {
        return true
      }
    } else {
      if (firstSegmentRouterSnapshot === REGISTER){
        return true
      } else {
        return this.router.parseUrl(`/${REGISTER}/step1`)
      }
    }
  }
  
}
