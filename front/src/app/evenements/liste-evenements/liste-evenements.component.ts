import { Component, OnInit } from '@angular/core';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Evenement, EvenementsService, Status } from '../evenements.service';

@Component({
  selector: 'app-liste-evenements',
  templateUrl: './liste-evenements.component.html',
  styleUrls: ['./liste-evenements.component.scss']
})
export class ListeEvenementsComponent implements OnInit {

  evenements: Evenement[];
  activeFilter: Status;
  public StatusEnum = Status;

  constructor(
    private evenementsService: EvenementsService,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.evenements = [];
    this.activeFilter = Status.ongoing;
    this.evenementsService.getEvenementsByHTTP().subscribe(evenements => {
      this.evenements = evenements
    })
  }

  setActiveFilter(status: Status): void {
    this.activeFilter = status;
  }

  ngOnInit(): void {
  }

}
