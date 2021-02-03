import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { EvenementsService } from '../evenements.service';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-create-evenement',
  templateUrl: './create-evenement.component.html',
  styleUrls: ['./create-evenement.component.scss']
})
export class CreateEvenementComponent implements OnInit {

  evenementGroup = new FormGroup({
    nomEvenement: new FormControl('', Validators.required),
    descriptionEvenement: new FormControl('', Validators.required),
  })

  evenementUrl: string;
  evenement: object;
  httpOptions: object;

  constructor(
    private http: HttpClient,
    private evenementsService: EvenementsService,
    private router: Router
  ) {
    this.evenement = {
      "creator_id": "my_id",
      "description": "This is a task description",
      "started_at": "2020-12-16T09:57:38.396Z",
      "title": "This is a event title ",
      "type":"natural"
    }
    this.evenementUrl = `${environment.backendUrl}/events`
    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
      })
    }
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    let formBody = {
      "creator_id": "my_id",
      "title": this.evenementGroup.value.nomEvenement,
      "description": this.evenementGroup.value.descriptionEvenement,
      "started_at": "2020-12-16T09:57:38.396Z",
      "type": "natural"
    }
    this.httpFormSubmit(formBody).subscribe(response => {
      this.evenementsService.evenements.push(response.data)
      this.router.navigate([`evenements/${response.data.uuid}`])
    })
  }

  httpFormSubmit(formBody): Observable<any> {
    return this.http.post(this.evenementUrl, formBody, this.httpOptions)
  }

}
