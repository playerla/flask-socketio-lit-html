import { Selector } from 'testcafe';

fixture `Testing user webcomponent`
    .page `http://localhost:5000`;

test('First user', async t => {
    await t
        .typeText('#username', 'John Smith')
        .click('#submit-button')
        .expect(Selector('ul').find('user-item').innerText).contains('John Smith');
});

test('Second user', async t => {
    await t
        .typeText('#username', 'Will Bill')
        .click('#submit-button')
        .expect(Selector('#user2').find('user-item').innerText).contains('Will Bill');
    const userInListText = await Selector('ul').find('user-item').innerText;
    console.log(userInListText);
    // await t.debug();
});

test('Change second user', async t => {
    await t
        .typeText('#username', 'new name')
        .click('#change-button')
        .expect(Selector('#user2').find('user-item').innerText).contains('new name');
});

test('Empty username', async t => {
    await t
        .click('#username')
        .pressKey('ctrl+a delete')
        .click('#change-button')
        .expect(Selector('#user2').find('user-item').innerText).eql('undefined');
});

test('Local user with event', async t => {
    await t
        .typeText('#username', 'Bull Will')
        .click('#submit-button')
        .expect(Selector('#latest').find('user-item').innerText).contains('Bull Will');
});