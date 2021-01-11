import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';
import { AppRoutingModule } from '../app-routing.module';



@NgModule({
  declarations: [UserDashboardComponent],
  imports: [
    AppRoutingModule,
    CommonModule
  ],
  exports: [
    UserDashboardComponent
  ]
})
export class UserDashboardModule { }
