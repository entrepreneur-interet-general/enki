import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

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
  // currentEvenement$;
  constructor(
    private http: HttpClient
    ) {
      this.evenements = []
      this.evenementsUrl = `http://localhost:5000/api/enki/v1/events`
      this.selectedEvenement = {
        uuid: '',
        title: '',
        description: '',
        started_at: ''
      }
      this.httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      }
  }

  getEvenements(): Observable<Evenement[]> {
    return this.http.get<any>(this.evenementsUrl, this.httpOptions)
      .pipe(
        map(response => response.data)
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
  getEvenementFromMemory(uuid: string): Evenement {
    return this.evenements ? this.evenements.filter(event => event.uuid == uuid)[0] : null
  }
}
