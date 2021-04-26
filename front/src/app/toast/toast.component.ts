import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

export const TOAST_DURATION = 3000;
@Component({
  selector: 'app-toast',
  template: `
    <div class="toast" [class.-show]="isDisplayed">
      <div class="toast--message">
        {{message}}
      </div>
      <a class="toast--close" (click)="closeMessage()">
        <svg class="icon-close-big icon"><use xlink:href="#icon-close-big"></use></svg>
      </a>
    </div>
  `,
  styleUrls: ['./toast.component.scss']
})

export class ToastComponent implements OnInit {
  isDisplayed: boolean;
  @Input() message: string;
  @Input() toastID: number;
  @Output() removeToast = new EventEmitter<number>();
  constructor() {
    // this.isDisplayed = false;
  }

  ngOnInit(): void {
  }

  closeMessage(): void {
    this.removeToast.emit(this.toastID);
  }

  showMessage(message: string): void {
    this.isDisplayed = true;
    this.message = message;
    setTimeout(() => {
      this.isDisplayed = false;
    }, TOAST_DURATION);
  }

}
