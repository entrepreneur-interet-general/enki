import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import data from '../../data/interventionsx10.json'
// import { Hero } from './hero';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const interventions = data.affairs;
    return { interventions };
  }

  // Overrides the genId method to ensure that an inter always has an id.
  // If the heroes array is empty,
  // the method below returns the initial number (11).
  // if the heroes array is not empty, the method below returns the highest
  // hero id + 1.
  genId(interventions: any): number {
    return interventions.length > 0 ? Math.max(...interventions.map(inter => inter.id)) + 1 : 11;
  }
}