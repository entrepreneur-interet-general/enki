import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { AddMessageComponent } from './add-message.component';

describe('AddMessageComponent', () => {
  let component: AddMessageComponent;
  let fixture: ComponentFixture<AddMessageComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ AddMessageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */
});
