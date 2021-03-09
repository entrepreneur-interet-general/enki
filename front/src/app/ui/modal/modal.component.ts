import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent implements OnInit {
  isOpened: boolean;
  @Output() closed = new EventEmitter<boolean>();

  constructor() {
    this.isOpened = false;
  }

  ngOnInit(): void {
  }

  open(): void {
    this.isOpened = true;
  }

  close(): void {
    this.isOpened = false;
    this.closed.emit(true);
  }

}
