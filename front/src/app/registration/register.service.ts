import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { pluck } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HTTP_DATA } from '../constants/constants';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  token: string;

  constructor(
    private http: HttpClient,
  ) {
    this.token = '';
  }

  getUserTypes(): Observable<[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups/types`)
      .pipe(
        pluck(HTTP_DATA)
      )
  }

  getUserPositions(groupeTypeName: string): Observable<object[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups/positions?groupType=${groupeTypeName}`)
      .pipe(
        pluck(HTTP_DATA)
      )
  }

}
