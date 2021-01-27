import { TestBed } from '@angular/core/testing';

import { GuardRegisterGuard } from './guard-register.guard';

describe('GuardRegisterGuard', () => {
  let guard: GuardRegisterGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(GuardRegisterGuard);
  });

/*   it('should be created', () => {
    expect(guard).toBeTruthy();
  }); */
});
