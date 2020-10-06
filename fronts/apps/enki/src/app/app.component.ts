import { Component } from '@angular/core';
import { AffairesService } from './affaires.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'enki';
  affaires;

  constructor(private affairesService: AffairesService) {
  }
  ngOnInit(): void {
    this.affairesService.getAffaires().subscribe((affaires) => {
      this.affaires = affaires
    })
  }
}
