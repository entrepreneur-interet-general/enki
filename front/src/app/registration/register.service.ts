import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {


  selectedLocation;

  mockLocations: object[] = [
    {
      name: '77108',
      label: 'Chelles'
    },
    {
      name: '51571',
      label: 'Val de Vesle'
    },
    {
      name: '77',
      label: 'Seine et Marne'
    }
  ];

  constructor(
    private http: HttpClient,
  ) {
    this.selectedLocation = {
      name: '',
      label: ''
    }
  }

  searchLocation(query): Observable<object[]> {
    return of(this.mockLocations)
  }


  getUserTypes(): Observable<[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups/types`)
      .pipe(
        map(res => res.data)
      )
  }

  getUserPositions(groupeTypeName: string): Observable<object[]> {
    return of([
      {
        name: 'prefet',
        label: 'Préfet'
      }
    ])
    // return this.http.get<any>(`${environment.backendUrl}/positions/${groupeTypeName}`)
  }

}
