import { Component, OnInit } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { UserService } from 'src/app/user/user.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  menuActive: boolean;

  constructor(private keycloakService: KeycloakService,
    public userService: UserService) {
    this.menuActive = false;
  }

  ngOnInit(): void {
  }

  openCloseMenu(): void {
    this.menuActive = this.menuActive ? false : true;
  }
  canSeeEvents(): boolean {
    return this.keycloakService.isUserInRole('watchEvents')
  }
  logout(): void {
    this.keycloakService.logout()
  }

}
