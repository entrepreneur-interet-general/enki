import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-create-evenement',
  templateUrl: './create-evenement.component.html',
  styleUrls: ['./create-evenement.component.scss']
})
export class CreateEvenementComponent implements OnInit {

  evenementGroup = new FormGroup({
    nomEvenement: new FormControl('', Validators.required),
    descriptionEvenement: new FormControl('', Validators.required),
  })


  evenement: object;

  constructor() {
    this.evenement = {
      "creator_id": "my_id",
      "description": "This is a task description",
      "started_at": "2020-12-16T09:57:38.396Z",
      "title": "This is a event title ",
      "type":"natural"
    }
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    
  }

}
