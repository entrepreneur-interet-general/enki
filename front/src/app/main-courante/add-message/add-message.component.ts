import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MessagesService } from '../messages.service';
import { LabelsService } from '../labels.service';

@Component({
  selector: 'app-add-message',
  templateUrl: './add-message.component.html',
  styleUrls: ['./add-message.component.scss']
})
export class AddMessageComponent implements OnInit {
  messageGroup = new FormGroup({
    title: new FormControl('', Validators.required),
    content: new FormControl('', Validators.required)
  })
  constructor(
    private messagesService: MessagesService,
    public labelsService: LabelsService,
    private router: Router
  ) { }
  

  onSubmit(): void {
    let selectedLabelsUUID = this.labelsService.selectedLabels.map(label => label.uuid)
    this.messagesService.addMessage(this.messageGroup.value.title, this.messageGroup.value.content, selectedLabelsUUID).subscribe(response => {
      this.router.navigate(['maincourante'])
      this.labelsService.selectedLabels = [];
    })
  }

  ngOnInit(): void {
  }

}
