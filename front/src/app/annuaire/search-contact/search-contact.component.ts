import { Component, OnInit } from '@angular/core';
import { Contact } from 'src/app/interfaces/Contact';
import { AnnuaireService } from '../annuaire.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { User } from 'src/app/interfaces/User';
import { UserService } from 'src/app/user/user.service';

@Component({
  selector: 'app-search-contact',
  templateUrl: './search-contact.component.html',
  styleUrls: ['./search-contact.component.scss']
})
export class SearchContactComponent implements OnInit {

  contactList: Contact[];
  contactSearch = new FormControl('')

  constructor(
    private annuaireService: AnnuaireService,
    public userService: UserService
  ) {
    this.contactList = []
  }

  ngOnInit(): void {
    // this.contactSearch.valueChanges.subscribe(value => this.onSearchInputChange(value));
    this.annuaireService.searchInAnnuaire().subscribe((res) => {
      this.contactList = res
    })
  }

  onSearchInputChange(query: string): void {

    /* TODO: search in backend */
/*     if (query.length >= 3) {
      this.annuaireService.searchInAnnuaire(query).subscribe((res) => {
        this.contactList = res
      })
    } */
  }

  addRemoveToUserFavs(contactId: string): void {
    if (this.userService.user.contacts.filter(contact => contact.uuid === contactId).length > 0) {
      this.userService.removeContactFromUserFavs(contactId).subscribe()
    } else {
      this.userService.addContactToUserFavs(contactId).subscribe()
    }
  }

  isUserFav(contactId: string): boolean {
    return this.userService.isUserFav(contactId)
  }
}
