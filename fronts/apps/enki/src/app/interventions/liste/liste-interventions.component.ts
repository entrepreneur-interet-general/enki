import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Affaire, AffairesService } from '../../affaires.service'

@Component({
  selector: 'app-liste-interventions',
  templateUrl: './liste-interventions.component.html',
  styleUrls: ['./liste-interventions.component.scss']
})
export class ListeInterventionsComponent implements OnInit {
  interventions;
  constructor(
    private affairesService: AffairesService,
  ) {
    this.affairesService.getAllInterventions().subscribe((affaire) => {
      this.interventions = affaire;
      // this.fetchedAffaire = true;
    });
  }

  ngOnInit(): void {
  }

}
