import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-detail',
  templateUrl: './contact-detail.component.html',
  styleUrls: ['./contact-detail.component.scss']
})
export class ContactDetailComponent implements OnInit {

  contactUUID;
  contact;

  constructor(
    private route: ActivatedRoute,
    private annuaireService: AnnuaireService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.contactUUID = params['uuid']
      this.annuaireService.getContactDetails(this.contactUUID).subscribe(contact => {
        this.contact = contact
      })
    })
  }

}
