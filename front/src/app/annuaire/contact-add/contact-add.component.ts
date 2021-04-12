import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Contact } from 'src/app/interfaces/Contact';
import { RegisterService } from 'src/app/registration/register.service';
import { SearchEtablissementService } from 'src/app/search-etablissement/search-etablissement.service';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-add',
  templateUrl: './contact-add.component.html',
  styleUrls: ['./contact-add.component.scss']
})
export class ContactAddComponent implements OnInit {
  contactGroup = new FormGroup({
    lastName: new FormControl('', Validators.required),
    firstName: new FormControl('', Validators.required),
    group: new FormControl('', Validators.required),
    etablissement: new FormControl('', Validators.required),
    position: new FormControl('', Validators.required),
    phone: new FormControl('', Validators.required),
    email: new FormControl('', Validators.required),
    address: new FormControl('', Validators.required),
  })
  userPositions: object[];

  userTypes: [];

  constructor(
    private annuaireService: AnnuaireService,
    private registerService: RegisterService,
    private searchEtablissementService: SearchEtablissementService,
    private router: Router
  ) {
    this.registerService.getUserTypes().subscribe(response => {
      this.userTypes = response
    })
    this.contactGroup.get('group').valueChanges.subscribe(typeName => {
      this.registerService.selectedGroupType.next(typeName);
      this.registerService.getUserPositions(typeName).subscribe(positions => {
        this.userPositions = positions
      })
    })

    this.searchEtablissementService.selectedEtablissement.subscribe((etablissement) => {
      this.contactGroup.get('etablissement').setValue(etablissement.label)
    })
  }

  ngOnInit(): void {
  }
  onSubmit(): void {
    const contact: Contact = {
      first_name: this.contactGroup.value.firstName,
      last_name: this.contactGroup.value.lastName,
      group_type: this.contactGroup.value.group,
      group_id: this.searchEtablissementService.selectedEtablissement.getValue().uuid,
      position_id: this.contactGroup.value.position,
      tel: {
        mobile: this.contactGroup.value.phone
      },
      email: this.contactGroup.value.email,
      address: this.contactGroup.value.address,
    }
    this.annuaireService.addContactToAnnuaire(contact).subscribe((contact) => {
      this.router.navigate(['annuaire/contactlist']);
    })
  }

  goToSearchEtablissement() {
    this.router.navigate([`contactadd/searchstructure`], { queryParams: { groupType: this.contactGroup.controls.group.value }})
  }

  ngOnDestroy(): void {
    this.searchEtablissementService.resetSelectedEtablissement();
  }
}
