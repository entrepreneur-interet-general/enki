import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

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
  constructor() { }

  ngOnInit(): void {
  }

}
