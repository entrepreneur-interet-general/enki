import { environment } from '../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';
import { BehaviorSubject, Observable, of } from 'rxjs';

import { UserService } from '../user/user.service';

export interface Affaire {
  id?: string; // used for in memory db
  uuid: string;
  dateTimeSent: object;
  natureDeFait: string;
  resource?: any;
  coord: Coordinates;
  victims: number;
  address: string;
  evenement_id: string;
}
interface Coordinates {
  lat: number;
  long: number;
}
@Injectable({
  providedIn: 'root'
})

export class AffairesService {
  readonly _affaires = new BehaviorSubject<Affaire[]>([]);

  interventionsUrl: string;
  affaires: Affaire[];
  httpOptions: object;

  constructor(
    private http: HttpClient,
    private userService: UserService
    ) {
      this.affaires = []
      this.interventionsUrl = `${environment.backendUrl}/affairs`;
      this.httpOptions = {
      };
    }

  getAffaires(): Affaire[] {
    return this._affaires.getValue();
  }
  private _setAffaires(affaires: Affaire[]): void {
    this._affaires.next(affaires);
  } 
  getAffaireByID(uuid: string): Affaire {
    return this.getAffaires().filter(affaire => affaire.uuid === uuid)[0];
  }


  mapHTTPAffaires(affaires): Affaire[] {
    let updatedAffaires: Affaire[];
    updatedAffaires = affaires.map(affaire => {
      return {
        uuid: affaire.uuid,
        evenement: affaire.evenement,
        evenement_id: affaire.evenement_id,
        dateTimeSent: new Date(affaire.affair.createdAt),
        natureDeFait: affaire.affair.primaryAlert.alertCode.whatsHappen.label,
        victims: affaire.affair.primaryAlert.alertCode.victims.count,
        coord: {
          lat: affaire.affair.eventLocation.coord.lat,
          long: affaire.affair.eventLocation.coord.lon
        },
        address: affaire.affair.eventLocation.address
      };
    });
    return updatedAffaires;
  }

  httpGetAllAffaires(): Observable<Affaire[]> {
    // if there's already affaires in memory, send these
    if (this.affaires !== undefined && this.affaires.length > 0) {
      return of(this.affaires);
    }
    if (!this.userService.user.attributes) {
      return of([]);
    }
    // if(this.userService.user.)
    return this.http.get<any>(`${environment.backendUrl}/users/me/affairs`, this.httpOptions)
      .pipe(
        map(affaires => {
          // affaires = environment.HTTPClientInMemory ? affaires : affaires.data;
          const updatedAffaires = this.mapHTTPAffaires(affaires.data);
          this._setAffaires(updatedAffaires)
          return updatedAffaires;
        }),
        tap(_ => this.log('fetched all affaires'))
      );
  }

  httpGetAffaire(uuid: string): Observable<Affaire> {
    return this.http.get<any>(`${this.interventionsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(affaire => {
          affaire = environment.HTTPClientInMemory ? affaire : affaire.data;
          let interventionsArray: Affaire[] = [];
          interventionsArray.push(affaire);
          interventionsArray = this.mapHTTPAffaires(interventionsArray);
          return interventionsArray[0];
        }),
        tap(_ => this.log('fetched one affaire'))
      );
  }

  getAffairesFromMemory(): Affaire[] {
    return this.affaires;
  }

  getAffaireFromMemory(uuid: string): Affaire {
    return this.affaires ? this.affaires.filter(affaire => affaire.uuid === uuid)[0] : null;
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

