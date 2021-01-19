import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EvenementsService } from '../../evenements.service';
import { Message, MessagesService } from '../messages.service';

@Component({
  selector: 'app-main-courante',
  templateUrl: './main-courante.component.html',
  styleUrls: ['./main-courante.component.scss']
})
export class MainCouranteComponent implements OnInit {

  constructor(

    ) {

  }

  ngOnInit(): void {
  }

}
