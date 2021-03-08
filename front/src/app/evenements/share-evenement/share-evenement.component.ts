import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-share-evenement',
  templateUrl: './share-evenement.component.html',
  styleUrls: ['./share-evenement.component.scss']
})
export class ShareEvenementComponent implements OnInit {

  // participants = new FormControl('', Validators.required)

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) { }

  ngOnInit(): void {
  }

  goToSearchUser(): void {
    this.router.navigate(['./searchuser'], {relativeTo: this.activatedRoute})
  }

}
