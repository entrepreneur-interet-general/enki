import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-select',
  template: `
    <div class="enkiform__group">
      <select class="enkiform__input" id="name" formControlName="name" required>
        <option *ngFor="let option of options" value="{{option.value}}">{{option.label}}</option>
      </select>
      <label for="name" class="enkiform__label">{{label}}</label>
      <svg class="icon-chevron icon"><use xlink:href="#icon-chevron"></use></svg>
    </div>
  `,
  styles: [
  ]
})
export class SelectComponent implements OnInit {

  @Input() name: string;
  @Input() label: string;
  @Input() options: object[];


  constructor() { }

  ngOnInit(): void {
  }

}
