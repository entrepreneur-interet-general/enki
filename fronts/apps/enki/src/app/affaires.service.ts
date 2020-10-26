import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import * as NatureDeFait from './naturedefait.json'
import { KeycloakService } from 'keycloak-angular';

interface Affaire {
  dateTimeSent: object;
  resource?: any;
  coord: Coordinates;
  victims: number;
  address: string;
}
interface Coordinates {
  lat: number,
  long: number
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
      this.affairesUrl = 'http://localhost:5000/affairs'
      this.httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.keycloakService.getToken() })
      };
      this.naturedefait = (NatureDeFait as any).default
    }

  getAffaires(): Observable<Affaire[]> {
    return this.http.get<any>(this.affairesUrl, this.httpOptions)
      .pipe(
        map(affaires => {
          let newAffaires = []
          // debugger;
          newAffaires = affaires.affairs.map((affaire: Affaire) => {
            const newAffaire: Affaire = {
              dateTimeSent: affaire.dateTimeSent,
              victims: affaire.resource.message.choice.primaryAlert.alertCode.victims.count,
              coord: {
                lat: affaire.resource.message.choice.eventLocation.coord.lat,
                long: affaire.resource.message.choice.eventLocation.coord.lon
              },
              address: affaire.resource.message.choice.eventLocation.address
            }
            
            return newAffaire
          })
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

