import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MessagesService } from '../messages.service';
import { LabelsService } from '../labels.service';
import { EvenementsService } from '../../evenements.service';

interface Media {
  uuid: string;
  url: string;
}
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
  evenementUUID: string;
  listOfMedias: Array<Media>;
  constructor(
    private messagesService: MessagesService,
    public labelsService: LabelsService,
    private evenementsService: EvenementsService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.listOfMedias = []
  }
  

  onSubmit(): void {
    let selectedLabelsUUID = this.labelsService.selectedLabels.map(label => label.uuid)
    this.evenementUUID = this.evenementsService.selectedEvenement.uuid
    this.messagesService.httpSubmitMessage(
        this.messageGroup.value.title,
        this.messageGroup.value.content,
        selectedLabelsUUID,
        this.evenementUUID,
        this.listOfMedias.map(media => media.uuid)
      ).subscribe(() => {

      /* if (this.listOfMedias.length > 0) {
        this.messagesService.addRessourceToMessage(this.listOfMedias.map(media => media.uuid), message.uuid)
          .subscribe(() => {
            this.router.navigate([`..`], { relativeTo: this.route })
          })
      } else { */
        this.router.navigate([`..`], { relativeTo: this.route })
      /* } */
    })
  }

  uploadFile(event: any): void {
    // TODO : montrer le loader
    const file = (event.target as HTMLInputElement).files[0]
    this.messagesService.getUrlFileUpload((event.target as HTMLInputElement).files[0]).subscribe(response => {
      this.messagesService.putFileOnServer(file, response.data.upload_url).subscribe(() => {
        // console.log('success, show image preview')
        // TODO : cacher le loader
        // montrer l'image de preview
        let mediaUUID = response.data.uuid
        this.messagesService.getUrlFileDownload(mediaUUID).subscribe(minioDataObj => {
          this.listOfMedias.push({uuid: mediaUUID, url: minioDataObj.data.url})
        })
      })
    })
  }

  removeMedia(mediaUUID: string): void {
    this.messagesService.removeFileFromServer(mediaUUID).subscribe(response => {
      if (response.message === 'success') {
        this.listOfMedias = this.listOfMedias.filter(media => media.uuid !== mediaUUID)
      }
    })
  }

  ngOnDestroy(): void {
    this.labelsService.selectedLabels = []
  }

  ngOnInit(): void {
  }

}
