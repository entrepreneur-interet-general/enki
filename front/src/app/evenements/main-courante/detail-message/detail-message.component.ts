import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessagesService } from '../messages.service';

@Component({
  selector: 'app-detail-message',
  templateUrl: './detail-message.component.html',
  styleUrls: ['./detail-message.component.scss']
})
export class DetailMessageComponent implements OnInit {

  messageUUID: string;

  constructor(
    private messagesService: MessagesService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.messageUUID = params['uuid']
    })
    
  }

}
