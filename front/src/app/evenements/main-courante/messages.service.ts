import { catchError, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

export interface Message {
  title: string;
  description: string;
  created_at: string;
  uuid: string;
}


@Injectable({
  providedIn: 'root'
})

export class MessagesService {
  messagesUrl: string;
  messages: Array<Message>;
  resourcesUrl: string;
  
  httpHeaders: object;
  constructor(
    private http: HttpClient,
  ) {
    this.messages = window.sessionStorage.getItem("messages") ? JSON.parse(window.sessionStorage.getItem("messages")) : [];
    this.messagesUrl = 'http://localhost:5000/api/enki/v1/messages'
    this.resourcesUrl = 'http://localhost:5000/api/enki/v1/resources'

    this.httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    }
  }

  uuidv4(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }



  addMessage(title, description, selectedLabels, event_id) : Observable<Message> {
    let uuid = this.uuidv4()
    let message = {
      "title":title,
      "description": description,
      "uuid": uuid,
      "tags": selectedLabels,
      "evenement_id": event_id
    }
    return this.http.post<any>(this.messagesUrl, message, this.httpHeaders)
      .pipe(
        map(message => {
          return message.data
        })
      )
  }

  addRessourceToMessage(mediaUUID, messageUUID): Observable<any> {
    return this.http.put<any>(`${this.messagesUrl}/${messageUUID}/resource/${mediaUUID}`, {})
  }

  getMessages(uuid): Observable<Message[]> {
    // TODO: ajouter la route pour récupérer les messages en fonction du uuid de l'event
    return this.http.get<any>(`${this.messagesUrl}`, { params: { "evenement_id": uuid }})
      .pipe(
        map(messages => {
          return messages.data
        })
      )
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
