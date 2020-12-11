import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Intervention, InterventionsService } from '../interventions.service'
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'fronts-detail-intervention',
  templateUrl: './detail-intervention.component.html',
  styleUrls: ['./detail-intervention.component.scss']
})
export class DetailInterventionComponent implements OnInit {
  intervention;
  fetchedIntervention;
  uuid;
  constructor(
    private interventionsService: InterventionsService,
    private route: ActivatedRoute
    ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      if (this.interventionsService.getInterventionFromMemory(this.uuid)) {
        this.intervention = this.interventionsService.getInterventionFromMemory(this.uuid)
        this.fetchedIntervention = true
      } else {
        this.interventionsService.httpGetIntervention(this.uuid).subscribe((intervention) => {
          this.intervention = intervention
          this.fetchedIntervention = true;
        });
      }
    });
  }

  getIntervention(): Observable<Intervention> {
    return of(this.intervention)
  }

}