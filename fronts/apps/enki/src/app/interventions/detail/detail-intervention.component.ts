import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Affaire, AffairesService } from '../../affaires.service'
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'fronts-detail-intervention',
  templateUrl: './detail-intervention.component.html',
  styleUrls: ['./detail-intervention.component.scss']
})
export class DetailInterventionComponent implements OnInit {
  affaire;
  fetchedAffaire;
  uuid;
  constructor(
    private affairesService: AffairesService,
    private route: ActivatedRoute,
    ) { }

  ngOnInit(): void {
    this.affairesService.getAffaire().subscribe((affaire) => {
      this.affaire = affaire;
      this.fetchedAffaire = true;
    })
    this.route.queryParams.subscribe(params => {
      this.uuid = params['uuid'];
    });
  }

  getIntervention(): Observable<Affaire> {
    return of(this.affaire)
  }

}
