import { Component, OnInit } from '@angular/core';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-liste-evenements',
  templateUrl: './liste-evenements.component.html',
  styleUrls: ['./liste-evenements.component.scss']
})
export class ListeEvenementsComponent implements OnInit {

  evenements: Evenement[]
  constructor(
    private evenementsService: EvenementsService,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.evenementsService.getEvenementsByHTTP().subscribe(evenements => {
      this.evenements = evenements
    })
  }

  ngOnInit(): void {
  }

}
