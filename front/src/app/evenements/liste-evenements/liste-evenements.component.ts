import { Component, OnInit } from '@angular/core';
import { EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-liste-evenements',
  templateUrl: './liste-evenements.component.html',
  styleUrls: ['./liste-evenements.component.scss']
})
export class ListeEvenementsComponent implements OnInit {

  constructor(
    public evenementsService: EvenementsService
  ) {
    this.evenementsService.getEvenements().subscribe(response => {
      this.evenementsService.evenements = response
    })
  }

  ngOnInit(): void {
  }

}
