import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { Location } from '../interfaces/Location';
import { map, pluck } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HTTP_DATA } from '../constants';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  selectedLocation = new BehaviorSubject<Location>({
    slug: '',
    label: '',
    uuid: ''
  });

  mockLocations: Location[] = [
    {
      slug: '77108',
      label: 'Chelles',
      uuid: ''
    },
    {
      slug: '51571',
      label: 'Val de Vesle',
      uuid: ''
    },
    {
      slug: '77',
      label: 'Seine et Marne',
      uuid: ''
    }
  ];

  constructor(
    private http: HttpClient,
  ) {
    
  }

  setSelectedLocation(location: Location): void {
    this.selectedLocation.next(location)
  }

  searchLocation(query: string): Observable<Location[]> {
    // return of(this.mockLocations as Location[])
    return this.http.get<any>(`${environment.backendUrl}/groups/locations?query=${query}`).pipe(
      pluck(HTTP_DATA)
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
