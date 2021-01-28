import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/user/user.service';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-list',
  templateUrl: './contact-list.component.html',
  styleUrls: ['./contact-list.component.scss']
})
export class ContactListComponent implements OnInit {
  contacts;
  constructor(
    private userService: UserService
  ) {
    this.contacts = [];
  }

  ngOnInit(): void {
    this.userService.getUserFavoriteContacts().subscribe((res) => {
      this.contacts = res;
    })
  }

}
