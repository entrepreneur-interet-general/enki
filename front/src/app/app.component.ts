import { Component } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../environments/environment';
import { UserService } from './user/user.service';

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
    public userService: UserService
    ) {
      this.environment = environment
      this.keycloakService.getToken().then((res) => {
        this.token = res
        window.localStorage.setItem('token', res)
      });
      this.fetchedAffaire = false;
  }
  ngOnInit(): void {

  }

  logout(): void {
    this.keycloakService.logout()
  }
  canSeeEvents(): boolean {
    return this.keycloakService.isUserInRole('watchEvents')
  }

}
