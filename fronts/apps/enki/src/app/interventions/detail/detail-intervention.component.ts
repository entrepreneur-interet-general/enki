import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Affaire, AffairesService } from '../../affaires.service'
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';

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
    private route: ActivatedRoute
    ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      this.affairesService.getAffaire(this.uuid).subscribe((affaire) => {
        this.affaire = affaire;
        this.fetchedAffaire = true;
      });
      
    });
  }

  getIntervention(): Observable<Affaire> {
    return of(this.affaire)
  }

}
