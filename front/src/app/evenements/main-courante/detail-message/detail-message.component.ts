import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Message, MessagesService } from '../messages.service';
import { MESSAGE_INIT } from '../../../constants/message_init';

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
    private route: ActivatedRoute,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.message = MESSAGE_INIT;
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
