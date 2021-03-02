import { Component, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-input',
  template: `
    <div class="enkiform__group" [formGroup]=group>
      <input type="text" class="enkiform__input" id="{{name}}" [formControl]="name" required>
      <label for="{{name}}" class="enkiform__label">{{label}}</label>
    </div>
  `,
  styles: [
  ]
})

export class InputComponent implements OnInit {

  @Input() name: string;
  @Input() label: string;
  @Input() group: FormGroup;

  constructor() { }

  ngOnInit(): void {
  }

}
