import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { KeycloakService } from 'keycloak-angular';

@Component({
  selector: 'app-first-step',
  templateUrl: './first-step.component.html',
  styleUrls: ['./first-step.component.scss']
})
export class FirstStepComponent {

  userGroup = new FormGroup({
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    fonction: new FormControl('', Validators.required),
    codeCommune: new FormControl('', Validators.required)
  })
  updateUserUrl: string;
  httpOptions: object;

  constructor(
    private http: HttpClient,
    private keycloakService: KeycloakService
  ) {
    this.updateUserUrl = `http://localhost:4201/api/user`;
    
    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('token')}`
      })
    }
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    console.warn(this.userGroup.value)
    let bodyForm = {
      attributes: {
        "communes": this.userGroup.value.codeCommune,
        "fonction": this.userGroup.value.fonction
      },
      firstName: this.userGroup.value.firstName,
      lastName: this.userGroup.value.lastName
    }
    this.httpSubmitForm(bodyForm).subscribe((response) => {
      console.log(response)
    })
  }

  httpSubmitForm(bodyForm): Observable<object> {
    return this.http.put<any>(this.updateUserUrl, bodyForm, this.httpOptions)
  }

}
