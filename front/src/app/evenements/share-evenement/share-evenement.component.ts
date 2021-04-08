import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/interfaces/User';
import { Participant } from 'src/app/interfaces/Participant';
import { ModalComponent } from 'src/app/ui/modal/modal.component';
import { Evenement, EvenementsService } from '../evenements.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { HTTP_DATA } from 'src/app/constants/constants';
import { pluck } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';

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

  participants = new BehaviorSubject<Participant[]>([]);
  @ViewChild(ModalComponent)
  modal: ModalComponent;
  roleGroup = new FormGroup({
    role: new FormControl('view', Validators.required)
  })
  meetingUUID: string;
  // role = new FormControl('')

  selectedParticipant: Participant;
  roles: object;

  evenementSubscriber: any;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    public evenementsService: EvenementsService,
    private http: HttpClient,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.selectedParticipant = null;
    this.meetingUUID = null;

    this.evenementSubscriber = this.evenementsService._evenements.subscribe((events) => {
      const currentEvents: Evenement[] = events.filter(event => event.uuid === this.evenementsService.selectedEvenementUUID.getValue())
      this.participants.next(currentEvents[0].user_roles)
    })
    const event = this.evenementsService.getEvenementByID(this.evenementsService.selectedEvenementUUID.getValue())
    this.participants.next(event.user_roles)
    this.roles = ROLES;

    this.roleGroup.controls.role.valueChanges.subscribe((value: string) => {
      this.updateParticipantRole(value).subscribe((res: User) => {
        this.evenementsService.changeParticipantRole({
          user: res,
          type: value
        });
      });
    });

    this.getMeetingData().subscribe(res => {
      this.meetingUUID = res.data[0].uuid
    })
  }

  getMeetingData(): Observable<any> {
    return this.http.get<any>(
      `${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/meeting`
      )
  }

  ngOnInit(): void {
  }
  updateParticipantRole(value: string): Observable<User> {
    return this.http.put<any>(
      `${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/invite/${this.selectedParticipant.user.uuid}?role_type=${value}`, {}
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

  createMeeting(): void {
    this.evenementsService.httpCreateMeeting().subscribe(res => {
      this.meetingUUID = res.uuid
      this.joinMeeting();
    })
  }
  joinMeeting(): void {
    this.evenementsService.httpJoinMeeting(this.meetingUUID).subscribe(
      res => {
        window.open(res.direct_uri, '_blank')
      }
    )
  }

  ngOnDestroy(): void {
    this.evenementSubscriber.unsubscribe();
  }


  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }
}
