import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main-courante',
  templateUrl: './main-courante.component.html',
  styleUrls: ['./main-courante.component.scss']
})
export class MainCouranteComponent implements OnInit {
  messages;
  constructor() {
    this.messages = [
      {
        "title": "Bonjour"
      }, {
        "title": "Hello"
      }
    ]
  }

  ngOnInit(): void {
  }

}
