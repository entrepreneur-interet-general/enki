import { Location } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { HistoryUrlService } from 'src/app/history-url.service';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Evenement } from '../evenements.service';

@Component({
  selector: 'app-detail-evenement',
  templateUrl: './detail-evenement.component.html',
  styleUrls: ['./detail-evenement.component.scss']
})
export class DetailEvenementComponent implements OnInit {
  uuid: string;
  evenement: Evenement;
  backLabel: string;
  constructor(
    private route: ActivatedRoute,
    public mobilePrototype: MobilePrototypeService,
    private router: Router,
    private historyUrl: HistoryUrlService,
    private activatedRoute: ActivatedRoute,
    ) {
      console.log(this.historyUrl.getPreviousUrl())
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: { event: Evenement }) => {
      this.evenement = data.event;
      this.uuid = data.event.uuid;
    });
  }
  goBack(): void {
    this.router.navigate(['evenements'])
  }

  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
