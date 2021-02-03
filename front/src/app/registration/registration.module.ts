import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchLocationComponent } from './register/search-location/search-location.component';
import { FirstStepComponent } from './register/first-step/first-step.component'
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { RegisterService } from './register.service';

const routes : Routes = [
  {
    path: 'register',
    component: RegisterComponent,
    children: [
      {
        path: '',
        redirectTo: 'step1',
        pathMatch: 'full'
      },
      {
        path: 'step1',
        component: FirstStepComponent
      },
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
    SearchLocationComponent,
    RegisterComponent
  ],
  providers: [ RegisterService ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)

  ]
})
export class RegistrationModule { }

