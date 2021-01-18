import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-detail-evenement',
  templateUrl: './detail-evenement.component.html',
  styleUrls: ['./detail-evenement.component.scss']
})
export class DetailEvenementComponent implements OnInit {
  uuid: string;
  evenement: Evenement;

  constructor(
    private route: ActivatedRoute,
    private evenementsService: EvenementsService
  ) { }

  ngOnInit(): void {
    // debugger;
    // this.uuid = this.route.snapshot.paramMap.get('foo')
    this.route.data.subscribe((data: { event: Evenement }) => {
      this.evenement = data.event;
      this.uuid = data.event.uuid;

    });
  }


}
