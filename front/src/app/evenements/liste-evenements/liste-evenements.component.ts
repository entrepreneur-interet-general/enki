import { Component, OnInit } from '@angular/core';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Evenement, EvenementsService, EvenementStatus } from '../evenements.service';

@Component({
  selector: 'app-liste-evenements',
  templateUrl: './liste-evenements.component.html',
  styleUrls: ['./liste-evenements.component.scss']
})
export class ListeEvenementsComponent implements OnInit {

  evenements: Evenement[];
  activeFilter: EvenementStatus;
  public StatusEnum = EvenementStatus;

  constructor(
    private evenementsService: EvenementsService,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.evenements = [];
    this.activeFilter = EvenementStatus.ongoing;
    this.evenementsService.getEvenementsByHTTP().subscribe(evenements => {
      this.evenements = evenements
    })
  }

  setActiveFilter(status: EvenementStatus): void {
    this.activeFilter = status;
  }

  ngOnInit(): void {
  }

}
