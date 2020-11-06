import { Component } from '@angular/core';
import { AffairesService } from './affaires.service'
import { add } from '@fronts/utilities'
import { KeycloakService } from 'keycloak-angular';

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
  

  constructor(private affairesService: AffairesService, private keycloakService: KeycloakService
    ) {
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
