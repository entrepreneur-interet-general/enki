import { environment } from '../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { Affaire } from '../interfaces/Affaire';

import { UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})

export class AffairesService {
  readonly _affaires = new BehaviorSubject<Affaire[]>([]);

  affairesUrl: string;
  evenementsUrl: string;

  constructor(
    private http: HttpClient,
    private userService: UserService
    ) {
      this.affairesUrl = `${environment.backendUrl}/affairs`;
      this.evenementsUrl = `${environment.backendUrl}/events`;
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

  updateAffaireEvenementID(evenementUUID: string, affaireUUID: string): void {
    let affaires = this.getAffaires();
    const affaireToUpdate = this.getAffaireByID(affaireUUID);
    affaireToUpdate.evenement_id = evenementUUID;
    affaires.map(affaire => affaire.uuid === affaireUUID ? affaireToUpdate : affaire);
    this._setAffaires(affaires);
  }
  attachEvenementToAffaire(evenementUUID: string, affaireUUID: string): Observable<any> {
    return this.http.put(`${this.evenementsUrl}/${evenementUUID}/affairs/${affaireUUID}`, {})
      .pipe(
        tap(() => {
          this.updateAffaireEvenementID(evenementUUID, affaireUUID)
        })
      )
  }
  detachEvenementToAffaire(evenementUUID: string, affaireUUID: string): Observable<any> {
    return this.http.delete(`${this.evenementsUrl}/${evenementUUID}/affairs/${affaireUUID}`)
      .pipe(
        tap(() => {
          this.updateAffaireEvenementID(null, affaireUUID)
        })
      )
  }

  mapHTTPAffaires(affaires: any[]): Affaire[] {
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
    if (!this.userService.user.attributes) {
      return of([]);
    }
    return this.http.get<any>(`${environment.backendUrl}/users/me/affairs`)
      .pipe(
        map(affaires => {
          const updatedAffaires = this.mapHTTPAffaires(affaires.data);
          this._setAffaires(updatedAffaires)
          return updatedAffaires;
        }),
        tap(_ => this.log('fetched all affaires'))
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

