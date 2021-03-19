import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
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
    type: new FormControl(''),
  })
  evenementUUID: string;
  etablissementOptions: any[];
  auteursOptions: any[];
  messageTypeOptions: any[];
  constructor(
    private evenementsService: EvenementsService,
    private messagesService: MessagesService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.evenementUUID = this.evenementsService.selectedEvenementUUID.getValue()
    this.etablissementOptions = [];
    this.auteursOptions = [];
    this.messageTypeOptions = [];
    this.evenementsService.getEvenementByID(this.evenementUUID).subscribe(evenement => {
      this.filterGroup.controls.etablissement.setValue(evenement.filter.etablissement)
      this.filterGroup.controls.auteur.setValue(evenement.filter.auteur)
      this.filterGroup.controls.type.setValue(evenement.filter.type)
    })
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

        if(!this.messageTypeOptions.includes(message.type)) {
          this.messageTypeOptions.push(message.type)
        }
      })
      
    })
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    this.evenementsService.updateEvenementFilter(this.evenementUUID, this.filterGroup.getRawValue()).subscribe(() => {
      this.router.navigate(['../liste'], { relativeTo: this.route})
    })
  }

}
