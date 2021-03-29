import { Component } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../environments/environment';
import { UserService } from './user/user.service';
import { Title } from '@angular/platform-browser';
import { MobilePrototypeService } from './mobile-prototype/mobile-prototype.service';
import { BehaviorSubject } from 'rxjs';

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
  showOnboarding = new BehaviorSubject<boolean>(true);

  constructor(
    private keycloakService: KeycloakService,
    public userService: UserService,
    private titleService: Title,
    public mobilePrototype: MobilePrototypeService
    ) {

      this.titleService.setTitle('Gestion de crise | ENKI')
      this.environment = environment;
      this.keycloakService.getToken().then((res) => {
        this.token = res;
        window.localStorage.setItem('token', res);
      })
      this.showOnboarding.next(window.localStorage.getItem('showOnboarding') === 'true' || window.localStorage.getItem('showOnboarding') === null ? true : false)
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

  onActivate(): void {
    window.scroll(0, 0);
  }

  hideOnboarding(): void {
    window.localStorage.setItem('showOnboarding', 'false')
    this.showOnboarding.next(false)
  }

  canSeeEvents(): boolean {
    return this.keycloakService.isUserInRole('watchEvents');
  }

}
