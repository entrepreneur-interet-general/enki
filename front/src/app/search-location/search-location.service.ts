import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Location } from '../interfaces/Location';

@Injectable({
  providedIn: 'root'
})
export class SearchLocationService {

  selectedEtablissement = new BehaviorSubject<Location>({
    slug: '',
    label: '',
    uuid: ''
  });
  constructor() { }

  setSelectedLocation(location: Location): void {
    this.selectedEtablissement.next(location)
  }
}
