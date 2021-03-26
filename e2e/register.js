import { Selector } from 'testcafe';

fixture `Authentication register`
    .page `http://localhost:1337`;

    const util = require('util');
    const exec = util.promisify(require('child_process').exec);

    async function createAffairs() {
        const result = await exec('docker exec backend_enki-api_1 flask create-affairs --number=10 --dept_code=77');
        console.log(result.stdout);
    }


    const structureSelect = Selector('#group');
    const structureOption = structureSelect.find('option');
    const positionSelect = Selector('#position');
    const positionOption = positionSelect.find('option')
    test('Create account maire', async t => {
        // Add affair
        await createAffairs();

        // Test code
        await t
        .click('.login-signupLink')
        .typeText('#email', 'mairie@chelles.fr')
        .typeText('#password', 'azeRTY123#')
        .typeText('#password-confirm', 'azeRTY123#')
        .click('#kc-form-buttons input')
        .click('#hideOnboarding')
        .click('.burger')
        .click('#mobile-prototype')
        .click('.burger')
        await Selector('.userInfoForm')
        await t
        .typeText('#lastName', 'PERNEY')
        .typeText('#firstName', 'Benjamin')
        .click(structureSelect)
        .click(structureOption.withText('Mairie'))
        .click(positionSelect)
        .click(positionOption.withText('Maire'))
        .click('#etablissement')
        .typeText('.fullscreen-form--searchInput', 'Chelles')
        .click('#locationid-77108')
        .click('#submit-register')
        
        await Selector('.dashboard')

        
    });

    test('Create account prefet', async t => {
        // Test code
        await t
        .click('.login-signupLink')
        .typeText('#email', 'prefet@seineetmarne.fr')
        .typeText('#password', 'azeRTY123#')
        .typeText('#password-confirm', 'azeRTY123#')
        .click('#kc-form-buttons input')
        .click('#hideOnboarding')
        .click('.burger')
        .click('#mobile-prototype')
        .click('.burger')
        await Selector('.userInfoForm')
        await t
        .typeText('#lastName', 'PERNEY')
        .typeText('#firstName', 'Benjamin')
        .click(structureSelect)
        .click(structureOption.withText('Prefecture'))
        .click(positionSelect)
        .click(positionOption.withText('Préfet'))
        .click('#etablissement')
        .typeText('.fullscreen-form--searchInput', 'Seine')
        .click('#locationid-77')
        .click('#submit-register')
        
        await Selector('.dashboard')

    })
    