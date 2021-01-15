import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../../user/user.service'
import { Router } from '@angular/router';

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
    private router: Router,
    private userService: UserService
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
    let bodyForm = {
      attributes: {
        "communes": this.userGroup.value.codeCommune,
        "fonction": this.userGroup.value.fonction
      },
      firstName: this.userGroup.value.firstName,
      lastName: this.userGroup.value.lastName,
      user_fonction: this.userGroup.value.fonction
    }
    this.httpSubmitForm(bodyForm).subscribe((response) => {
      this.userService.user.attributes = {
        code_insee: this.userGroup.value.codeCommune,
        fonction: this.userGroup.value.fonction
      }
      this.userService.user.fullname = `${this.userGroup.value.firstName} ${this.userGroup.value.lastName}`
      /* this.keycloakService.updateToken(3600).then(() => {
        if(this.keycloakService.getUserRoles().includes('watchEvents')) { */
          this.router.navigate(['dashboard'])
/*         }
      }) */
    })
  }

  httpSubmitForm(bodyForm): Observable<object> {
    return this.http.put<any>(this.updateUserUrl, bodyForm, this.httpOptions)
  }

}
