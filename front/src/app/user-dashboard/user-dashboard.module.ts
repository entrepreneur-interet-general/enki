import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [UserDashboardComponent],
  imports: [
    CommonModule
  ],
  exports: [
    UserDashboardComponent,
    RouterModule
  ]
})
export class UserDashboardModule {}
