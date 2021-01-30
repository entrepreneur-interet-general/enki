import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ListeMainCouranteComponent } from './liste-main-courante.component';

describe('ListeMainCouranteComponent', () => {
  let component: ListeMainCouranteComponent;
  let fixture: ComponentFixture<ListeMainCouranteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ListeMainCouranteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListeMainCouranteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */
});
