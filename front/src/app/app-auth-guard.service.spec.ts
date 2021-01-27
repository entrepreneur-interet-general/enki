import { TestBed } from '@angular/core/testing';

import { AuthGuard } from './app-auth-guard.service';

describe('AppAuthGuardService', () => {
  let service: AuthGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthGuard);
  });

/*   it('should be created', () => {
    expect(service).toBeTruthy();
  }); */
});
