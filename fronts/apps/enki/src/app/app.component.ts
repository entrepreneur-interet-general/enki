import { Component } from '@angular/core';
import { add } from '@fronts/utilities'
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'enki';
  affaire;
  fetchedAffaire: boolean;
  number = add(1, 2);
  token;
  environment;
  

  constructor(private keycloakService: KeycloakService
    ) {
      this.environment = environment
      this.keycloakService.getToken().then((res) => {
        this.token = res
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
