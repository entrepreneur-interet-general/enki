import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main-courante',
  templateUrl: './main-courante.component.html',
  styleUrls: []
})
export class MainCouranteComponent implements OnInit {

  constructor(

    ) {

  }

  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

  ngOnInit(): void {
  }

}
