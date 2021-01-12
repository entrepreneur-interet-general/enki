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
  httpOptions: object;
  constructor(
    private http: HttpClient
  ) {
    this.evenements = []
    this.evenementsUrl = `http://localhost:5000/api/enki/v1/events`
    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
      })
    }
  }

  getEvenements(): Observable<Evenement[]> {
    return this.http.get<any>(this.evenementsUrl, this.httpOptions)
      .pipe(
        map(response => response.evenements)
      )
  }

  getEvenement(uuid): Observable<Evenement> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(response => response.evenement)
      )
  }
}
