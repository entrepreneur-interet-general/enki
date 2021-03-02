import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { interval, Observable, Subject } from 'rxjs';
import { debounce, switchMap } from 'rxjs/operators';
import { REGISTER } from 'src/app/constants';
import { Location } from '../../../../interfaces/Location';
import { RegisterService } from '../../../register.service';

@Component({
  selector: 'app-search-location',
  templateUrl: './search-location.component.html'
})
export class SearchLocationComponent implements OnInit {

  locationSearch = new FormControl('', Validators.required)
  locationResults$: Observable<Location[]>;
  locationResults: Location[];
  subjet = new Subject();

  constructor(
    private registerService: RegisterService,
    private router: Router
  ) {

    this.locationResults$ = this.subjet.pipe(
      debounce(() => interval(500)),
      switchMap((searchText: string) => {
        return this.registerService.searchLocation(searchText, this.registerService.selectedGroupType.getValue())
      })
    )

    this.locationResults$.subscribe((results) => {
      this.locationResults = results
    })

    this.locationSearch.valueChanges.subscribe((value: string) => {
      if (value.length > 2) {
        this.subjet.next(value)
      }
    })
  }

  ngOnInit(): void {
    
  }

  selectLocation(location: Location) {
    this.registerService.setSelectedLocation(location)
    this.router.navigate([`${REGISTER}/step1`])
  }

}
