import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, Subject, throwError } from 'rxjs';
import { Location } from '../interfaces/Location';
import { catchError, map, pluck, retry } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HTTP_DATA } from '../constants';
import { group } from '@angular/animations';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  selectedLocation = new BehaviorSubject<Location>({
    slug: '',
    label: '',
    uuid: '',
    location: {
      external_id: ''
    },
  });

  selectedGroupType = new BehaviorSubject<string>('');

  token: string;

  constructor(
    private http: HttpClient,
  ) {
    this.token = '';
  }

  setSelectedLocation(location: Location): void {
    this.selectedLocation.next(location)
  }

  setGroupType(groupType: string): void {
    this.selectedGroupType.next(groupType)
  }

  searchLocation(query: string, groupType: string): Observable<Location[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups?groupType=${groupType}&query=${query}`).pipe(
      pluck(HTTP_DATA),
      catchError((error) => {
        if (error.status === 404) {
          return of([])
        } else {
          console.error(error)
          return throwError(
            'Something bad happened; please try again later.');
        }
      })
    )
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
