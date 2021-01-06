import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MessagesService } from '../messages.service';

@Component({
  selector: 'app-add-message',
  templateUrl: './add-message.component.html',
  styleUrls: ['./add-message.component.scss']
})
export class AddMessageComponent implements OnInit {
  messageGroup = new FormGroup({
    title: new FormControl('', Validators.required),
    content: new FormControl('', Validators.required),
    tag: new FormControl('')
  })
  constructor(
    private messagesService: MessagesService,
    private router: Router
  ) { }
  submitTag(): void {
    this.messagesService.addTag(this.messageGroup.value.tag).subscribe(tag => {
      console.log(tag)
      this.messagesService.tags.push(tag)
    })
  }

  onSubmit(): void {
    this.messagesService.addMessage(this.messageGroup.value.title, this.messageGroup.value.content).subscribe(response => {
      this.router.navigate(['maincourante'])
    })
  }

  ngOnInit(): void {
  }

}
