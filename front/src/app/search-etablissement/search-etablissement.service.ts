import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Location } from '../interfaces/Location';

@Injectable({
  providedIn: 'root'
})
export class SearchEtablissementService {

  selectedEtablissement = new BehaviorSubject<Location>({
    slug: '',
    label: '',
    uuid: '',
    location: {
      external_id: ''
    },
  });
  constructor() { }

  setSelectedEtablissement(etablissement: Location): void {
    this.selectedEtablissement.next(etablissement)
  }
}
