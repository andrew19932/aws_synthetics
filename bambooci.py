var synthetics = require('Synthetics');
var AWS = require('aws-sdk'),
    region = "eu-west-1";

var client = new AWS.SecretsManager({region: region});
const log = require('SyntheticsLogger');

function getAwsSecret(secretName) {
    return client.getSecretValue({ SecretId: secretName }).promise();
}

// Create a async function to use the Promise
// Top level await is a proposal
async function getAwsSecretAsync (secretName) {
    var error;
    var response = await getAwsSecret(secretName).catch(err => (error = err));
    return [error, response];
}
const flowBuilderBlueprint = async function () {
    let url = "https://ci.wolterskluwer.io/";


    let secret = await synthetics.executeStep('load creds', async function (timeoutInMillis = 30000) {
        var [error, secret] = await getAwsSecretAsync('username');
        return JSON.parse(secret.SecretString);
    });
    let page = await synthetics.getPage();
    log.info(secret);
    await synthetics.executeStep('navigateToUrl', async function (timeoutInMillis = 30000) {
        await page.goto(url, {waitUntil: ['load', 'networkidle0'], timeout: timeoutInMillis});
    });
    // Execute customer steps
    await synthetics.executeStep('customerActions', async function () {
        await page.type("[id='loginForm_os_username']", secret.username);
        try {
            await synthetics.takeScreenshot("input", 'result');
        } catch (ex) {
            synthetics.addExecutionError('Unable to capture screenshot.', ex);
        }

        await page.type("[id='loginForm_os_password']", secret.password);
        try {
            await synthetics.takeScreenshot("input", 'result');
        } catch (ex) {
            synthetics.addExecutionError('Unable to capture screenshot.', ex);
        }

        await page.waitForSelector("[id='loginForm_save']", {timeout: 30000});
        await page.click("[id='loginForm_save']");
        try {
            await synthetics.takeScreenshot("click", 'result');
        } catch (ex) {
            synthetics.addExecutionError('Unable to capture screenshot.', ex);
        }

        await page.waitForSelector("[id='allProjects']", { timeout: 30000 });
        await page.click("[id='allProjects']");
        try {
            await synthetics.takeScreenshot("click", 'result');
        } catch(ex) {
            synthetics.addExecutionError('Unable to capture screenshot.', ex);
        }

        await page.waitForSelector("[id='myBamboo']", { timeout: 30000 });
        await page.click("[id='myBamboo']");
        try {
            await synthetics.takeScreenshot("click", 'result');
        } catch(ex) {
            synthetics.addExecutionError('Unable to capture screenshot.', ex);
        }

        await page.waitForSelector("[alt='Kovalenko, Andrii']", { timeout: 30000 });
        try {
            await synthetics.takeScreenshot("verifySelector", 'result');
        } catch(ex) {
            synthetics.addExecutionError('Unable to capture screenshot.', ex);
        }


    });

};
exports.handler = async () => {
    return await flowBuilderBlueprint();
};
