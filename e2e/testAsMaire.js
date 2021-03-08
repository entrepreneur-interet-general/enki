import { Selector } from 'testcafe';
const randomString = function makeid(length) {
  var result           = '';
  var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
     result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

fixture `Test as Maire`
    .page `http://localhost:1337`
    .beforeEach( async t => {
      await t
      .typeText('#username', 'mairie@chelles.fr')
      .typeText('#password', 'azeRTY123#')
      .click('#kc-login')

      await Selector('.dashboard')
    })

    const EVENT_TITLE = 'Test auto événement'
    const EVENT_DESCRIPTION = 'Test auto événement'

    test('Create `événement`', async t => {
      await t
      .click('.burger')
      .click('#test--link-situation')
      .click('#test--evenements')
      .click('.action--add')
      .typeText('#nomEvenement', EVENT_TITLE)
      .typeText('#descriptionEvenement', EVENT_DESCRIPTION)
      .typeText('#startDate', `2021-03-09T19:37`)
      .click('.createEvenement--form input[type="submit"]')
      .expect(Selector('.evenement--title').innerText).eql(EVENT_TITLE)
      .click('#test--maincourante')
      .expect(Selector('.mc--empty').exists).ok()
    })

    const MESSAGE_TITLE = 'Test auto message 2'
    const MESSAGE_DESCRIPTION = 'Test auto description'
    const LABEL_TITLE = randomString(5)
    test('Add message to `main courante`', async t => {
      await t
      // go to the previously created event
      .click('.burger')
      .click('#test--link-situation')
      .click('#test--evenements')
      .click('.evenement--element:last-child')
      .click('#test--maincourante')
      // the main courante should be empty
      // create a new message
      .click('.mc--empty button')
      .typeText('.addMessageForm--titleInput', MESSAGE_TITLE)
      .typeText('.addMessageForm--descriptionTextarea', MESSAGE_DESCRIPTION)
      // BEGIN label testing
      .click('.labelGroup--labelLink')
      .typeText('.fullscreen-form--searchInput', LABEL_TITLE)
      .expect(Selector('.searchList--element:first-child .badge').innerText).eql(LABEL_TITLE.toUpperCase())
      .click('.searchList--element:first-child')
      .click('.selectedLabels--item .icon-close')
      .click('.searchList--element:first-child')
      .click('.fullscreen-form--cancel')
      // END label testing
      .setFilesToUpload('#mediaFile', './gymnase.jpg')
      .click('.addMessageForm input[type="submit"]')
      // verify message infos from the list of messages
      .expect(Selector('.list--element:first-child .mainInfos--title').innerText).contains('MAIRE')
      .expect(Selector('.list--element:first-child .mainInfos--content').innerText).contains(MESSAGE_TITLE)
      .expect(Selector('.list--element:first-child .previewImage').exists).ok()
      .click('.list--element:first-child')
      .expect(Selector('.detail-message--description').innerText).contains(MESSAGE_DESCRIPTION)
      .click('.goTo')
      .expect(Selector('.mc').exists).ok()
      // add an other message but cancel before sending
      .click('.action--add')
      .click('.small-heading--close')
      .expect(Selector('.mc').exists).ok()

    })

    const INPUT_INFOS = randomString(5)
    const structureSelect = Selector('#group');
    const structureOption = structureSelect.find('option');
    const positionSelect = Selector('#position');
    const positionOption = positionSelect.find('option')
    test('Create contact and add to favorite', async t => {
      await t
        .click('.burger')
        .click('#test--link-annuaire')
        // add contact to annuaire
        .click('.action--add')
        .typeText('#lastName', INPUT_INFOS)
        .typeText('#firstName', INPUT_INFOS)
        .click(structureSelect)
        .click(structureOption.withText('Mairie'))
        .click(positionSelect)
        .click(positionOption.withText('Maire'))
        .click('#structure')
        .typeText('.fullscreen-form--searchInput', 'Chelles')
        .click('#locationid-77108')

        .typeText('#phone', INPUT_INFOS)
        .typeText('#email', INPUT_INFOS)
        .typeText('#address', INPUT_INFOS)
        .click('#test--add-contact')
        .click('#test--search-contact')
        .typeText('.fullscreen-form--searchInput', INPUT_INFOS)
        .debug()

      const contactsNb = await Selector('.searchList--link').count;
      let containsPreviouslyCreatedContact = false;
      let indexOfPreviouslyCreatedContact = 0;
      for (let index = 0; index <= contactsNb - 1; index++) {
        if (await Selector('.searchList--link').nth(index).innerText === INPUT_INFOS) {
          containsPreviouslyCreatedContact = true;
          indexOfPreviouslyCreatedContact = index;
        }
      }
      await t
        .expect(containsPreviouslyCreatedContact).ok()
      await t
        .click(Selector(".searchList--action").nth(indexOfPreviouslyCreatedContact))
        .click('.fullscreen-form--cancel')
      let userContactsNb = await Selector('.test--contact-link').count;
      for (let index = 0; index <= userContactsNb - 1; index++) {
        // let currentSelector = await Selector('.test--contact-link').nth(index)
        if (await Selector('.test--contact-link').nth(index).innerText === INPUT_INFOS) {
          await t
            .click(await Selector('.test--contact-link').nth(index))
        }
      }
      await t
        .click('.contact-detail--addToFav')
        .click('.goTo')
      userContactsNb = await Selector('.test--contact-link').count;
      let userContainsContact = false
      for (let index = 0; index <= userContactsNb - 1; index++) {
        let currentSelector = await Selector('.test--contact-link').nth(index)
        if (currentSelector.innerText === INPUT_INFOS) [
          userContainsContact = true
        ]
      }
      await t.expect(userContainsContact).notOk()


    })

