import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as L from 'leaflet';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-detail-evenement',
  templateUrl: './detail-evenement.component.html',
  styleUrls: ['./detail-evenement.component.scss']
})
export class DetailEvenementComponent implements OnInit {
  uuid: string;
  evenement: Evenement;
  fetchedEvenement: boolean;
  map;
  icon;

  constructor(
    private route: ActivatedRoute,
    private evenementsService: EvenementsService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      this.evenementsService.getEvenement(this.uuid).subscribe((evenement) => {
        this.fetchedEvenement = true;
        this.evenement = evenement
      });
    })
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
    this.initMap()
  }

}
