import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchEtablissementComponent } from './search-etablissement.component';
import { SearchEtablissementService } from './search-etablissement.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'search-etablissement',
    component: SearchEtablissementComponent
  }
]

@NgModule({
  declarations: [SearchEtablissementComponent],
  providers: [
    SearchEtablissementService
  ],
  imports: [
    ReactiveFormsModule,
    CommonModule,
    RouterModule.forChild(routes)
  ]
})
export class SearchEtablissementModule { }
