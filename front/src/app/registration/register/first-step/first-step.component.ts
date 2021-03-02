import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { Observable} from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../../../user/user.service';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { RegisterService } from '../../register.service';
import { REGISTER } from 'src/app/constants';

@Component({
  selector: 'app-first-step',
  templateUrl: './first-step.component.html',
  styleUrls: ['./first-step.component.scss']
})
export class FirstStepComponent {

  userGroup = new FormGroup({
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    group: new FormControl('', Validators.required),
    position: new FormControl('', Validators.required),
    structure: new FormControl('', Validators.required),
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
    private registerService: RegisterService
  ) {
    this.httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('token')}`
      })
    }

    this.registerService.selectedLocation.subscribe((structure) => {
      this.userGroup.get('structure').setValue(structure.label)
    })
    
    this.registerService.getUserTypes().subscribe(response => {
      this.userTypes = response
    })
    
    
    this.userGroup.get('group').valueChanges.subscribe(typeName => {
      this.registerService.selectedGroupType.next(typeName);
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
        group_type: this.userGroup.value.group,
        group_id: this.registerService.selectedLocation.getValue().uuid
    }
    this.httpSubmitForm(bodyForm).subscribe((response) => {

      this.userService.user.attributes = {
        fonction: this.userGroup.value.fonction
      }
      console.log(response.data)

      this.router.navigate(['dashboard'])

    })
  }

  httpSubmitForm(bodyForm): Observable<any> {
    return this.http.post<any>(`${environment.backendUrl}/users`, bodyForm, this.httpOptions)
  }

  goToSearchLocation() {
    this.router.navigate([`${REGISTER}/step1/searchlocation`])
  }
}
