import { Component, OnInit } from '@angular/core';
import { MessagesService } from '../messages.service';

@Component({
  selector: 'app-main-courante',
  templateUrl: './main-courante.component.html',
  styleUrls: ['./main-courante.component.scss']
})
export class MainCouranteComponent implements OnInit {
  messages;
  constructor(messagesService: MessagesService) {
    this.messages = messagesService.getMessages();
    window.sessionStorage.setItem('messages', JSON.stringify(this.messages))
  }

  ngOnInit(): void {
  }

}
