import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { AnnuaireService } from './annuaire.service';
import { CONTACTS } from '../mocks/contacts-mocks';

describe('AnnuaireService', () => {
  let annuaireService: AnnuaireService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AnnuaireService]
    });
    annuaireService = TestBed.inject(AnnuaireService);
  });

  it('should be created', () => {
    expect(annuaireService).toBeTruthy();
  });

  describe('all user favs contacts', () => {
    it('should return favorite contacts of user', () => {
      const contactResponse = CONTACTS;
      let response;
      spyOn(annuaireService, 'getUserFavoriteContacts').and.returnValue(of(contactResponse));

      annuaireService.getUserFavoriteContacts().subscribe(res => {
        response = res
      })

      expect(response).toEqual(contactResponse)
    })
  })
  /* describe('add contact to favorite', () => {
    it('should add contact to user favs', () => {
      const newContact = {
        uuid: '3',
        name: 'Benjamin',
        group: 'Préfecture du 77',
        function: 'Préfet',
        phone: '0606060606',
        address: '55 avenue de saint ouen'
      }
      spyOn(annuaireService, 'addContactToUserFavs').and.
    })
  }) */

  describe('contact detail', () => {
    it('should return a contact detail', () => {
      const contactResponse = CONTACTS[0];
      let response;
      spyOn(annuaireService, 'getContactDetail').and.returnValue(of(contactResponse));

      annuaireService.getContactDetail('1').subscribe(res => {
        response = res
      })

      expect(response).toEqual(contactResponse)
    })
  })

});
