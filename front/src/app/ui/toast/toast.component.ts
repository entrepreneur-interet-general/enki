import { Component, OnInit } from '@angular/core';

export const TOAST_DURATION = 3000;
@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss']
})

export class ToastComponent implements OnInit {
  isDisplayed: boolean;
  message: string;
  constructor() {
    this.isDisplayed = false;
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
