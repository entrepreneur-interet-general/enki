import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { interval, Observable, Subject } from 'rxjs';
import { debounce, switchMap } from 'rxjs/operators';
import { RegisterService } from '../registration/register.service';
import { Location } from '../interfaces/Location';
import { SEARCH_MIN_CHARS } from '../constants/constants';

@Component({
  selector: 'app-search-structure',
  templateUrl: './search-structure.component.html',
  styles: [
  ]
})
export class SearchStructureComponent implements OnInit {

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
      if (value.length >= SEARCH_MIN_CHARS) {
        this.subjet.next(value)
      }
    })
  }

  ngOnInit(): void {
    
  }

  selectLocation(location: Location) {
    this.registerService.setSelectedLocation(location)
    this.router.navigate([`contactadd`])
  }

}
