import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, pluck } from 'rxjs/operators';
import { Intervention, InterventionsService } from '../interventions/interventions.service';
import { Location } from '../interfaces/Location';
import { Participant } from '../interfaces/Participant';
import { HTTP_DATA } from '../constants';
import { Message } from './main-courante/messages.service';

export enum EvenementType {
  INCENDIE = "incendie",
  INONDATION = "inondation",
  ATTENTAT = "attentat"
}

export enum EvenementStatus {
  ongoing = "En cours",
  tobegoing = "À venir",
  over = "Terminé"
};
export interface Evenement {
  uuid: string;
  title: string;
  creator: {
    position: {
      group: {
        label: string;
      }
    }
  };
  location_id: string;
  started_at: string;
  ended_at: string;
  description: string;
  created_at: string;
  closed: boolean;
  user_roles: Participant[];
  messages: Message[];
  filter: Filter;
  status: EvenementStatus;
}

export interface Filter {
  etablissement: string;
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

  readonly _evenements = new BehaviorSubject<Evenement[]>([]);
  evenementsUrl: string;
  selectedEvenementUUID = new BehaviorSubject<string>('');
  selectedEvenementParticipants = new BehaviorSubject<Participant[]>([]);
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


  addOrUpdateEvenement(evenementToAdd: Evenement): void {
    let evenements: Evenement[] = this.getEvenements()
    evenementToAdd.filter = {
      etablissement: '',
      auteur: '',
      type: '',
      fromDatetime: '',
      toDatetime: '',
    };
    // if it already exist, then update it
    if (evenements.some(event => event.uuid === evenementToAdd.uuid)) {
      evenements.map(evenement => {
        return evenementToAdd.uuid === evenement.uuid ? evenementToAdd : evenement
      })
    } {
      // if it doesn't exist, just add it
      evenements = evenements.concat(evenementToAdd)
    }
    this._setEvenements(evenements)
  }

  updateEvenementFilter(evenement_id: string, filter: Filter): Observable<Filter> {
    let evenementToFilter = this.getEvenements().filter(evenement => evenement.uuid === evenement_id)
    evenementToFilter[0].filter = filter
    this.addOrUpdateEvenement(evenementToFilter[0])
    return of(filter)
  }

  setMessages(evenement_id: string, messages: Message[]): void {
    let events = this.getEvenements()
    events.map(event => {
      return event.uuid === evenement_id ? event.messages = messages : event
    })
    this._setEvenements(events)
  }

  checkStatus(event: Evenement): EvenementStatus {
    if (event.ended_at) {
      return EvenementStatus.over;
    }
    return new Date(event.started_at) < new Date() ? EvenementStatus.ongoing : EvenementStatus.tobegoing
  }

  getEvenementLocationPolygon(location_id: string): Observable<Location> {
    return this.http.get<any>(`${environment.backendUrl}/locations/${location_id}`)
      .pipe(
        pluck(HTTP_DATA)
      )
  }

  getEvenementsByHTTP(): Observable<Evenement[]> {
    return this.http.get<EvenementsHTTP>(`${environment.backendUrl}/users/me/events`)
      .pipe(
        map(
          response => {
            const evenementsList = response.data.map((event: Evenement) => {
              const currentStatus = this.checkStatus(event);
              return {
                uuid: event.uuid,
                title: event.title,
                description: event.description,
                created_at: event.created_at,
                closed: event.closed,
                started_at: event.started_at,
                ended_at: event.ended_at,
                user_roles: event.user_roles,
                location_id: event.location_id,
                messages: [],
                creator: {
                  position: {
                    group: {
                      label: event.creator.position.group.label
                    }
                  }
                },
                filter: {
                  etablissement: '',
                  auteur: '',
                  type: '',
                  fromDatetime: '',
                  toDatetime: '',
                },
                status: currentStatus
              }
            });
            this._setEvenements(evenementsList);
            return evenementsList;
          }
        )
      )
  }
  getSelectedEvenementsParticipants(): Participant[] {
    return this.selectedEvenementParticipants.getValue();
  }
  getEvenementByID(uuid: string): Observable<Evenement> {
    return this.evenementIsInMemory ? of(this.getEvenements().filter(evenement => evenement.uuid === uuid)[0]) : this.httpGetEvenementById(uuid)
  }
  private evenementIsInMemory(evenementUUID: string): boolean {
    return this.getEvenements().some(evenement => evenement.uuid === evenementUUID)
  }
  httpGetEvenementById(uuid: string): Observable<Evenement> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(response => {
          let event: Evenement = response.data as Evenement
          event.filter = {
            etablissement: '',
            auteur: '',
            type: '',
            fromDatetime: '',
            toDatetime: '',
          } 
          this.addOrUpdateEvenement(event)
          return event
        })
      )
  }
  addParticipantsToEvenement(participant: Participant): void {
    this.getEvenementByID(this.selectedEvenementUUID.getValue()).subscribe(evenement => {
      const copyEvent = evenement;
      copyEvent.user_roles = copyEvent.user_roles.concat(participant);
      this.addOrUpdateEvenement(copyEvent);
    })
  }
  changeParticipantRole(participant: Participant): void {
    this.getEvenementByID(this.selectedEvenementUUID.getValue()).subscribe(evenement => {
      const copyEvent = evenement;
      // Replace the right participant by the received one
      const newUserRoles = copyEvent.user_roles.map(user_role => {
        if (user_role.user.uuid === participant.user.uuid) {
          return participant
        } else {
          return user_role
        }
      });
      copyEvent.user_roles = newUserRoles;
      this.addOrUpdateEvenement(copyEvent);
    })

  }
  selectEvenement(event: Evenement): void {
    this.selectedEvenementUUID.next(event.uuid);
    this.selectedEvenementParticipants.next(event.user_roles);
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
        `${environment.backendUrl}/events/${this.selectedEvenementUUID.getValue()}/export?format=csv`,
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
      a.setAttribute("download", `${this.selectedEvenementUUID.getValue()}-${(new Date()).toISOString()}`);
    
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
    return this.http.post<any>(`${environment.backendUrl}/events/${this.selectedEvenementUUID.getValue()}/meeting`, {
      evenement_id: this.selectedEvenementUUID.getValue()
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
    return this.http.get<any>(`${environment.backendUrl}/events/${this.selectedEvenementUUID.getValue()}/meeting/${meetingUUID}/join`).pipe(
      pluck(HTTP_DATA)
    )
  }
}
