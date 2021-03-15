import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchEtablissementComponent } from './search-etablissement.component';

describe('SearchEtablissementComponent', () => {
  let component: SearchEtablissementComponent;
  let fixture: ComponentFixture<SearchEtablissementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchEtablissementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchEtablissementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
