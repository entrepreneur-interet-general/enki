import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SituationsComponent } from './situations.component';

describe('SituationsComponent', () => {
  let component: SituationsComponent;
  let fixture: ComponentFixture<SituationsComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SituationsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SituationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */
});
