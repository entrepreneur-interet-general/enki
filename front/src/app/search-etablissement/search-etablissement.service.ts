import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Location } from '../interfaces/Location';
import { LOCATION_INIT } from '../constants/location_init';

@Injectable({
  providedIn: 'root'
})
export class SearchEtablissementService {

  selectedEtablissement = new BehaviorSubject<Location>(LOCATION_INIT);
  constructor() { }

  setSelectedEtablissement(etablissement: Location): void {
    this.selectedEtablissement.next(etablissement)
  }
}
