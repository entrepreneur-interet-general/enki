import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../../user/user.service'
import { Router } from '@angular/router';
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
    // group: new FormControl('', Validators.required),
    fonction: new FormControl('', Validators.required),
    codeCommune: new FormControl('', Validators.required)
  })
  fonctions: object;
  updateUserUrl: string;
  httpOptions: object;

  constructor(
    private http: HttpClient,
    private router: Router,
    private userService: UserService,
    private keycloakService: KeycloakService
  ) {
    this.updateUserUrl = `http://localhost:8000/enki/v1/users`;
    this.fonctions = {
      mairie: [
        {
          id: "maire",
          label: "Maire"
        },
        {
          id: "securite",
          label: "Service sécurité"
        }
      ],
      prefecture: [
        {
          id: "cod",
          label: "COD"
        },
        {
          id: "prefet",
          label: "Préfèt"
        }
      ]
    };


    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('token')}`
      })
    }
  }

  ngOnInit(): void {
    // this.userGroup.controls.group.valueChanges.subscribe(value => this.onGroupChange(value));
  }

/*   onGroupChange(value: any): void {
    console.log(value)

  } */

  onSubmit(): void {
    let bodyForm = {
        code_insee: this.userGroup.value.codeCommune,
        // code_departement: 
        first_name: this.userGroup.value.firstName,
        last_name: this.userGroup.value.lastName,
        // group: this.userGroup.value.group, // SDIS, prefecture, mairie
        position: this.userGroup.value.fonction, // maire, COD, chef de salle
        // locationID: this.userGroup.value.locationID // ID commune, ID département

    }
    this.httpSubmitForm(bodyForm).subscribe((response) => {
      this.userService.user.attributes = {
        code_insee: this.userGroup.value.codeCommune,
        fonction: this.userGroup.value.fonction
      }
      this.userService.user.fullname = `${this.userGroup.value.firstName} ${this.userGroup.value.lastName}`
      /* this.keycloakService.updateToken(3600).then(() => {
        if(this.keycloakService.getUserRoles().includes('watchEvents')) { */
          this.keycloakService.clearToken()
          this.keycloakService.getToken().then((res) => {
            console.log(res)
            window.localStorage.setItem('token', res)
            // let decodedJWT: any = jwt_decode(res)

            // this.userService.user.attributes.fonction = decodedJWT.fonction ? decodedJWT.fonction : ""
            // this.userService.user.attributes.code_insee = decodedJWT.code_insee ? decodedJWT.code_insee : ""
          })
          this.router.navigate(['dashboard'])
/*         }
      }) */
    })
  }

  httpSubmitForm(bodyForm): Observable<object> {
    return this.http.post<any>(this.updateUserUrl, bodyForm, this.httpOptions)
  }

}
