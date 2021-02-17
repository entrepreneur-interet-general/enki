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

