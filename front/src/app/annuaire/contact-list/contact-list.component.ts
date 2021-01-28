import { Component, OnInit } from '@angular/core';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-list',
  templateUrl: './contact-list.component.html',
  styleUrls: ['./contact-list.component.scss']
})
export class ContactListComponent implements OnInit {
  contacts;
  constructor(
    private annuaireService: AnnuaireService
  ) {
    this.contacts = [];
  }

  ngOnInit(): void {
    this.annuaireService.getUserFavoriteContacts().subscribe((res) => {
      this.contacts = res;
    })
  }

}
