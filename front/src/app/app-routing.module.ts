import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
import { GuardRegisterGuard } from './guards/guard-register.guard';
import { ListeInterventionsComponent } from './interventions/liste-interventions/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard/user-dashboard.component';
import { FirstStepComponent } from './registration/first-step/first-step.component';
import { SecondStepComponent } from './registration/second-step/second-step.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SituationsComponent } from './situations/situations.component';
import { ListeEvenementsComponent } from './evenements/liste-evenements/liste-evenements.component';
import { EvenementsModule } from './evenements/evenements.module';
import { AnnuaireModule } from './annuaire/annuaire.module';

const routes: Routes = [
  {
    path: 'register/step1',
    component: FirstStepComponent,
    canActivate: [ GuardRegisterGuard ]
  },
  {
    path: 'register/step2',
    component: SecondStepComponent,
    canActivate: [ GuardRegisterGuard ]
  },
  {
    path: 'dashboard',
    component: UserDashboardComponent,
    // canActivate: [ AuthGuard ]
  },
  {
    path: 'situations',
    canActivate: [ AuthGuard ],
    component: SituationsComponent,
    children: [
      {
        path: 'interventions',
        canActivate: [ AuthGuard ],
        component: ListeInterventionsComponent
      },
      {
        path: 'evenements',
        canActivate: [ AuthGuard ],
        component: ListeEvenementsComponent
      }
    ]
  },
  {
    path: 'detail-intervention/:uuid',
    canActivate: [AuthGuard],
    component: DetailInterventionComponent
  },
  {
    path: '',
    redirectTo: '/dashboard', pathMatch: 'full'
  },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' }),
    EvenementsModule,
    AnnuaireModule
  ],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
