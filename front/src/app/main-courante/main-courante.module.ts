import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainCouranteComponent } from './main-courante/main-courante.component';
import { MessageComponent } from './message/message.component';
import { AddMessageComponent } from './add-message/add-message.component';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../app-auth-guard.service';
import { ReactiveFormsModule } from '@angular/forms';
import { AddLabelComponent } from './add-label/add-label.component';


const routes : Routes = [
  {
    path: 'maincourante',
    component: MainCouranteComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'addmessage',
    component: AddMessageComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'addlabel',
    component: AddLabelComponent,
    canActivate: [AuthGuard]
  }
];
@NgModule({
  declarations: [MainCouranteComponent, MessageComponent, AddMessageComponent, AddLabelComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes)

  ]
})
export class MainCouranteModule { }
