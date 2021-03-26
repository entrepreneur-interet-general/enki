import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchLocationComponent } from './search-location.component';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { DirectivesModule } from '../directives.module';

const routes: Routes = [
  {
    path: 'search-location',
    component: SearchLocationComponent
  }
]

@NgModule({
  declarations: [
    SearchLocationComponent,
  ],
  imports: [
    ReactiveFormsModule,
    CommonModule,
    DirectivesModule,
    RouterModule.forChild(routes),
  ]
})
export class SearchLocationModule { }
