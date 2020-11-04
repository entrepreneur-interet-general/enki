import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Affaire, AffairesService } from '../../affaires.service'

@Component({
  selector: 'fronts-detail-intervention',
  templateUrl: './detail-intervention.component.html',
  styleUrls: ['./detail-intervention.component.scss']
})
export class DetailInterventionComponent implements OnInit {
  affaire;
  fetchedAffaire;
  constructor(private affairesService: AffairesService) { }

  ngOnInit(): void {
    this.affairesService.getAffaire().subscribe((affaire) => {
      this.affaire = affaire;
      this.fetchedAffaire = true;
    })
  }

  getIntervention(): Observable<Affaire> {
    return of(this.affaire)
  }

}
