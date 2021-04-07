import { Component, OnInit } from '@angular/core';
import { AffairesService } from '../../affaires/affaires.service';
import { UserService } from '../../user/user.service'

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: [
    './user-dashboard.component.scss'
  ]
})
export class UserDashboardComponent implements OnInit {

  affaires;
  user;
  constructor(
    private interventionsService: AffairesService,
    private userService: UserService,
    ) {
    this.affaires = []
    this.interventionsService.httpGetAllAffaires().subscribe((affaires) => {
      this.affaires = affaires;
    });
    this.user = this.userService.user
  }

  ngOnInit(): void {
    
  }

  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
