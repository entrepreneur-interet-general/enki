import { Component, OnInit } from '@angular/core';
import { Contact } from 'src/app/interfaces/Contact';
import { UserService } from 'src/app/user/user.service';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-list',
  templateUrl: './contact-list.component.html',
  styleUrls: ['./contact-list.component.scss']
})
export class ContactListComponent implements OnInit {
  contacts: Contact[];
  constructor(
    private userService: UserService
  ) {
    this.contacts = [];
  }

  ngOnInit(): void {
    this.userService.getUserFavoriteContacts().subscribe((res) => {
      this.contacts = this.sort(res);
    })
  }

  sort(contacts: Contact[]): Array<Contact> {
    return contacts.sort(this.compare)
  }
  compare(a, b): any {
    if (a.name.toLowerCase() < b.name.toLowerCase()) {
      return -1;
    }
    if (a.name.toLowerCase() > b.name.toLowerCase()) {
      return 1;
    }
    return 0;
  }

  compareIfFirstLetterIsDifferent(contactA, contactB): boolean {
    if (contactA && contactB && contactA.name[0] !== contactB.name[0]) {
      return true;
    }
    return contactA === undefined;
  }

}
