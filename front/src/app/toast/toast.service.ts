import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ToastService {
  
  private readonly _messages = new Subject<string>();
  readonly messages$ = this._messages.asObservable();

  constructor() { }

  addMessage(message: string): void {
    this._messages.next(message);
  }
  
}
