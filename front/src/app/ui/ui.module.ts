import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SvgDefinitionsComponent } from './svg-definitions/svg-definitions.component';
import { SmallHeadingComponent } from './small-heading/small-heading.component';
import { RouterModule } from '@angular/router';
import { ModalComponent } from './modal/modal.component';



@NgModule({
  declarations: [
    SvgDefinitionsComponent,
    SmallHeadingComponent,
    ModalComponent,
  ],
  exports: [
    SvgDefinitionsComponent,
    SmallHeadingComponent,
    ModalComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class UiModule { }
