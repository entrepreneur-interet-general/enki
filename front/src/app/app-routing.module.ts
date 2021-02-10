import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
import { GuardRegisterGuard } from './guards/guard-register.guard';
import { UserInfoGuard } from './guards/user-info.guard';
import { ListeInterventionsComponent } from './interventions/liste-interventions/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard/user-dashboard.component';
import { SecondStepComponent } from './registration/second-step/second-step.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SituationsComponent } from './situations/situations.component';
import { ListeEvenementsComponent } from './evenements/liste-evenements/liste-evenements.component';
import { EvenementsModule } from './evenements/evenements.module';
import { AnnuaireModule } from './annuaire/annuaire.module';
import { RegistrationModule } from './registration/registration.module';
import { REGISTER } from './constants';

const routes: Routes = [
  {
    path: '',
    canActivate: [ UserInfoGuard ],
    children: [
/*       {
        path: `${REGISTER}/step2`,
        component: SecondStepComponent,
        canActivate: [ GuardRegisterGuard ]
      }, */
      {
        path: 'dashboard',
        component: UserDashboardComponent,
      },
      {
        path: 'situations',
        component: SituationsComponent,
        children: [
          {
            path: 'interventions',
            component: ListeInterventionsComponent
          },
          {
            path: 'evenements',
            component: ListeEvenementsComponent
          }
        ]
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
    RouterModule.forRoot(routes),
    EvenementsModule,
    AnnuaireModule,
    RegistrationModule
  ],
  exports: [ RouterModule ],
  providers: [ AuthGuard ]
})
export class AppRoutingModule { }
