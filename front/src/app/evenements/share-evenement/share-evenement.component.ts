import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/interfaces/User';
import { EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-share-evenement',
  templateUrl: './share-evenement.component.html',
  styleUrls: ['./share-evenement.component.scss']
})
export class ShareEvenementComponent implements OnInit {

  // participants = new FormControl('', Validators.required)
  participants: User[];

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    public evenementsService: EvenementsService
  ) {
    this.participants = [];
    this.evenementsService.selectedEvenement.subscribe((event) => {
      this.participants = event.user_roles
    })
  }

  ngOnInit(): void {
  }

  goToSearchUser(): void {
    this.router.navigate(['./searchuser'], {relativeTo: this.activatedRoute})
  }

  mapUserRoleToLabel(type: string): string {
    switch (type) {
      case 'view':
        return 'Lecteur'
      case 'admin':
        return 'Administrateur'
      case 'write':
        return 'Éditeur'
      default:
        return 'Lecteur'
    }
  }

}
