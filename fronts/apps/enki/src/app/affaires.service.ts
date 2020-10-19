import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import * as NatureDeFait from './naturedefait.json'
import { KeycloakService } from 'keycloak-angular';

interface Affaires {
  hits: Hits
}
interface Hits {
  hits: []
}
interface Affaire {
  natureDeFait: string;
  nbDeVictimes: string;
  location: {
    lon: number;
    lat: number;
  };
  adresse: string;
}
@Injectable({
  providedIn: 'root'
})

export class AffairesService {
  affairesUrl: string;
  httpOptions: object;
  naturedefait;

  constructor(
    private http: HttpClient,
    private keycloakService: KeycloakService
    ) { 
      this.affairesUrl = 'http://localhost:9200/affaire/_search'
      this.httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.keycloakService.getToken() })
      };
      this.naturedefait = (NatureDeFait as any).default
    }

  getAffaires(): Observable<Affaire[]> {
    return this.http.get<Affaires>(this.affairesUrl, this.httpOptions)
      .pipe(
        map(affaires => {
          let newAffaires = []
          newAffaires = affaires.hits.hits.map((affaire: any) => {
            const newAffaire: Affaire = {
              natureDeFait: affaire._source.nature_de_fait_0_label,
              nbDeVictimes: affaire._source.nombre_de_victimes,
              adresse: affaire._source.adresse,
              location: {
                lon: affaire._source.location.lon,
                lat: affaire._source.location.lat
              }
            }
            
            return newAffaire
          })
          affaires.hits.hits
          return newAffaires
        }),
        tap(_ => this.log('fetched affaires'))
      );
  }
  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
  private log(message: string): void {
    console.log(message);
  }
}

