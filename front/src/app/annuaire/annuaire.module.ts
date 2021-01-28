import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContactListComponent } from './contact-list/contact-list.component';
import { ContactDetailComponent } from './contact-detail/contact-detail.component';
import { SearchContactComponent } from './search-contact/search-contact.component';
import { RouterModule, Routes } from '@angular/router';
import { ContactAddComponent } from './contact-add/contact-add.component';
import { AnnuaireComponent } from './annuaire.component';
import { AnnuaireService } from './annuaire.service';
import { ReactiveFormsModule } from '@angular/forms';

const routes : Routes = [
  {
    path: 'annuaire',
    component: AnnuaireComponent,
    children: [
      {
        path: '',
        redirectTo: 'contactlist',
        pathMatch: 'full'
      },
      {
        path: 'contactlist',
        component: ContactListComponent,
      },
      {
        path: 'searchcontact',
        component: SearchContactComponent
      },
      {
        path: 'contactdetail',
        component: ContactDetailComponent
      }
    ]
  },
  {
    path: 'contactadd',
    component: ContactAddComponent
  }
]
@NgModule({
  declarations: [
    ContactListComponent,
    ContactDetailComponent,
    SearchContactComponent,
    ContactAddComponent,
    AnnuaireComponent
  ],
  providers: [AnnuaireService],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)
  ]
})
export class AnnuaireModule { }
