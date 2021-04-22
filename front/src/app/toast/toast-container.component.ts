import { Component, ComponentFactoryResolver, OnInit, ViewChild } from '@angular/core';
import { ToastDirective } from '../toast.directive';
import { ToastComponent } from './toast.component';

@Component({
  selector: 'app-toast-container',
  template: `
    <div>
      <ng-template toastHost></ng-template>
    </div>
  `,
  styleUrls: ['./toast-container.component.scss']
})
export class ToastContainerComponent implements OnInit {
  
  @ViewChild(ToastDirective, {static: true}) toastHost: ToastDirective;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(ToastComponent);
    console.log(this.toastHost)
    const viewContainerRef = this.toastHost.viewContainerRef;
    viewContainerRef.clear();
    const componentRef = viewContainerRef.createComponent<ToastComponent>(componentFactory);
    componentRef.instance.message = 'Hello toast';
  }

  ngOnInit(): void {
  }

}
