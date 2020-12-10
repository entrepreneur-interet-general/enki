import { Injectable } from '@angular/core';

export interface Message {
  title: string;
  content: string;
}

@Injectable({
  providedIn: 'root'
})

export class MessagesService {

  messages: Array<Message>;
  constructor() {
    this.messages = window.sessionStorage.getItem("messages") ? JSON.parse(window.sessionStorage.getItem("messages")) : [];
  }

  addMessage(title, content) : void {
    this.messages.push({
      title: title,
      content: content
    });
  }

  getMessages(): Array<Message> {
    return this.messages;
  }
}
