import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { Intervention, InterventionsService } from '../interventions/interventions.service';
import { User } from '../interfaces/User';
import { Participant } from '../interfaces/Participant';

export interface Evenement {
  uuid: string;
  title: string;
  description: string;
  created_at: string;
  closed: boolean;
  user_roles: Participant[];
}

@Injectable({
  providedIn: 'root'
})
export class EvenementsService {

  evenements: Array<Evenement>
  evenementsUrl: string;
  selectedEvenement = new BehaviorSubject<Evenement>({
    uuid: '',
    title: '',
    description: '',
    created_at: '',
    closed: false,
    user_roles: []
  });
  httpOptions: object;
  constructor(
    private http: HttpClient,
    private interventionsService: InterventionsService
    ) {
      this.evenements = []
      this.evenementsUrl = `${environment.backendUrl}/events`
      this.httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json'
        })
      }
  }

  getEvenements(): Observable<Evenement[]> {
    return this.http.get<any>(`${environment.backendUrl}/users/me/events`)
      .pipe(
        map(response => {
          return response.data.map(event => {
            return {
              uuid: event.uuid,
              title: event.title,
              description: event.description,
              created_at: event.created_at,
              closed: event.closed,
              user_roles: event.user_roles
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
  addParticipantsToEvenement(participant: Participant): void {
    const copyEvent = this.selectedEvenement.getValue()
    copyEvent.user_roles = copyEvent.user_roles.concat(participant)
    this.selectedEvenement.next(copyEvent);
  }
  changeParticipantRole(participant: Participant): void {
    const copyEvent = this.selectedEvenement.getValue();

    // Replace the right participant by the received one
    const newUserRoles = copyEvent.user_roles.map(user_role => {
      if (user_role.user.uuid === participant.user.uuid) {
        return participant
      } else {
        return user_role
      }
    })
    copyEvent.user_roles = newUserRoles
    this.selectedEvenement.next(copyEvent)
  }
  selectEvenement(event: Evenement): void {
    this.selectedEvenement.next(event);
  }
  getSignalementsForEvenement(uuid): Observable<Intervention[]> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}/affairs`, this.httpOptions)
      .pipe(
        map(response => {
          return this.interventionsService.mapHTTPInterventions(response.data)
        })
      )
  }

  closeEvenement(uuid: string): Observable<any> {
    return this.http.put<any>(`${environment.backendUrl}/events/${uuid}/close`, {})
  }
}
