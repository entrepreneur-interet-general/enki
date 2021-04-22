import { Component, Input, OnInit } from '@angular/core';

export const TOAST_DURATION = 3000;
@Component({
  selector: 'app-toast',
  template: `
    <div class="toast" [class.-show]="isDisplayed">
      {{message}}
    </div>
  `,
  styleUrls: ['./toast.component.scss']
})

export class ToastComponent implements OnInit {
  isDisplayed: boolean;
  @Input() message: string;
  constructor() {
    // this.isDisplayed = false;
  }

  ngOnInit(): void {
  }

  showMessage(message: string) {
    this.isDisplayed = true;
    this.message = message;
    setTimeout(() => {
      this.isDisplayed = false;
    }, TOAST_DURATION);
  }

}
