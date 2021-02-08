import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { MainCouranteComponent } from './main-courante.component';

describe('MainCouranteComponent', () => {
  let component: MainCouranteComponent;
  let fixture: ComponentFixture<MainCouranteComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ MainCouranteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MainCouranteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */
});
