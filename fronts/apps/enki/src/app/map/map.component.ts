import { Component, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { AppComponent } from '../app.component'

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  map;
  icon;

  constructor(private appComponent: AppComponent) { }

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
  }

  ngAfterViewInit(): void {
    this.initMap()
    this.appComponent.getAffaire().subscribe((affaire) => {
      this.map.panTo([affaire.coord.lat, affaire.coord.long])
      // const marker = L.marker([affaires[0].location.lat, affaires[0].location.lon], {icon: this.icon}).addTo(this.map);
      L.marker([affaire.coord.lat, affaire.coord.long], {icon: this.icon}).addTo(this.map);
      
    })
  }

  ngOnInit(): void {
  }

}
