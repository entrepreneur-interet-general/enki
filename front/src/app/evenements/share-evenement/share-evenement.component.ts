import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/interfaces/User';
import { Participant } from 'src/app/interfaces/Participant';
import { ModalComponent } from 'src/app/ui/modal/modal.component';
import { EvenementsService } from '../evenements.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { HTTP_DATA } from 'src/app/constants';
import { pluck } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

const ROLES = {
  admin: 'Administrateur',
  view: 'Lecteur',
  edit: 'Éditeur'
}

@Component({
  selector: 'app-share-evenement',
  templateUrl: './share-evenement.component.html',
  styleUrls: ['./share-evenement.component.scss'],
})
export class ShareEvenementComponent implements OnInit {

  participants: Participant[];
  @ViewChild(ModalComponent)
  modal: ModalComponent;
  roleGroup = new FormGroup({
    role: new FormControl('view', Validators.required)
  })
  // role = new FormControl('')

  selectedParticipant: Participant;
  roles: object;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    public evenementsService: EvenementsService,
    private http: HttpClient
  ) {
    this.participants = [];
    this.selectedParticipant = null;
    this.evenementsService.selectedEvenement.subscribe((event) => {
      this.participants = event.user_roles
    })
    this.roles = ROLES;

    this.roleGroup.controls.role.valueChanges.subscribe((value: string) => {
      this.updateParticipantRole(value).subscribe((res: User) => {
        this.evenementsService.changeParticipantRole({
          user: res,
          type: value
        });
      });
    });
  }

  ngOnInit(): void {
  }
  updateParticipantRole(value): Observable<User> {
    return this.http.put<any>(
      `${environment.backendUrl}/events/${this.evenementsService.selectedEvenement.getValue().uuid}/invite/${this.selectedParticipant.user.uuid}?role_type=${value}`, {}
      ).pipe(
      pluck(HTTP_DATA)
    )
  }
  showEditParticipantRights(participant): void {
    this.selectedParticipant = participant
    this.roleGroup.controls.role.setValue(participant.type)
    this.modal.open()
  }
  removeSelectedParticipant(closed: boolean): void {
    if (closed) {
      this.selectedParticipant = null;
    }
  }
  goToSearchUser(): void {
    this.router.navigate(['./searchuser'], {relativeTo: this.activatedRoute})
  }

  mapUserRoleToLabel(type: string): string {
    return ROLES[type];
  }

}
