import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { InterventionsService } from '../../interventions/interventions.service';
import { UserService } from '../../user/user.service'

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: [
    './user-dashboard.component.scss'
  ]
})
export class UserDashboardComponent implements OnInit {

  interventions;
  user;
  constructor(
    private interventionsService: InterventionsService,
    private userService: UserService,
    private activatedRoute: ActivatedRoute
    ) {
    this.interventions = []
    this.interventionsService.httpGetAllInterventions().subscribe((interventions) => {
      this.interventions = interventions;
    });
    this.user = this.userService.user
  }

  ngOnInit(): void {
    
  }

  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
