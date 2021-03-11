import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { RegisterService } from 'src/app/registration/register.service';

@Component({
  selector: 'app-invitation',
  templateUrl: './invitation.component.html',
  styleUrls: ['./invitation.component.scss']
})
export class InvitationComponent implements OnInit {


  invitationGroup = new FormGroup({
    email: new FormControl('', Validators.required),
    phone: new FormControl('', Validators.required),
    group: new FormControl('', Validators.required),
    structure: new FormControl('', Validators.required),
  })

  groupTypes: [];

  constructor(
    private registerService: RegisterService
  ) {
    this.registerService.getUserTypes().subscribe(response => {
      console.log(response)
      this.groupTypes = response
    })
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    console.log('submit')
  }

  goToSearchLocation(): void {
    console.log('go to search location')
  }

}
