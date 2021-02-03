import { Component, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchLocationComponent } from './first-step/search-location/search-location.component';
import { FirstStepComponent } from './first-step/first-step.component'
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

const routes : Routes = [
  {
    path: 'register/step1',
    component: FirstStepComponent,
    children: [
      {
        path: 'searchlocation',
        component: SearchLocationComponent
      }
    ]
  }
]

@NgModule({
  declarations: [
    FirstStepComponent,
    SearchLocationComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)

  ]
})
export class RegistrationModule { }

