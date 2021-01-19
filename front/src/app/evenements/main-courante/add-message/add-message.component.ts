import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MessagesService } from '../messages.service';
import { LabelsService } from '../labels.service';
import { EvenementsService } from '../../evenements.service';

@Component({
  selector: 'app-add-message',
  templateUrl: './add-message.component.html',
  styleUrls: ['./add-message.component.scss']
})
export class AddMessageComponent implements OnInit {
  messageGroup = new FormGroup({
    title: new FormControl('', Validators.required),
    content: new FormControl('', Validators.required),
    files: new FormControl('', Validators.required)
  })
  uuid: string;
  constructor(
    private messagesService: MessagesService,
    public labelsService: LabelsService,
    private evenementsService: EvenementsService,
    private router: Router,
    private route: ActivatedRoute
  ) { }
  

  onSubmit(): void {
    let selectedLabelsUUID = this.labelsService.selectedLabels.map(label => label.uuid)
    this.uuid = this.evenementsService.selectedEvenement.uuid
    this.messagesService.addMessage(this.messageGroup.value.title, this.messageGroup.value.content, selectedLabelsUUID, this.uuid).subscribe(response => {
      this.router.navigate([`..`], { relativeTo: this.route })
      this.labelsService.selectedLabels = [];
    })
  }

  uploadFile(event: any): void {
    console.log("ouuhh", (event.target as HTMLInputElement).files[0])
    const file = (event.target as HTMLInputElement).files[0]
    // this.messageGroup.get('files').setValue(file)
    // this.messageGroup.get('files').updateValueAndValidity()
    this.messagesService.getUrlFileUpload((event.target as HTMLInputElement).files[0]).subscribe(response => {
      console.log(response)
      // const formData = new FormData();
      // formData.append('file', this.messageGroup.get('files').value);
      this.messagesService.putFileOnServer(file, response.data.upload_url).subscribe(response => console.log('test'))
    })
  }

  ngOnDestroy(): void {
    this.labelsService.selectedLabels = []
  }

  ngOnInit(): void {
/*     this.route.params.subscribe(params => {
      this.uuid = params.uuid
    }) */
  }

}
