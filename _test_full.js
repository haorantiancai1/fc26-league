const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage();
  
  const errors = [];
  page.on('pageerror', err => {
    errors.push({type: 'pageerror', message: err.message, stack: err.stack});
  });
  
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push({type: 'console', text: msg.text(), location: msg.location()});
    }
  });
  
  await page.goto('http://localhost:8099', {waitUntil: 'networkidle'});
  
  // Try login
  await page.fill('#login-name', '浩然');
  await page.fill('#login-pass', '123456');
  await page.click('.login-btn');
  await page.waitForTimeout(3000);
  
  const title = await page.title();
  const body = await page.evaluate(() => document.body.innerText.substring(0, 500));
  const url = page.url();
  
  console.log('=== RESULTS ===');
  console.log('Title:', title);
  console.log('URL:', url);
  console.log('Body:', body.substring(0, 300));
  console.log('=== PAGE ERRORS ===');
  for (const e of errors) {
    console.log('PAGE ERROR:', e.message);
    if (e.stack) console.log('  Stack:', e.stack.substring(0, 200));
  }
  console.log('=== CONSOLE ERRORS ===');
  for (const e of consoleErrors) {
    console.log('CONSOLE ERROR:', e.text, '| URL:', e.location.url, '| Line:', e.location.lineNumber);
  }
  
  await browser.close();
})();
