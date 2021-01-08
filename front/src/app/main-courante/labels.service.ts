import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Label {
  title: string;
  uuid: string;
}

@Injectable({
  providedIn: 'root'
})
export class LabelsService {
  labels: Array<Label>;
  selectedLabels: Array<Label>;
  labelUrl: string;
  httpHeaders: object;
  constructor(
    private http: HttpClient,
  ) {
    this.labelUrl = 'http://localhost:5000/api/enki/v1/tags'
    this.labels = []
    this.selectedLabels = []
    this.httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    }
  }

  addLabel(title): Observable<Label> {
    let tag = {
      "title": title
    }
    return this.http.post<any>(this.labelUrl, tag, this.httpHeaders)
      .pipe(
        map(label => label.tag)
      )
  }
  getLabels(): Observable<Label[]> {
    return this.http.get<any>(this.labelUrl)
      .pipe(
        map(labels => {
          return labels.tags
        })
      )
  }
}
