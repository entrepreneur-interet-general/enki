import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
// import { AppComponent } from './app.component';
import { ListeInterventionsComponent } from './interventions/liste/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FirstStepComponent } from './registration/first-step/first-step.component';
import { SecondStepComponent } from './registration/second-step/second-step.component';


const routes: Routes = [
  {
    path: 'register/step1',
    component: FirstStepComponent
  },
  {
    path: 'register/step2',
    component: SecondStepComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [ AuthGuard ],
    data: { roles: ['watchEvents'] }
  },
  {
    path: 'liste-interventions',
    canActivate: [ AuthGuard ],
    component: ListeInterventionsComponent,
    data: { roles: ['watchEvents'] }
  },
  {
    path: 'detail-intervention/:uuid',
    canActivate: [AuthGuard],
    component: DetailInterventionComponent,
    data: {
      roles: ['watchEvents']
    }
  },
  {
    path: '',
    redirectTo: '/register/step1', pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
