import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { TOAST_DURATION } from '../constants/constants';

@Component({
  selector: 'app-toast',
  template: `
    <div class="toast" [class.-show]="isDisplayed" [style.animation-delay]="TOAST_DURATION">
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
  public readonly TOAST_DURATION: string = `${(TOAST_DURATION / 1000) - 1}s`;
  @Input() message: string;
  @Input() toastID: number;
  @Output() removeToast = new EventEmitter<number>();
  constructor() {
  }

  ngOnInit(): void {
  }

  closeMessage(): void {
    this.removeToast.emit(this.toastID);
  }

}
