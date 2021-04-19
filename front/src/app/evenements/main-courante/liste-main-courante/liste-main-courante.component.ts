import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { User } from 'src/app/interfaces/User';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { ModalComponent } from 'src/app/ui/modal/modal.component';
import { UserService } from 'src/app/user/user.service';
import { EvenementsService, Filter } from '../../evenements.service';
import { Message, MessagesService } from '../messages.service';



@Component({
  selector: 'app-liste-main-courante',
  templateUrl: './liste-main-courante.component.html',
  styleUrls: ['./liste-main-courante.component.scss']
})
export class ListeMainCouranteComponent implements OnInit {

  messages: Array<Message>;
  uuid: string;
  fetchedMessages: boolean;
  user: User;
  currentEventFilter: Filter;
  exportType = new FormControl('csv');
  messages$: Observable<Message[]>;
  subscription: any;

  @ViewChild(ModalComponent) modal: ModalComponent;

  constructor(
    private messagesService: MessagesService,
    private evenementsService: EvenementsService,
    private userService: UserService,
    private router: Router,
    public mobilePrototype: MobilePrototypeService,
    private route: ActivatedRoute,
    ) {
      this.messages = []
      this.uuid = this.evenementsService.selectedEvenementUUID.getValue()
    const event = this.evenementsService.getEvenementByID(this.uuid)
    this.currentEventFilter = event.filter
    this.user = this.userService.user
  }

  ngOnInit(): void {
    const timer$ = timer(0, 3000);
    this.messages$ = timer$.pipe(
      switchMap(() => this.messagesService.getMessagesByEvenementID(this.uuid))
    )
    this.subscription = this.messages$.subscribe((messages) => {
      this.evenementsService.setMessages(this.uuid, this.messages);
      this.fetchedMessages = true;
      this.messages = messages.sort((a, b) => {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      });
    })
  }
  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
  openModal(): void {
    this.modal.open()
  }
  exportMainCourante(): void {
    this.evenementsService.getMainCouranteData().subscribe(data => {
      const a = document.createElement("a");
      a.style.display = "none";
      document.body.appendChild(a);
    
      // Set the HREF to a Blob representation of the data to be downloaded
      a.href = window.URL.createObjectURL(
        new Blob([data], { type: 'text/csv;charset=utf-8;' })
      );
    
      // Use download attribute to set set desired file name
      a.setAttribute("download", `${this.evenementsService.selectedEvenementUUID.getValue()}-${(new Date()).toISOString()}.csv`);
    
      // Trigger the download by simulating click
      a.click();
    
      // Cleanup
      this.modal.close()
      window.URL.revokeObjectURL(a.href);
      document.body.removeChild(a);
    });
  }

  clickOnMessage(message: Message): void {
    // routerLink="../detailmessage/{{message.uuid}}"
    if (message.type === 'meeting') {
      // TODO
      // replace window.open by calling joinMeeting in evenementsService and passing meetingID...
      window.open(message.description, '_blank')
    } else {
      this.router.navigate([`../message/${message.uuid}`], { relativeTo: this.route })
    }
  }

}
