import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Contact } from 'src/app/interfaces/Contact';
import { uuidv4 } from 'src/app/utilities';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-add',
  templateUrl: './contact-add.component.html',
  styleUrls: ['./contact-add.component.scss']
})
export class ContactAddComponent implements OnInit {
  contactGroup = new FormGroup({
    name: new FormControl('', Validators.required),
    group: new FormControl('', Validators.required),
    function: new FormControl('', Validators.required),
    phone: new FormControl('', Validators.required),
    email: new FormControl('', Validators.required),
    address: new FormControl('', Validators.required),
  })
  constructor(
    private annuaireService: AnnuaireService,
    private router: Router
  ) { }

  ngOnInit(): void {
  }
  onSubmit(): void {
    const contact: Contact = {
      uuid: uuidv4(),
      name: this.contactGroup.value.name,
      group: this.contactGroup.value.group,
      function: this.contactGroup.value.function,
      phone: this.contactGroup.value.phone,
      email: this.contactGroup.value.email,
      address: this.contactGroup.value.address,
    }
    this.annuaireService.addContactToAnnuaire(contact).subscribe((contact) => {
      this.router.navigate(['annuaire/contactlist']);
    })
  }

}
