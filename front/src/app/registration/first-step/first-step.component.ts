import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-first-step',
  templateUrl: './first-step.component.html',
  styleUrls: ['./first-step.component.scss']
})
export class FirstStepComponent implements OnInit {

  firstName = new FormControl();
  lastName = new FormControl();
  role = new FormControl();
  codeCommune = new FormControl();

  constructor() { }

  ngOnInit(): void {
  }

}
