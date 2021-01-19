import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SummaryEvenementComponent } from './summary-evenement.component';

describe('SummaryEvenementComponent', () => {
  let component: SummaryEvenementComponent;
  let fixture: ComponentFixture<SummaryEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SummaryEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SummaryEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});