import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { Observable} from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../../../user/user.service';
import { Router } from '@angular/router';
import { KeycloakService } from 'keycloak-angular';
import { environment } from 'src/environments/environment';
import { RegisterService } from '../../register.service';

@Component({
  selector: 'app-first-step',
  templateUrl: './first-step.component.html',
  styleUrls: ['./first-step.component.scss']
})
export class FirstStepComponent {

  userGroup = new FormGroup({
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    position: new FormControl('', Validators.required),
    structure: new FormControl('', Validators.required),
    location: new FormControl('', Validators.required)
  })
  fonctions: object;
  updateUserUrl: string;
  httpOptions: object;
  userTypes: [];
  userPositions: object[];

  constructor(
    private http: HttpClient,
    private router: Router,
    private userService: UserService,
    private keycloakService: KeycloakService
    private registerService: RegisterService
  ) {
    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('token')}`
      })
    }

    this.registerService.selectedLocation.subscribe((location) => {
      this.userGroup.get('location').setValue(location.label)
      console.log(this.userGroup.status)
    })

    this.registerService.getUserTypes().subscribe(response => {
      this.userTypes = response
    })


    this.userGroup.get('structure').valueChanges.subscribe(typeName => {
      this.registerService.getUserPositions(typeName).subscribe(positions => {
        this.userPositions = positions
      })
    })
  }

  ngOnInit(): void {
  }


  onSubmit(): void {
    let bodyForm = {
        position_id: this.userGroup.value.position,
        first_name: this.userGroup.value.firstName,
        last_name: this.userGroup.value.lastName,
        group_type: this.userGroup.value.structure,
        location_id: this.registerService.selectedLocation.getValue().uuid
    }
    console.log(bodyForm);
    this.httpSubmitForm(bodyForm).subscribe((response) => {

      this.userService.user.attributes = {
        fonction: this.userGroup.value.fonction
      }
      this.userService.user.location = this.userGroup.value.location
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
    return this.http.post<any>(`${environment.backendUrl}/users`, bodyForm, this.httpOptions)
  }

  goToSearchLocation() {
    this.router.navigate(["register/step1/searchlocation"])
  }
}
