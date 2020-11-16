import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { KeycloakService } from 'keycloak-angular';

export interface Intervention {
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
  interventionUrl: string;
  interventionsUrl: string;
  interventions: Intervention[];
  httpOptions: object;

  constructor(
    private http: HttpClient,
    private keycloakService: KeycloakService
    ) { 
      this.interventionUrl = environment.interventionUrl;
      this.interventionsUrl = environment.interventionsUrl;
      this.httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.keycloakService.getToken() })
      };
    }

  mapHTTPInterventions(interventions): Intervention[] {
    let updatedInterventions: Intervention[];
    interventions = environment.HTTPClientInMemory ? interventions : interventions.affairs
    updatedInterventions = interventions.map(intervention => {
      return {
        uuid:  environment.HTTPClientInMemory ? intervention.id : intervention.distributionID,
        dateTimeSent: new Date(intervention.dateTimeSent),
        natureDeFait: intervention.resource.message.choice.primaryAlert.alertCode.whatsHappen.label,
        victims: intervention.resource.message.choice.primaryAlert.alertCode.victims.count,
        coord: {
          lat: intervention.resource.message.choice.eventLocation.coord.lat,
          long: intervention.resource.message.choice.eventLocation.coord.lon
        },
        address: intervention.resource.message.choice.eventLocation.address
      }
    })
    return updatedInterventions
  }

  getAllInterventions(): Observable<Intervention[]> {
    // if there's already interventions in memory, send these
    if (this.interventions !== undefined && this.interventions.length > 0) {
      return of(this.interventions)
    }
    return this.http.get<any>(this.interventionsUrl, this.httpOptions)
      .pipe(
        map(interventions => {
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

