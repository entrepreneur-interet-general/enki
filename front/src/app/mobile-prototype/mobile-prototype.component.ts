import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MobilePrototypeService } from './mobile-prototype.service';

@Component({
  selector: 'app-mobile-prototype',
  templateUrl: './mobile-prototype.component.html',
  styleUrls: ['./mobile-prototype.component.scss']
})
export class MobilePrototypeComponent implements OnInit {

  checked = new FormControl(true)
  constructor(
    public prototypeService: MobilePrototypeService
  ) {
    this.checked.valueChanges.subscribe(isChecked => {
      this.prototypeService.setChecked(isChecked);
    })
  }

  ngOnInit(): void {
  }

}
