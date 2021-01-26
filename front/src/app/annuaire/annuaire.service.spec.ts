import { TestBed } from '@angular/core/testing';

import { AnnuaireService } from './annuaire.service';

describe('AnnuaireService', () => {
  let service: AnnuaireService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnnuaireService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
