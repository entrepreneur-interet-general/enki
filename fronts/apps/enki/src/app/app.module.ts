import { BrowserModule } from '@angular/platform-browser';
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { KeycloakAngularModule, KeycloakService } from 'keycloak-angular';

import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { ListeInterventionsComponent } from './interventions/liste/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { SvgDefinitionsComponent } from './ui/svg-definitions/svg-definitions.component';
import { HeaderComponent } from './ui/header/header.component';

import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService } from './in-memory-data.service';

function initializeKeycloak(keycloak: KeycloakService) {
  return () =>
    keycloak.init({
      config: {
        "realm": "sapeurs",
        "url": "http://localhost:8084/auth/",
        "clientId": "enki",
      },
      initOptions: {
        onLoad: 'login-required'
      },
    });
}
@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    ListeInterventionsComponent,
    DetailInterventionComponent,
    SvgDefinitionsComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    // The HttpClientInMemoryWebApiModule module intercepts HTTP requests
    // and returns simulated server responses.
    // Remove it when a real server is ready to receive requests.
    environment.HTTPClientInMemory ? HttpClientInMemoryWebApiModule.forRoot(
      InMemoryDataService, { dataEncapsulation: false }
    ) : [],
    AppRoutingModule,
    KeycloakAngularModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production })
  ],
  providers: [{
    provide: APP_INITIALIZER,
    useFactory: initializeKeycloak,
    multi: true,
    deps: [KeycloakService],
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
