import { Component } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../environments/environment';
import { UserService } from './user/user.service';
import jwt_decode from 'jwt-decode';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'enki';
  affaire;
  fetchedAffaire: boolean;
  token;
  environment;
  

  constructor(
    private keycloakService: KeycloakService,
    public userService: UserService,
    ) {
      this.environment = environment
      this.keycloakService.getToken().then((res) => {
        this.token = res
        window.localStorage.setItem('token', res)
        let decodedJWT: any = jwt_decode(res)

        this.userService.user.attributes.fonction = decodedJWT.fonction ? decodedJWT.fonction : ""
        this.userService.user.location = decodedJWT.code_insee ? decodedJWT.code_insee : ""
        if (this.userService.userIsValid()) {
          // this.router.navigate(['dashboard'])
        }
      });
      this.fetchedAffaire = false;
  }
  ngOnInit(): void {

  }

  canSeeEvents(): boolean {
    return this.keycloakService.isUserInRole('watchEvents')
  }

}
