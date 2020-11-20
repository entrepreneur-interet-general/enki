import { Component, OnInit } from '@angular/core';
import { InterventionsService } from '../interventions/interventions.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [
    './dashboard.component.scss',
    '../interventions/liste/liste-interventions.component.scss'
  ]
})
export class DashboardComponent implements OnInit {

  interventions;
  constructor(
    private interventionsService: InterventionsService,
  ) {
    this.interventionsService.httpGetAllInterventions().subscribe((interventions) => {
      this.interventions = interventions;
    });
  }

  ngOnInit(): void {
  }

}
