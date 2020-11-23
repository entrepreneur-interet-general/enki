import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
// import { AppComponent } from './app.component';
import { ListeInterventionsComponent } from './interventions/liste/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { DashboardComponent } from './dashboard/dashboard.component';


const routes: Routes = [
  {
    path: 'dashboard',
    component: DashboardComponent
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
    redirectTo: '/dashboard', pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
