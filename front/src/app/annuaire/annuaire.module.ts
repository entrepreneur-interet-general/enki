import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContactListComponent } from './contact-list/contact-list.component';
import { ContactDetailComponent } from './contact-detail/contact-detail.component';
import { SearchContactComponent } from './search-contact/search-contact.component';


@NgModule({
  declarations: [
    ContactListComponent,
    ContactDetailComponent,
    SearchContactComponent
  ],
  imports: [
    CommonModule
  ]
})
export class AnnuaireModule { }
