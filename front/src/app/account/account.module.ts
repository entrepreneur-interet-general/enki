import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { InvitationComponent } from './invitation/invitation.component';
import { AccountComponent } from './account.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SearchEtablissementComponent } from '../search-etablissement/search-etablissement.component';

const routes : Routes = [
  {
    path: 'account',
    component: AccountComponent,
    children: [
      {
        path: '',
        redirectTo: 'invitation',
        pathMatch: 'full'
      },
      {
        path: 'invitation',
        component: InvitationComponent,
        children: [
          {
            path: 'searchetablissement',
            component: SearchEtablissementComponent
          }
        ]
      }
    ]
  }
]

@NgModule({
  declarations: [
    AccountComponent,
    InvitationComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes),
    
  ]
})
export class AccountModule { }
