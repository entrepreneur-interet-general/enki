import { Component } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../environments/environment';
import { UserService } from './user/user.service';
import jwt_decode from 'jwt-decode';
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';

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
  user;

  constructor(
    private keycloakService: KeycloakService,
    public userService: UserService,
    private titleService: Title
    ) {

      this.titleService.setTitle('Gestion de crise | ENKI')
      this.environment = environment;
      this.keycloakService.getToken().then((res) => {
        this.token = res;
        window.localStorage.setItem('token', res);
      })
      
      this.fetchedAffaire = false;

  }
  // tslint:disable-next-line:use-lifecycle-interface
  ngOnInit(): void {
    console.log(`---
Bienvenue sur 🅴🅽🅺🅸 !
Un petit 🅱🅱🆃🅴🅰 ?
---
`)
  }

  canSeeEvents(): boolean {
    return this.keycloakService.isUserInRole('watchEvents');
  }

}
