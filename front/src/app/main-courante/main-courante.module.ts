import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainCouranteComponent } from './main-courante/main-courante.component';
import { MessageComponent } from './message/message.component';
import { AddMessageComponent } from './add-message/add-message.component';



@NgModule({
  declarations: [MainCouranteComponent, MessageComponent, AddMessageComponent],
  imports: [
    CommonModule
  ]
})
export class MainCouranteModule { }
