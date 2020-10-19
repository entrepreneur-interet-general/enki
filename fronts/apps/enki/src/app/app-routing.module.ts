import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
import { TestAuthComponent } from './test-auth/test-auth.component';


const routes: Routes = [
  {
    path: 'test',
    canActivate: [AuthGuard],
    component: TestAuthComponent,
    data: { roles: ['accessEnki'] }
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
