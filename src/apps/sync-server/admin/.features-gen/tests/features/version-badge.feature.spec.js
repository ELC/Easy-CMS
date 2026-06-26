// Generated from: tests\features\version-badge.feature
import { test } from "playwright-bdd";

test.describe('Platform Admin Panel version badge', () => {

  test('Sync Server version is visible from HAR replay', async ({ Given, Then, page }) => { 
    await Given('the Platform Admin Panel version Web View is open with HAR replay', null, { page }); 
    await Then('the Sync Server version badge shows "0.1.0"', null, { page }); 
  });

});

// == technical section ==

test.use({
  $test: [({}, use) => use(test), { scope: 'test', box: true }],
  $uri: [({}, use) => use('tests\\features\\version-badge.feature'), { scope: 'test', box: true }],
  $bddFileData: [({}, use) => use(bddFileData), { scope: "test", box: true }],
});

const bddFileData = [ // bdd-data-start
  {"pwTestLine":6,"pickleLine":3,"tags":[],"steps":[{"pwStepLine":7,"gherkinStepLine":4,"keywordType":"Context","textWithKeyword":"Given the Platform Admin Panel version Web View is open with HAR replay","stepMatchArguments":[]},{"pwStepLine":8,"gherkinStepLine":5,"keywordType":"Outcome","textWithKeyword":"Then the Sync Server version badge shows \"0.1.0\"","stepMatchArguments":[{"group":{"start":36,"value":"\"0.1.0\"","children":[{"start":37,"value":"0.1.0","children":[{}]},{"children":[{}]}]},"parameterTypeName":"string"}]}]},
]; // bdd-data-end