import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-add-label',
  templateUrl: './add-label.component.html',
  styleUrls: ['./add-label.component.scss']
})
export class AddLabelComponent implements OnInit {
  labelSearch = new FormControl('')
  constructor() { }

  ngOnInit(): void {
  }

  addLabel(): void {
    console.log('on ajoute le label !')
  }
}
