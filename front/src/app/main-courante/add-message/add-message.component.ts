import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
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
  uuid: string;
  constructor(
    private messagesService: MessagesService,
    public labelsService: LabelsService,
    private router: Router,
    private route: ActivatedRoute
  ) { }
  

  onSubmit(): void {
    let selectedLabelsUUID = this.labelsService.selectedLabels.map(label => label.uuid)
    this.messagesService.addMessage(this.messageGroup.value.title, this.messageGroup.value.content, selectedLabelsUUID, this.uuid).subscribe(response => {
      this.router.navigate([`maincourante/${this.uuid}`])
      this.labelsService.selectedLabels = [];
    })
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params.uuid
    })
  }

}
