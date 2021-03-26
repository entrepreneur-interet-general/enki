import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Evenement, EvenementsService, EvenementType } from '../evenements.service';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { SearchLocationService } from 'src/app/search-location/search-location.service';
import { HTTP_DATA } from 'src/app/constants';
import { pluck } from 'rxjs/operators';

@Component({
  selector: 'app-create-evenement',
  templateUrl: './create-evenement.component.html',
  styleUrls: ['./create-evenement.component.scss']
})
export class CreateEvenementComponent implements OnInit {

  evenementGroup = new FormGroup({
    nomEvenement: new FormControl('', Validators.required),
    descriptionEvenement: new FormControl('', Validators.required),
    startDate: new FormControl('', Validators.required),
    startNow: new FormControl(true),
    location: new FormControl('', Validators.required),
    eventType: new FormControl('', Validators.required)
  })

  evenementUrl: string;
  evenement: object;
  httpOptions: object;
  todayDay: Date;
  public EvenementTypeEnum = EvenementType;

  constructor(
    private http: HttpClient,
    private evenementsService: EvenementsService,
    private router: Router,
    private searchLocationService: SearchLocationService,
  ) {
    this.todayDay = new Date();
    this.evenementUrl = `${environment.backendUrl}/events`
    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
      })
    }
    this.searchLocationService.selectedEtablissement.subscribe(location => {
      this.evenementGroup.controls.location.setValue(location.label)
    })
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    const startDate = !this.evenementGroup.controls.startNow.value ? (new Date(this.evenementGroup.controls.startDate.value)).toISOString() : (new Date()).toISOString()
    let formBody = {
      "creator_id": "my_id",
      "title": this.evenementGroup.value.nomEvenement,
      "description": this.evenementGroup.value.descriptionEvenement,
      "started_at": startDate,
      "location_id": this.searchLocationService.selectedEtablissement.getValue().uuid,
      "type": this.evenementGroup.value.eventType
    }
    this.httpFormSubmit(formBody).subscribe(response => {
      this.evenementsService.addOrUpdateEvenement(response)
      this.router.navigate([`evenements/${response.uuid}`])
    })
  }

  goToSearchLocation(): void {
    // this.router.navigate([''])
    this.router.navigate([`evenements/create/searchlocation`])

  }

  httpFormSubmit(formBody): Observable<Evenement> {
    return this.http.post<any>(this.evenementUrl, formBody, this.httpOptions).pipe(
      pluck(HTTP_DATA)
    )
  }

}
