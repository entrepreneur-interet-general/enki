import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FocusFormInputDirective } from './focus-form-input.directive';



@NgModule({
  declarations: [
    FocusFormInputDirective
  ],
  imports: [
    CommonModule
  ],
  exports: [
    FocusFormInputDirective
  ]
})
export class DirectivesModule { }
