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
  affaires;
  number = add(1, 2);
  

  constructor(private affairesService: AffairesService, private keycloakService: KeycloakService
    ) {
  }
  ngOnInit(): void {
    this.affairesService.getAffaires().subscribe((affaires) => {
      this.affaires = affaires
    })
  }
  logout(): void {
    this.keycloakService.logout()
  }
  canSeeEvents(): boolean {
    return this.keycloakService.isUserInRole('watchEvents')
  }
}
