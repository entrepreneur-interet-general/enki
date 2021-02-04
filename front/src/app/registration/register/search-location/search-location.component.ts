import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router, Routes } from '@angular/router';
import { RegisterService } from '../../register.service';

@Component({
  selector: 'app-search-location',
  templateUrl: './search-location.component.html'
})
export class SearchLocationComponent implements OnInit {

  locationSearch = new FormControl('', Validators.required)
  locationResults: object[]

  constructor(
    private registerService: RegisterService,
    private router: Router
  ) {
    this.locationResults = []
    this.locationSearch.valueChanges.subscribe(value => {
      if (value.length > 1) {
        this.registerService.searchLocation(value).subscribe(res => {

          this.locationResults = res
        })
      }
    })
  }

  ngOnInit(): void {
    
  }

  selectLocation(name, label) {
    this.registerService.selectedLocation = {
      name: name,
      label: label
    }
    this.router.navigate(['register/step1'])
  }

}
