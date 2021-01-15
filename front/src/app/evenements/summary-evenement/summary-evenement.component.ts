import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as L from 'leaflet';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-summary-evenement',
  templateUrl: './summary-evenement.component.html',
  styleUrls: ['./summary-evenement.component.scss']
})
export class SummaryEvenementComponent implements OnInit {
  map;
  icon;
  evenement;
  uuid;

  constructor(
    private evenementsService: EvenementsService,
    private route: ActivatedRoute
  ) {
    // this.id = this.route.snapshot.paramMap.get('id');
    // this.evenement = this.evenementsService.evenements[0]
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: { event: Evenement }) => {
      this.evenement = data.event;
      this.uuid = data.event.uuid;
    });
  }
  initMap(): void {
    this.icon = L.icon({
      iconUrl: 'assets/marker-icon-2x.png',
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    })
    this.map = L.map('mapid', {
      center: [ 39, -98 ],
      zoom: 10
    })
    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

    this.map.panTo([48.886622, 2.598313])
      // const marker = L.marker([affaires[0].location.lat, affaires[0].location.lon], {icon: this.icon}).addTo(this.map);
      L.marker([48.886622, 2.598313], {icon: this.icon}).addTo(this.map);
  }
  ngAfterViewInit(): void {
    // this.initMap()
  }

}
