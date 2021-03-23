import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as L from 'leaflet';
import { BehaviorSubject } from 'rxjs';

import { Intervention } from 'src/app/interventions/interventions.service';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-summary-evenement',
  templateUrl: './summary-evenement.component.html',
  styleUrls: ['./summary-evenement.component.scss']
})
export class SummaryEvenementComponent implements OnInit {
  map;
  icon;
  evenementUUID: string;
  evenement: Evenement;
  interventions = new BehaviorSubject<Intervention[]>([]);
  uuid;

  constructor(
    private evenementsService: EvenementsService,
    private router: Router
  ) {
    this.evenementUUID = this.evenementsService.selectedEvenementUUID.getValue()
    this.evenementsService.getEvenementByID(this.evenementUUID).subscribe(evenement => {
      this.evenement = evenement;
    })
  }

  getInterventions(): Intervention[] {
    return this.interventions.getValue();
  }
  ngOnInit(): void {
    this.interventions.subscribe((interventions) => {
      if (interventions.length > 0) {
        this.initMap()
      }
    })
  }
  private initMap(): void {
    this.icon = L.icon({
      iconUrl: 'assets/marker-icon-2x.png',
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    })
    this.map = L.map('map', {
      center: [ 39, -98 ],
      zoom: 10
    })
    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);
    this.map.panTo([this.getInterventions()[0].coord.lat, this.getInterventions()[0].coord.long])
    // const marker = L.marker([affaires[0].location.lat, affaires[0].location.lon], {icon: this.icon}).addTo(this.map);
    
    this.interventions.getValue().forEach(inter => {
      L.marker([inter.coord.lat, inter.coord.long], {icon: this.icon}).addTo(this.map);
    })
  }



  ngAfterViewInit(): void {
    this.evenementsService.getSignalementsForEvenement(this.evenement.uuid).subscribe(response => {
      this.interventions.next(response)
    })
  }

  closeEvenement(): void {
    this.evenementsService.closeEvenement(this.evenement.uuid).subscribe((res) => {
      this.router.navigate(['/evenements'])
    })
  }

}
