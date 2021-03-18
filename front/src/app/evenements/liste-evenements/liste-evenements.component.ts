import { Component, OnInit } from '@angular/core';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-liste-evenements',
  templateUrl: './liste-evenements.component.html',
  styleUrls: ['./liste-evenements.component.scss']
})
export class ListeEvenementsComponent implements OnInit {

  constructor(
    public evenementsService: EvenementsService,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.evenementsService.getEvenements().subscribe(response => {
      this.evenementsService.evenements = response
    })
  }

  ngOnInit(): void {
  }

}
