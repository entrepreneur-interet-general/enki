import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Location } from '../../../../interfaces/Location';
import { RegisterService } from '../../../register.service';

@Component({
  selector: 'app-search-location',
  templateUrl: './search-location.component.html'
})
export class SearchLocationComponent implements OnInit {

  locationSearch = new FormControl('', Validators.required)
  locationResults: Location[]

  constructor(
    private registerService: RegisterService,
    private router: Router
  ) {
    this.locationResults = []
    this.locationSearch.valueChanges.subscribe(value => {
      if (value.length > 1) {
        this.registerService.searchLocation(value).subscribe(locationResults => {
          this.locationResults = locationResults
        })
      }
    })
  }

  ngOnInit(): void {
    
  }

  selectLocation(location: Location) {
    this.registerService.setSelectedLocation(location)
    this.router.navigate(['register/step1'])
  }

}
