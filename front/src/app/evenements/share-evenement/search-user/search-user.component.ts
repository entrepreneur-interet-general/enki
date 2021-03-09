import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { interval, Observable, of, Subject, throwError } from 'rxjs';
import { catchError, debounce, pluck, switchMap } from 'rxjs/operators';
import { HTTP_DATA } from 'src/app/constants';
import { User } from 'src/app/interfaces/User';
import { environment } from 'src/environments/environment';
import { EvenementsService } from '../../evenements.service';

@Component({
  selector: 'app-search-user',
  templateUrl: './search-user.component.html',
  styleUrls: ['./search-user.component.scss']
})
export class SearchUserComponent implements OnInit {
  userResults: User[];
  userResults$: Observable<User[]>;
  userSearch = new FormControl('', Validators.required)
  subject = new Subject()

  constructor(
    private http: HttpClient,
    private evenementsService: EvenementsService,
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {
    this.userResults = [];

    this.userSearch.valueChanges.subscribe((value: string) => {
      if (value.length > 2) {
        this.subject.next(value)
      }
    })

    this.userResults$ = this.subject.pipe(
      debounce(() => interval(500)),
      switchMap((searchText: string) => {
        return this.searchUsersHttp(searchText)
      })
    )

    this.userResults$.subscribe((result) => {
      this.userResults = result
    })

  }

  ngOnInit(): void {
  }

  searchUsersHttp(query: string): Observable<User[]> {
    return this.http.get<any>(`${environment.backendUrl}/users?query=${query}`).pipe(
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
  }

  selectUser(user: User): void {
    // PUT http://localhost:8000/enki/v1/events/<event_id>/invite/<user_id>
    this.addParticipantsToEvenement(user.uuid).subscribe((res) => {
      this.evenementsService.addParticipantsToEvenement({user: res, type: 'view'});
      this.router.navigate(['..'], { relativeTo: this.activatedRoute});
    })
  }
  
  addParticipantsToEvenement(userUUID: string): Observable<User> {
    return this.http.put<any>(`${environment.backendUrl}/events/${this.evenementsService.selectedEvenement.getValue().uuid}/invite/${userUUID}`, {}).pipe(
      pluck(HTTP_DATA)
    )
  }
}
