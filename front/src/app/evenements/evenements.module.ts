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

const routes : Routes = [
  {
    path: 'evenements/create',
    canActivate: [ AuthGuard ],
    component: CreateEvenementComponent
  },
  {
    path: 'evenements',
    canActivate: [AuthGuard],
    component: DetailEvenementComponent,
    /* resolve: {
      event: EvenementDetailResolverService
    }, */
    children: [
      {
        path: ':uuid',
        redirectTo: 'summary/:uuid'
      },
      {
        path: 'summary/:uuid',
        component: SummaryEvenementComponent,
        resolve: {
          event: EvenementDetailResolverService
        }
      },
      {
        path: 'maincourante/:uuid',
        component: MainCouranteComponent,
        children: [
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
  },
]

@NgModule({
  declarations: [
    CreateEvenementComponent,
    DetailEvenementComponent,
    MainCouranteComponent,
    AddMessageComponent,
    AddLabelComponent,
    FilterLabelsPipe,
    DetailMessageComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)
  ]
})
export class EvenementsModule { }
