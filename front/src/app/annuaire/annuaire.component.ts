import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-annuaire',
  template: `
    <router-outlet (activate)="onActivate($event)" (deactivate)="onActivate($event)"></router-outlet>
  `,
  styles: [
  ]
})
export class AnnuaireComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
