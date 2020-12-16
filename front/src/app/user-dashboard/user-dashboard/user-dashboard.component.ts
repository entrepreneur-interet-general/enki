import { Component, OnInit } from '@angular/core';
import { InterventionsService } from '../../interventions/interventions.service';

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: [
    './user-dashboard.component.scss',
    '../../interventions/liste/liste-interventions.component.scss'
  ]
})
export class UserDashboardComponent implements OnInit {

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
