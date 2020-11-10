import { TestBed } from '@angular/core/testing';

import { AppAuthGuardService } from './app-auth-guard.service';

describe('AppAuthGuardService', () => {
  let service: AppAuthGuardService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AppAuthGuardService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
