import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../app-auth-guard.service';
import { CreateEvenementComponent } from './create-evenement/create-evenement.component';
import { DetailEvenementComponent } from './detail-evenement/detail-evenement.component';
import { SummaryEvenementComponent } from './summary-evenement/summary-evenement.component';
import { ReactiveFormsModule } from '@angular/forms';
import { MainCouranteComponent } from './main-courante/main-courante/main-courante.component';
import { AddMessageComponent } from './main-courante/add-message/add-message.component';
import { AddLabelComponent } from './main-courante/add-label/add-label.component';
import { FilterLabelsPipe } from './main-courante/add-label/filter-labels.pipe';
import { DetailMessageComponent } from './main-courante/detail-message/detail-message.component';
import { EvenementDetailResolverService } from './evenement-detail-resolver.service';
import { ListeMainCouranteComponent } from './main-courante/liste-main-courante/liste-main-courante.component';
import { MessagesService } from './main-courante/messages.service';
import { UiModule } from '../ui/ui.module';
import { UserInfoGuard } from '../guards/user-info.guard';


const routes : Routes = [
  {
    path: '',
    canActivate: [ UserInfoGuard ],
    children: [
      {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full'
      },
      {
        path: 'evenements/create',
        canActivate: [ AuthGuard ],
        component: CreateEvenementComponent
      },
      {
        path: 'evenements/:uuid',
        canActivate: [AuthGuard],
        component: DetailEvenementComponent,
        resolve: {
          event: EvenementDetailResolverService
        },
        children: [
          {
            path: '',
            redirectTo: 'summary',
            pathMatch: 'full'
          },
          {
            path: 'summary',
            component: SummaryEvenementComponent,
          },
          {
            path: 'maincourante',
            component: MainCouranteComponent,
            children: [
              {
                path: '',
                redirectTo: 'liste',
                pathMatch: 'full'
              },
              {
                path: 'liste',
                component: ListeMainCouranteComponent
              },
              {
                path: 'detailmessage/:uuid',
                component: DetailMessageComponent
              },
              {
                path: 'addmessage',
                component: AddMessageComponent,
                children: [
                  {
                    path: 'addlabel',
                    component: AddLabelComponent
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
]

@NgModule({
  declarations: [
    CreateEvenementComponent,
    DetailEvenementComponent,
    MainCouranteComponent,
    AddMessageComponent,
    AddLabelComponent,
    FilterLabelsPipe,
    DetailMessageComponent,
    SummaryEvenementComponent,
    ListeMainCouranteComponent
  ],
  providers: [MessagesService],
  imports: [
    UiModule,
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)
  ]
})
export class EvenementsModule { }
