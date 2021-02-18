import { catchError, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';
import { uuidv4 } from '../../utilities';

export interface Message {
  title: string;
  description: string;
  created_at: string;
  uuid: string;
  tags: [];
  resources: [];
  evenement_id: string;
}


@Injectable({
  providedIn: 'root'
})

export class MessagesService {
  messagesUrl: string;
  resourcesUrl: string;
  private readonly _messagesSource = new BehaviorSubject<Message[]>([]);

  httpHeaders: object;
  constructor(
    private http: HttpClient,
  ) {
    this.resourcesUrl = `${environment.backendUrl}/resources`
    this.messagesUrl = `${environment.backendUrl}/messages`

    this.httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    }
  }

  getMessages(): Message[] {
    return this._messagesSource.getValue();
  }

  private _setMessages(messages: Message[]): void {
    this._messagesSource.next(messages)
  }

  private addMessages(messages: Message[]): void {
    const messagesConcat = [...this.getMessages(), ...messages]
    this._setMessages(messagesConcat)
  }

  private containsEvenementMessages(evenementUUID: string): boolean {
    return this.getMessages().some(message => message.evenement_id === evenementUUID)
  }

  getMessagesByEvenementID(evenementUUID: string): Observable<Message[]> {
    const messages = this.getMessages().filter(message => message.evenement_id === evenementUUID)
    return this.containsEvenementMessages(evenementUUID) ? of(messages) : this.httpGetMessages(evenementUUID)
  }

  httpGetMessages(evenementUUID: string): Observable<Message[]> {
    return this.http.get<any>(`${this.messagesUrl}`, { params: { "evenement_id": evenementUUID }})
      .pipe(
        map(messages => {
          if (!this.containsEvenementMessages(evenementUUID)) {
            this.addMessages(messages.data)
          }
          return messages.data
        })
      )
  }

  getMessageByID(messageUUID: string): Observable<Message> {
    const message = this.getMessages().filter(message => message.uuid === messageUUID)
    return message.length > 0 ? of(message[0]) : this.httpGetMessageByID(messageUUID)
  }

  httpGetMessageByID(messageUUID: string): Observable<Message> {
    return this.http.get<any>(`${this.messagesUrl}/${messageUUID}`)
      .pipe(
        map(response => {
          return response.data
        })
      )
  }

  httpSubmitMessage(title, description, selectedLabels, event_id, resources) : Observable<Message> {
    let uuid = uuidv4()
    let message = {
      "title":title,
      "description": description,
      "uuid": uuid,
      "tags": selectedLabels,
      "evenement_id": event_id,
      "resources": resources
    }
    return this.http.post<any>(this.messagesUrl, message, this.httpHeaders)
      .pipe(
        map(message => {
          this.addMessages([message.data])
          return message.data
        })
      )
  }

  addRessourceToMessage(mediaUUIDs, messageUUID): Observable<any> {
    return this.http.put<any>(`${this.messagesUrl}/${messageUUID}/resource/add`, {
        resource_ids: mediaUUIDs
    })
  }

  getUrlFileUpload(file: any): Observable<any> {
    let formBody = {
      "content_type": file.type,
      "original_name": file.name
    }
    return this.http.post<any>(`${this.resourcesUrl}`, formBody)
  }

  getUrlFileDownload(uuid: string): Observable<any> {
    return this.http.get<any>(`${this.resourcesUrl}/${uuid}`)
  }
  removeFileFromServer(resourceUUID: string): Observable<any> {
    return this.http.delete<any>(`${this.resourcesUrl}/${resourceUUID}`)
  }
  putFileOnServer(file, url): Observable<any> {
    const httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  file.type
      })
    }
    return this.http.put<any>(url, file, httpHeaders)
      .pipe(
        catchError((error) => {
          if (error.error instanceof ErrorEvent) {
            // A client-side or network error occurred. Handle it accordingly.
            console.error('An error occurred:', error.error.message);
          } else {
            // The backend returned an unsuccessful response code.
            // The response body may contain clues as to what went wrong.
            console.error(
              `Backend returned code ${error.status}, ` +
              `body was: ${error.error}`);
          }
          return throwError(
            'Something really bad happend'
          )
        })
      )
  }


}
