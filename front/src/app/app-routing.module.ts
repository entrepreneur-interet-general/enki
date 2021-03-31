import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
import { UserInfoGuard } from './guards/user-info.guard';
import { ListeInterventionsComponent } from './interventions/liste-interventions/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard/user-dashboard.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
// import { SituationsComponent } from './situations/situations.component';
import { ListeEvenementsComponent } from './evenements/liste-evenements/liste-evenements.component';
import { EvenementsModule } from './evenements/evenements.module';
import { AnnuaireModule } from './annuaire/annuaire.module';
import { RegistrationModule } from './registration/registration.module';
import { DirectivesModule } from './directives.module';

const routes: Routes = [
  {
    path: '',
    canActivate: [ UserInfoGuard ],
    children: [
      {
        path: 'dashboard',
        component: UserDashboardComponent,
      },
      {
        path: 'interventions',
        component: ListeInterventionsComponent
      },
      {
        path: 'evenements',
        component: ListeEvenementsComponent
      },
      {
        path: 'detail-intervention/:uuid',
        component: DetailInterventionComponent
      }
    ]
  },
  { path: '**', component: PageNotFoundComponent }

];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {scrollOffset: [0, 0], scrollPositionRestoration: 'enabled' }),
    DirectivesModule,
    EvenementsModule,
    AnnuaireModule,
    RegistrationModule,
  ],
  exports: [ RouterModule ],
  providers: [ AuthGuard ]
})
export class AppRoutingModule { }
