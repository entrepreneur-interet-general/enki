import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-detail-evenement',
  templateUrl: './detail-evenement.component.html',
  styleUrls: ['./detail-evenement.component.scss']
})
export class DetailEvenementComponent implements OnInit {
  uuid: string;
  evenement: Evenement;

  constructor(
    private route: ActivatedRoute,
    public mobilePrototype: MobilePrototypeService
  ) { }

  ngOnInit(): void {
    this.route.data.subscribe((data: { event: Evenement }) => {
      this.evenement = data.event;
      this.uuid = data.event.uuid;
    });
  }

  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
