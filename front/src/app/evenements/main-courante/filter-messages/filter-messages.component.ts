import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { EvenementsService } from '../../evenements.service';
import { MessagesService } from '../messages.service';

@Component({
  selector: 'app-filter-messages',
  templateUrl: './filter-messages.component.html',
  styleUrls: ['./filter-messages.component.scss']
})
export class FilterMessagesComponent implements OnInit {

  filterGroup = new FormGroup({
    etablissement: new FormControl(''),
    auteur: new FormControl(''),
    messageType: new FormControl(''),
  })
  evenementUUID: string;
  etablissementOptions: any[];
  auteursOptions: any[];
  constructor(
    private evenementsService: EvenementsService,
    private messagesService: MessagesService
  ) {
    this.evenementUUID = this.evenementsService.selectedEvenementUUID.getValue()
    this.etablissementOptions = [];
    this.auteursOptions = [];
    this.messagesService.getMessagesByEvenementID(this.evenementUUID).subscribe(messages => {
      messages.forEach(message => {
        if (!this.etablissementOptions.some(item => item.group_id === message.creator.position.group_id)) {
          this.etablissementOptions.push({
            group_id: message.creator.position.group_id,
            group_label: message.creator.position.group.label
          })
        }

        if(!this.auteursOptions.some(item => item.auteur_id === message.creator.uuid)) {
          this.auteursOptions.push({
            auteur_id: message.creator.uuid,
            auteur_label: `${message.creator.first_name} ${message.creator.last_name}`
          })
        }
      })
      
    })
  }

  ngOnInit(): void {
  }

}
