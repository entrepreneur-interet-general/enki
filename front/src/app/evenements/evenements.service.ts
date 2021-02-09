import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Intervention, InterventionsService } from '../interventions/interventions.service';

export interface Evenement {
  uuid: string;
  title: string;
  description: string;
  started_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class EvenementsService {

  evenements: Array<Evenement>
  evenementsUrl: string;
  selectedEvenement: Evenement;
  httpOptions: object;
  constructor(
    private http: HttpClient,
    private interventionsService: InterventionsService
    ) {
      this.evenements = []
      this.evenementsUrl = `${environment.backendUrl}/events`
      this.selectedEvenement = {
        uuid: '',
        title: '',
        description: '',
        started_at: ''
      }
      this.httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json'
        })
      }
  }

  getEvenements(): Observable<Evenement[]> {
    return this.http.get<any>(this.evenementsUrl)
      .pipe(
        map(response => {
          return response.data.map(event => {
            return {
              uuid: event.uuid,
              title: event.title,
              description: event.description,
              started_at: event.started_at
            }
          })
        })
      )
  }

  getEvenement(uuid): Observable<Evenement> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(response => response.data)
      )
  }
  selectEvenement(event: Evenement): void {
    this.selectedEvenement = event;
  }
  getSignalementsForEvenement(uuid): Observable<Intervention[]> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}/affairs`, this.httpOptions)
      .pipe(
        map(response => {
          return this.interventionsService.mapHTTPInterventions(response.data)
        })
      )
  }
}
