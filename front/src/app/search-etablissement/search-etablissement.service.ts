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
    uuid: ''
  });
  constructor() { }

  setSelectedEtablissement(etablissement: Location): void {
    this.selectedEtablissement.next(etablissement)
  }
}
