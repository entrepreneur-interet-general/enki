import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, pluck, tap } from 'rxjs/operators';
import { Intervention, InterventionsService } from '../interventions/interventions.service';
import { Participant } from '../interfaces/Participant';
import { HTTP_DATA } from '../constants';
import { Message } from './main-courante/messages.service';

export interface Evenement {
  uuid: string;
  title: string;
  description: string;
  created_at: string;
  closed: boolean;
  user_roles: Participant[];
  messages: Message[];
  filters: Filters;
}

export interface Filters {
  typeEtablissement: string;
  auteur: string;
  type: string;
  fromDatetime: string;
  toDatetime: string;
} 

export interface EvenementsHTTP {
  data: Evenement[];
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class EvenementsService {

  private readonly _evenements = new BehaviorSubject<Evenement[]>([]);
  evenementsUrl: string;
  selectedEvenement = new BehaviorSubject<Evenement>({
    uuid: '',
    title: '',
    description: '',
    created_at: '',
    closed: false,
    user_roles: [],
    messages: [],
    filters: {
      typeEtablissement: '',
      auteur: '',
      type: '',
      fromDatetime: '',
      toDatetime: '',
    }
  });
  httpOptions: object;
  constructor(
    private http: HttpClient,
    private interventionsService: InterventionsService,
    // private messagesService: MessagesService
    ) {
      this.evenementsUrl = `${environment.backendUrl}/events`
      this.httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      }
  }

  getEvenements(): Evenement[] {
    return this._evenements.getValue();
  }

  private _setEvenements(evenements: Evenement[]): void {
    this._evenements.next(evenements)
  }

  private _addEvenement(evenementToAdd: Evenement): void {
    let evenements = this.getEvenements()
    // if it already exist, then update it
    if (evenements.some(event => event.uuid === evenementToAdd.uuid)) {
      evenements.map(evenement => {
        return evenement.uuid === evenement.uuid ? evenement = evenementToAdd : evenement
      })
    } {
      // if it doesn't exist, just add it
      evenements = evenements.concat(evenementToAdd)
    }
    this._setEvenements(evenements)
  }

  setMessages(evenement_id: string, messages: Message[]): void {
    let events = this.getEvenements() // Evenement[]
    events.map(event => {
      return event.uuid === evenement_id ? event.messages = messages : event
    })
    this._setEvenements(events)
  }

  getEvenementsByHTTP(): Observable<Evenement[]> {
    return this.http.get<EvenementsHTTP>(`${environment.backendUrl}/users/me/events`)
      .pipe(
        map(
          response => {
            const evenementsList = response.data.map((event: Evenement) => {
              return {
                uuid: event.uuid,
                title: event.title,
                description: event.description,
                created_at: event.created_at,
                closed: event.closed,
                user_roles: event.user_roles,
                messages: []
              }
            });
            this._setEvenements(evenementsList);
            return evenementsList;
          }
        )
      )
  }

  getEvenement(uuid: string): Observable<Evenement> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(response => {
          this._addEvenement(response.data)
          return response.data
        })
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

  callMainCouranteData(): Observable<any> {
    return this.http.get<any>(
        `${environment.backendUrl}/events/${this.selectedEvenement.getValue().uuid}/export?format=csv`,
        { responseType: "arraybuffer" as "json" }
      ).pipe(
      map((file: ArrayBuffer) => {
        return file;
      })
    )
  }

  downloadFile(): void {
    this.callMainCouranteData().subscribe(data => {
      const a = document.createElement("a");
      a.style.display = "none";
      document.body.appendChild(a);
    
      // Set the HREF to a Blob representation of the data to be downloaded
      a.href = window.URL.createObjectURL(
        new Blob([data], { type: 'text/csv;charset=utf-8;' })
      );
    
      // Use download attribute to set set desired file name
      a.setAttribute("download", `${this.selectedEvenement.getValue().uuid}-${(new Date()).toISOString()}`);
    
      // Trigger the download by simulating click
      a.click();
    
      // Cleanup
      window.URL.revokeObjectURL(a.href);
      document.body.removeChild(a);
    })
  }

  closeEvenement(uuid: string): Observable<any> {
    return this.http.put<any>(`${environment.backendUrl}/events/${uuid}/close`, {})
  }

  httpCreateMeeting(): Observable<any> {
    return this.http.post<any>(`${environment.backendUrl}/events/${this.selectedEvenement.getValue().uuid}/meeting`, {
      evenement_id: this.selectedEvenement.getValue().uuid
    }).pipe(
      pluck(HTTP_DATA)
    )
  }
  joinMeeting(meetingUUID: string): void {
    this.httpJoinMeeting(meetingUUID).subscribe(res => {
      window.open(res.direct_uri, '_blank')
    })
  }
  httpJoinMeeting(meetingUUID: string): Observable<any> {
    return this.http.get<any>(`${environment.backendUrl}/events/${this.selectedEvenement.getValue().uuid}/meeting/${meetingUUID}/join`).pipe(
      pluck(HTTP_DATA)
    )
  }
}
