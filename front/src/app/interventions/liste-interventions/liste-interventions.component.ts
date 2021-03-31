import { Component, OnInit } from '@angular/core';
import { InterventionsService } from '../interventions.service'
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-liste-interventions',
  templateUrl: './liste-interventions.component.html',
  styleUrls: ['./liste-interventions.component.scss']
})
export class ListeInterventionsComponent implements OnInit {
  interventions;
  constructor(
    private interventionsService: InterventionsService,
  ) {
    this.interventions = [];
    this.interventionsService.httpGetAllInterventions().subscribe((interventions) => {
        this.interventions = environment.HTTPClientInMemory ? interventions.map((intervention, index) => {
          intervention.uuid = (index + 1).toString()
          return intervention
        }) : interventions
    });
  }
  ngOnInit(): void {

  }
  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
  }
}
