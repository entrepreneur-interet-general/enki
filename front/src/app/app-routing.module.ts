import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
import { GuardRegisterGuard } from './guards/guard-register.guard';
import { GuardTestGuard } from './guards/guard-test.guard';
import { ListeInterventionsComponent } from './interventions/liste/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard/user-dashboard.component';
import { FirstStepComponent } from './registration/first-step/first-step.component';
import { SecondStepComponent } from './registration/second-step/second-step.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { MainCouranteComponent } from './main-courante/main-courante/main-courante.component';
import { AddMessageComponent } from './main-courante/add-message/add-message.component';


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
    canActivate: [ GuardTestGuard ]
  },
  {
    path: 'maincourante',
    component: MainCouranteComponent,
    canActivate: [ GuardTestGuard ]
  },
  {
    path: 'addmessage',
    component: AddMessageComponent,
    canActivate: [ GuardTestGuard ]
  },
  {
    path: 'liste-interventions',
    canActivate: [ GuardTestGuard ],
    component: ListeInterventionsComponent
  },
  {
    path: 'detail-intervention/:uuid',
    canActivate: [ GuardTestGuard ],
    component: DetailInterventionComponent
  },
  {
    path: '',
    redirectTo: '/register/step1', pathMatch: 'full'
  },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
