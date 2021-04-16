import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Observable } from 'rxjs';
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
    private affairesService: AffairesService,
    private route: ActivatedRoute,
    private historyUrl: HistoryUrlService,
    private evenementsService: EvenementsService,
    private http: HttpClient,
    private _location: Location,
    private router: Router
    ) {
      this.CREATE_EVENT_VALUE = 'create';
      this.previousLinkLabel = this.historyUrl.getPreviousLabel()

      this.evenementsList = [];
      this.evenementsUrl = `${environment.backendUrl}/events`;
    }

  

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      if (this.affairesService.getAffaireByID(this.uuid)) {
        this.affaire = this.affairesService.getAffaireByID(this.uuid)
        this.getEvenements();
        this.fetchedAffaire = true
      } else {
        this.affairesService.httpGetAllAffaires().subscribe(() => {
          this.affaire = this.affairesService.getAffaireByID(this.uuid)
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
  attachEvenementToAffaire(): void {
    if (this.evenementGroup.controls.evenement.value === this.CREATE_EVENT_VALUE) {
      this.router.navigate(['./create-evenement'], { queryParams: { affaireUUID: this.uuid }, relativeTo: this.route});
      return;
    }
    this.submitAttachEvenementToAffaire().subscribe(() => {
      this.selectedEvenementTitle = this.evenementsService.getEvenementByID(this.evenementGroup.controls.evenement.value).title;
    })
  }
  submitAttachEvenementToAffaire(): Observable<any> {
    return this.http.put(`${this.evenementsUrl}/${this.evenementGroup.value.evenement}/affairs/${this.uuid}`, {})
      .pipe(
        tap(() => {
          // change current affaire "evenementID"
          this.affairesService.updateAffaireEvenementID(this.evenementGroup.value.evenement, this.uuid)
        })
      )
  }
  detachEvenementToAffaire(): void {
    this.submitDetachEvenementToAffaire().subscribe()
  }
  submitDetachEvenementToAffaire(): Observable<any> {
    return this.http.delete(`${this.evenementsUrl}/${this.evenementGroup.value.evenement}/affairs/${this.uuid}`)
      .pipe(
        tap(() => {
          this.affairesService.updateAffaireEvenementID(null, this.uuid)
        })
      )
  }
  goBack(): void {
    this._location.back()
  }
}
