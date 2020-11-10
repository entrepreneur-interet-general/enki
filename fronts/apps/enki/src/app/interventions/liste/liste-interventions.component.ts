import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Intervention, InterventionsService } from '../interventions.service'

@Component({
  selector: 'app-liste-interventions',
  templateUrl: './liste-interventions.component.html',
  styleUrls: ['./liste-interventions.component.scss']
})
export class ListeInterventionsComponent implements OnInit {
  interventions;
  constructor(
    private interventionsService: InterventionsService,
  ) {
    this.interventionsService.getAllInterventions().subscribe((interventions) => {
      this.interventions = interventions;
      // this.fetchedAffaire = true;
    });
  }

  ngOnInit(): void {
  }

}
