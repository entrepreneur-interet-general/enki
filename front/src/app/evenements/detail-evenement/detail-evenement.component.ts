import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Evenement, EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-detail-evenement',
  templateUrl: './detail-evenement.component.html',
  styleUrls: ['./detail-evenement.component.scss']
})
export class DetailEvenementComponent implements OnInit {
  uuid: string;
  evenement: Evenement;
  fetchedEvenement: boolean;
  constructor(
    private route: ActivatedRoute,
    private evenementsService: EvenementsService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      this.evenementsService.getEvenement(this.uuid).subscribe((evenement) => {
        this.evenement = evenement
        this.fetchedEvenement = true;
      });
    })
  }

}
