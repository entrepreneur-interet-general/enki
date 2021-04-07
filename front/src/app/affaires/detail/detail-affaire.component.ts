import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Observable, of } from 'rxjs';
import { Affaire, AffairesService } from '../affaires.service'
import { ActivatedRoute, Router } from '@angular/router';
import { Evenement, EvenementsService } from 'src/app/evenements/evenements.service';
import { FormControl, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { tap } from 'rxjs/operators';
import { HistoryUrlService } from '../../history-url.service';

@Component({
  selector: 'fronts-detail-affaire',
  templateUrl: './detail-affaire.component.html',
  styleUrls: ['./detail-affaire.component.scss']
})
export class DetailAffaireComponent implements OnInit {
  affaire: Affaire;
  fetchedAffaire: boolean;
  uuid: string;
  evenementsList: Evenement[];
  evenementsUrl: string;
  previousLinkLabel: string;
  readonly CREATE_EVENT_VALUE: string;
  evenementGroup = new FormGroup({
    evenement: new FormControl({value:'', disabled: false})
  });
  selectedEvenementTitle: string;
  constructor(
    private interventionsService: AffairesService,
    private route: ActivatedRoute,
    private historyUrl: HistoryUrlService,
    private evenementsService: EvenementsService,
    private http: HttpClient,
    private _location: Location,
    ) {
      this.CREATE_EVENT_VALUE = 'create';
      this.previousLinkLabel = this.historyUrl.getPreviousLabel()

      this.evenementsList = [];
      this.evenementsUrl = `${environment.backendUrl}/events`;
      this.evenementGroup.controls.evenement.valueChanges.subscribe(value => {
        if (value === this.CREATE_EVENT_VALUE) {
          console.log('create event')
        }
      })
    }

  

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      if (this.interventionsService.getAffaireFromMemory(this.uuid)) {
        this.affaire = this.interventionsService.getAffaireFromMemory(this.uuid)
        this.getEvenements();
        this.fetchedAffaire = true
      } else {
        this.interventionsService.httpGetAffaire(this.uuid).subscribe((affaire) => {
          this.affaire = affaire
          this.getEvenements();
          this.fetchedAffaire = true;
        });
      }

    });
  }
  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
    document.querySelector('main').scroll(0,0)
  }
  getEvenements(): void {
    this.evenementsService.getEvenementsByHTTP().subscribe((evenements) => {
      this.evenementsList = evenements;
      if (this.affaire.evenement_id) {
        this.evenementGroup.controls.evenement.setValue(this.affaire.evenement_id);
        this.selectedEvenementTitle = this.evenementsService.getEvenementByID(this.affaire.evenement_id).title;
      } else {
        this.evenementGroup.controls.evenement.setValue('');
      }
    })
  }
  getAffaire(): Observable<Affaire> {
    return of(this.affaire)
  }
  attachEvenementToAffaire(): void {
    this.submitAttachEvenementToAffaire().subscribe(() => {
      // console.log(this.evenementsService.getEvenements(), this.affaire.evenement_id)
      // console.log(this.evenementsService.getEvenementByID(this.affaire.evenement_id))
      this.selectedEvenementTitle = this.evenementsService.getEvenementByID(this.evenementGroup.controls.evenement.value).title;
    })
  }
  submitAttachEvenementToAffaire(): Observable<any> {
    return this.http.put(`${this.evenementsUrl}/${this.evenementGroup.value.evenement}/affairs/${this.uuid}`, {})
      .pipe(
        tap(() => {
          // change current affaire "evenementID"
          this.interventionsService.affaires = this.interventionsService.affaires.map((affaire) => {
            if (affaire.uuid === this.uuid) {
              affaire.evenement_id = this.evenementGroup.value.evenement
            }
            return affaire
          })
        })
      )
  }
  detachEvenementToAffaire(): void {
    this.submitDetachEvenementToAffaire().subscribe(() => {
      console.log()
    })
  }
  submitDetachEvenementToAffaire(): Observable<any> {
    return this.http.delete(`${this.evenementsUrl}/${this.evenementGroup.value.evenement}/affairs/${this.uuid}`)
      .pipe(
        tap(() => {
          console.log('test')
        })
      )
  }
  goBack(): void {
    this._location.back()
  }
}
