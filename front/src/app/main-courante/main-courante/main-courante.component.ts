import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Message, MessagesService } from '../messages.service';

@Component({
  selector: 'app-main-courante',
  templateUrl: './main-courante.component.html',
  styleUrls: ['./main-courante.component.scss']
})
export class MainCouranteComponent implements OnInit {
  messages: Array<Message>;
  uuid: string;
  fetchedMessages: boolean;
  constructor(
    private messagesService: MessagesService,
    private route: ActivatedRoute
    ) {
    this.messages = []
    /* messagesService.getMessages().subscribe(messages => {
      this.messages = messages
    }) */
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      this.messagesService.getMessages(this.uuid).subscribe(messages => {
        this.messages = messages
        this.fetchedMessages = true
      })
    })
  }

}
