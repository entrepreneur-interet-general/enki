import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { interval, Observable, of, Subject } from 'rxjs';
import { debounce, map, pluck, switchMap } from 'rxjs/operators';
import { REGISTER } from 'src/app/constants';
import { environment } from 'src/environments/environment';
import { Location } from '../../../../interfaces/Location';
import { RegisterService } from '../../../register.service';

@Component({
  selector: 'app-search-location',
  templateUrl: './search-location.component.html'
})
export class SearchLocationComponent implements OnInit {

  locationSearch = new FormControl('', Validators.required)
  locationResults$: Observable<Location[]>;
  subjet = new Subject();

  constructor(
    private registerService: RegisterService,
    private router: Router
  ) {
    this.locationResults$ = this.subjet.pipe(
      debounce(() => interval(500)),
      switchMap((searchText: string) => {
        return this.registerService.searchLocation(searchText)
      })
    )
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
