import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import data from '../../data/interventionsx10.json'

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const interventions = data.affairs;
    return { interventions };
  }
  genId(interventions: any): number {
    return interventions.length > 0 ? Math.max(...interventions.map(inter => inter.id)) + 1 : 11;
  }
}