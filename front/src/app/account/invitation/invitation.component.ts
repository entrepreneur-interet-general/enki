import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { RegisterService } from 'src/app/registration/register.service';
import { SearchEtablissementService } from 'src/app/search-etablissement/search-etablissement.service';

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
    private registerService: RegisterService,
    private router: Router,
    private etablissementService: SearchEtablissementService
  ) {
    this.registerService.getUserTypes().subscribe(response => {
      console.log(response)
      this.groupTypes = response
    })

    this.etablissementService.selectedEtablissement.subscribe((structure) => {
      this.invitationGroup.get('structure').setValue(structure.label)
    })
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    console.log('submit')
  }

  goToSearchEtablissement(): void {
    this.router.navigate([`account/invitation/searchetablissement`], { queryParams: { groupType: this.invitationGroup.controls.group.value }})
  }

}
