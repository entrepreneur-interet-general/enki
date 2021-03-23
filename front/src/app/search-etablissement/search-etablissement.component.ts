import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { interval, Observable, of, Subject, throwError } from 'rxjs';
import { catchError, debounce, pluck, switchMap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HTTP_DATA } from '../constants';
import { SearchEtablissementService } from './search-etablissement.service';
import { Location } from '../interfaces/Location';

@Component({
  selector: 'app-search-etablissement',
  templateUrl: './search-etablissement.component.html'
  // styleUrls: ['./search-etablissement.component.scss']
})
export class SearchEtablissementComponent implements OnInit {

  etablissementSearch = new FormControl('', Validators.required);
  subject = new Subject();
  etablissementResults$: Observable<Location[]>;
  etablissementResults: Location[];
  groupType: string;


  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
    private etablissementService: SearchEtablissementService
  ) {
    this.groupType = this.route.snapshot.queryParams.groupType

    this.etablissementResults$ = this.subject.pipe(
      debounce(() => interval(500)),
      switchMap((inputValue: string) => {
        return this.http.get<any>(`${environment.backendUrl}/groups?groupType=${this.groupType}&query=${inputValue}`).pipe(
          pluck(HTTP_DATA),
          catchError((error) => {
            if (error.status === 404) {
              return of([])
            } else {
              console.error(error)
              return throwError(
                'Something bad happened; please try again later.');
            }
          })
        )
      })
    );

    this.etablissementResults$.subscribe((results) => {
      this.etablissementResults = results
    });

    this.etablissementSearch.valueChanges.subscribe((value: string) => {
      if (value.length > 2) {
        this.subject.next(value)
      }
    });
  }

  ngOnInit(): void {
  }

  selectEtablissement(etablissement: Location): void {
    this.etablissementService.setSelectedEtablissement(etablissement)
    this.router.navigate([`..`], {relativeTo: this.route})
  }

}
