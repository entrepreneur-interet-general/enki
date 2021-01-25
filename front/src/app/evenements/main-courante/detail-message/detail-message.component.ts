import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Message, MessagesService } from '../messages.service';

@Component({
  selector: 'app-detail-message',
  templateUrl: './detail-message.component.html',
  styleUrls: ['./detail-message.component.scss']
})
export class DetailMessageComponent implements OnInit {

  messageUUID: string;
  message: Message;

  constructor(
    private messagesService: MessagesService,
    private route: ActivatedRoute
  ) {
    this.message = {
      title: '',
      description: '',
      created_at: '',
      uuid: '',
      tags: [],
      resources: [],
      evenement_id: ''
    }
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.messageUUID = params['uuid']
      this.messagesService.getMessageByID(this.messageUUID).subscribe(message => {
        this.message = message
      })
    })
    
  }

}
