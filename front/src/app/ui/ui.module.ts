import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SvgDefinitionsComponent } from './svg-definitions/svg-definitions.component';
import { SmallHeadingComponent } from './small-heading/small-heading.component';
import { RouterModule } from '@angular/router';



@NgModule({
  declarations: [
    SvgDefinitionsComponent,
    SmallHeadingComponent
  ],
  exports: [
    SvgDefinitionsComponent,
    SmallHeadingComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class UiModule { }
