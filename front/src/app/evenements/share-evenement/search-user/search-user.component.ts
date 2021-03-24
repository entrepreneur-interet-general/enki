import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { interval, Observable, of, Subject, throwError } from 'rxjs';
import { catchError, debounce, pluck, switchMap } from 'rxjs/operators';
import { HTTP_DATA } from 'src/app/constants';
import { Participant } from 'src/app/interfaces/Participant';
import { User } from 'src/app/interfaces/User';
import { UserService } from 'src/app/user/user.service';
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
    private activatedRoute: ActivatedRoute,
    private userService: UserService
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
    // exclude current `Participants` from being retrieved by search
    const participants: string[] = this.evenementsService.getSelectedEvenementsParticipants().map(participant => participant.user.uuid)
    // exclude current user from being retrieved by search
    participants.push(this.userService.user.uuid)
    const participantsParam = participants.toString()
    const user_ids = participantsParam ? `&uuids=${participants}` : ``;
    return this.http.get<any>(`${environment.backendUrl}/users?query=${query}${user_ids}`).pipe(
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
    return this.http.put<any>(`${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/invite/${userUUID}`, {}).pipe(
      pluck(HTTP_DATA)
    )
  }
}
