import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EvenementsService } from '../../evenements.service';
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
  constructor(
    private messagesService: MessagesService,
    private evenementsService: EvenementsService
    ) {
    this.messages = []
    this.uuid = this.evenementsService.selectedEvenement.uuid
  }

  ngOnInit(): void {
    this.messagesService.getMessages(this.uuid).subscribe(messages => {
      this.messages = messages.sort((a, b) => {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      })
      this.fetchedMessages = true
    })
  }

}
