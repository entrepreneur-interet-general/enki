import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainCouranteComponent } from './main-courante/main-courante.component';
import { MessageComponent } from './message/message.component';
import { AddMessageComponent } from './add-message/add-message.component';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../app-auth-guard.service';
import { ReactiveFormsModule } from '@angular/forms';


const routes : Routes = [
  {
    path: 'maincourante',
    component: MainCouranteComponent,
    canActivate: [AuthGuard],
    data: { roles: ['watchEvents'] }
  },
  {
    path: 'addmessage',
    component: AddMessageComponent,
    canActivate: [AuthGuard],
    data: { roles: ['watchEvents'] }
  }
];
@NgModule({
  declarations: [MainCouranteComponent, MessageComponent, AddMessageComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes)

  ]
})
export class MainCouranteModule { }
