import { Selector } from 'testcafe';

fixture `Authentication register`
    .page `http://localhost:1337`;

    const structureSelect = Selector('#structure');
    const structureOption = structureSelect.find('option');
    const positionSelect = Selector('#position');
    const positionOption = positionSelect.find('option')
    test('Create account maire', async t => {

        // Test code
        await t
        .click('.login-signupLink')
        .typeText('#email', 'mairie@chelles.fr')
        .typeText('#password', 'azeRTY123#')
        .typeText('#password-confirm', 'azeRTY123#')
        .click('#kc-form-buttons input')

        await Selector('.userInfoForm')
        await t
        .typeText('#lastName', 'PERNEY')
        .typeText('#firstName', 'Benjamin')
        .click(structureSelect)
        .click(structureOption.withText('Mairie'))
        .click(positionSelect)
        .click(positionOption.withText('Maire'))
        .click('#location')
        .typeText('.fullscreen-form--searchInput', 'Chelles')
        .click('#chelles')
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

        await Selector('.userInfoForm')
        await t
        .typeText('#lastName', 'PERNEY')
        .typeText('#firstName', 'Benjamin')
        .click(structureSelect)
        .click(structureOption.withText('Prefecture'))
        .click(positionSelect)
        .click(positionOption.withText('Préfet'))
        .click('#location')
        .typeText('.fullscreen-form--searchInput', 'Seine')
        .click('#seine-et-marne')
        .click('#submit-register')
        
        await Selector('.dashboard')

    })
    
    
    
    
    /* 
            .typeText('#username', 'mairie@chelles.fr')
            .typeText('#password', 'azeRTY123#')
            .click('#kc-login')
    
            await Selector('.userInfoForm')
            await t
            .typeText('#lastName', 'PERNEY')
            .typeText('#firstName', 'Benjamin')
            .click(fonctionSelect)
            .click(fonctionOption.withText('Préfet'))
            .expect(fonctionSelect.value).eql('prefet') */