import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SvgDefinitionsComponent } from './svg-definitions/svg-definitions.component';
import { SmallHeadingComponent } from './small-heading/small-heading.component';
import { RouterModule } from '@angular/router';
import { ModalComponent } from './modal/modal.component';
import { ToastComponent } from './toast/toast.component';



@NgModule({
  declarations: [
    SvgDefinitionsComponent,
    SmallHeadingComponent,
    ModalComponent,
    ToastComponent
  ],
  exports: [
    SvgDefinitionsComponent,
    SmallHeadingComponent,
    ToastComponent,
    ModalComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class UiModule { }
