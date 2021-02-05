import { Selector } from 'testcafe';

fixture `Getting Started`
    .page `http://localhost:1337`;

    const fonctionSelect = Selector('#fonction');
    const fonctionOption = fonctionSelect.find('option');
test('My first test', async t => {

    // Test code
    await t
      .typeText('#username', 'mairie@chelles.fr')
      .typeText('#password', 'azeRTY123#')
      .click('#kc-login')

      await Selector('.userInfoForm')
      await t
      .typeText('#lastName', 'PERNEY')
      .typeText('#firstName', 'Benjamin')
      .click(fonctionSelect)
      .click(fonctionOption.withText('Préfet'))
      .expect(fonctionSelect.value).eql('prefet')

});