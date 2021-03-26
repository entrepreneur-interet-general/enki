import { Location } from '@angular/common';
import { Directive, ElementRef, HostListener } from '@angular/core';

@Directive({
  selector: '[appFocusFormInput]'
})
export class FocusFormInputDirective {

  constructor(
    public el: ElementRef,
    private _location: Location 
    ) {}
  ngAfterViewInit(): void {
    const input: HTMLInputElement = this.el.nativeElement as HTMLInputElement;
    input.focus();
  }

  @HostListener('keydown', ['$event.keyCode', '$event.target.value']) onTabKeyup(keyCode, targetValue) {
    if (keyCode !== 9) return;
    if (keyCode === 9) {
      if (targetValue === '') {
        this._location.back();
      }
    } 
  }

}
