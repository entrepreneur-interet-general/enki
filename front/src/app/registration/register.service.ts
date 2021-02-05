import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { Location } from '../interfaces/Location';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  selectedLocation = new BehaviorSubject<Location>({
    slug: '',
    label: ''
  });

  mockLocations: Location[] = [
    {
      slug: '77108',
      label: 'Chelles'
    },
    {
      slug: '51571',
      label: 'Val de Vesle'
    },
    {
      slug: '77',
      label: 'Seine et Marne'
    }
  ];

  constructor(
    private http: HttpClient,
  ) {
    
  }

  setSelectedLocation(location: Location): void {
    this.selectedLocation.next(location)
  }

  searchLocation(query): Observable<Location[]> {
    // return of(this.mockLocations as Location[])
    return this.http.get<any>(`${environment.backendUrl}/groups/locations?query=${query}`)
      .pipe(
        map(res => res.data)
      )
  }


  getUserTypes(): Observable<[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups/types`)
      .pipe(
        map(res => res.data)
      )
  }

  getUserPositions(groupeTypeName: string): Observable<object[]> {
    // return of([
    //   {
    //     name: 'prefet',
    //     label: 'Préfet'
    //   }
    // ])
    return this.http.get<any>(`${environment.backendUrl}/groups/positions?groupType=${groupeTypeName}`)
      .pipe(
        map(res => res.data)
      )
  }

}
