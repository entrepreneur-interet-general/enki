import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-search-user',
  templateUrl: './search-user.component.html',
  styleUrls: ['./search-user.component.scss']
})
export class SearchUserComponent implements OnInit {
  userResults: [];
  userSearch = new FormControl('', Validators.required)

  constructor() {
    this.userResults = [];
  }

  ngOnInit(): void {
  }

}
