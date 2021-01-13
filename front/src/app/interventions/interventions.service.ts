import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { KeycloakService } from 'keycloak-angular';

import { User, UserService } from '../user/user.service';

export interface Intervention {
  id?: string; // used for in memory db
  uuid: string;
  dateTimeSent: object;
  natureDeFait: string;
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

export class InterventionsService {
  interventionsUrl: string;
  interventions: Intervention[];
  httpOptions: object;

  constructor(
    private http: HttpClient,
    private keycloakService: KeycloakService,
    private userService: UserService
    ) { 
      this.interventionsUrl = environment.interventionsUrl;
      this.httpOptions = {
/*         headers: new HttpHeaders({ 'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.keycloakService.getToken() }) */
      };
    }

  mapHTTPInterventions(interventions): Intervention[] {
    let updatedInterventions: Intervention[];
    updatedInterventions = interventions.map(intervention => {
      return {
        uuid: intervention.eventId,
        dateTimeSent: new Date(intervention.createdAt),
        natureDeFait: intervention.primaryAlert.alertCode.whatsHappen.label,
        victims: intervention.primaryAlert.alertCode.victims.count,
        coord: {
          lat: intervention.eventLocation.coord.lat,
          long: intervention.eventLocation.coord.lon
        },
        address: intervention.eventLocation.address
      }
    })
    return updatedInterventions
  }

  httpGetAllInterventions(): Observable<Intervention[]> {
    // if there's already interventions in memory, send these
    if (this.interventions !== undefined && this.interventions.length > 0) {
      return of(this.interventions)
    }
    if (!this.userService.user.attributes) {
      return of([]);
    }
    return this.http.get<any>(`${this.interventionsUrl}?insee_code=${this.userService.user.attributes.code_insee}`, this.httpOptions)
      .pipe(
        map(interventions => {
          interventions = environment.HTTPClientInMemory ? interventions : interventions.data
          let updatedInterventions = this.mapHTTPInterventions(interventions)
          this.interventions = updatedInterventions
          return updatedInterventions
        }),
        tap(_ => this.log('fetched all interventions'))
      );
  }

  httpGetIntervention(uuid: string): Observable<Intervention> {
    return this.http.get<any>(`${this.interventionsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(intervention => {
          intervention = environment.HTTPClientInMemory ? intervention : intervention.data
          let interventionsArray: Intervention[] = [];
          interventionsArray.push(intervention);
          interventionsArray = this.mapHTTPInterventions(interventionsArray)
          return interventionsArray[0]
        }),
        tap(_ => this.log('fetched one intervention'))
      );
  }

  getInterventionsFromMemory(): Intervention[] {
    return this.interventions;
  }

  getInterventionFromMemory(uuid: string): Intervention {
    return this.interventions ? this.interventions.filter(intervention => intervention.uuid == uuid)[0] : null
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

