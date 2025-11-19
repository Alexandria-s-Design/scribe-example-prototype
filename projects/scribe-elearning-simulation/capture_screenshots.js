/**
 * Automated screenshot capture for Scribe simulation validation.
 * Captures all 7 screens for comparison with actual Scribe.com onboarding.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function captureAllScreens() {
  const htmlFile = path.resolve(__dirname, 'scribe-simulation.html');
  const screenshotsDir = path.join(__dirname, 'validation_screenshots');

  // Create screenshots directory
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  // Launch browser
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  // Open HTML file
  await page.goto(`file:///${htmlFile.replace(/\\/g, '/')}`);
  await page.waitForTimeout(1000);

  console.log('📸 Capturing screenshots...');

  // Screen 1: Cover screen
  console.log('  1/7 - Cover screen');
  await page.waitForSelector('.btn-primary', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '01_cover_screen.png'), fullPage: false });
  await page.waitForTimeout(500);

  // Click "Start Simulation" to go to homepage
  await page.click('.btn-primary');
  await page.waitForTimeout(1000);

  // Screen 2: Homepage (use cases)
  console.log('  2/7 - Homepage with use cases');
  await page.waitForSelector('.use-case-card', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '02_homepage_use_cases.png'), fullPage: false });
  await page.waitForTimeout(500);

  // Click first use case card (Onboard)
  await page.click('.use-case-card:first-child');
  await page.waitForTimeout(1000);

  // Screen 3: Sign in screen
  console.log('  3/7 - Sign in screen');
  await page.waitForSelector('.google-button', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '03_sign_in.png'), fullPage: false });
  await page.waitForTimeout(500);

  // Click "Sign in with Google"
  await page.click('.google-button');
  await page.waitForTimeout(1000);

  // Screen 4: Account chooser
  console.log('  4/7 - Account chooser');
  await page.waitForSelector('.account-option', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '04_account_chooser.png'), fullPage: false });
  await page.waitForTimeout(500);

  // Click the account option (there's only one)
  await page.click('.account-option');
  await page.waitForTimeout(1000);

  // Screen 5: OAuth permissions
  console.log('  5/7 - OAuth permissions');
  await page.waitForSelector('.btn-allow', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '05_oauth_permissions.png'), fullPage: false });
  await page.waitForTimeout(500);

  // Click "Allow"
  await page.click('.btn-allow');
  await page.waitForTimeout(1000);

  // Screen 6: Team naming
  console.log('  6/7 - Team naming');
  await page.waitForSelector('#team-name-input', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '06_team_naming.png'), fullPage: false });
  await page.waitForTimeout(500);

  // Enter team name to enable the submit button
  await page.fill('#team-name-input', 'Test Team');
  await page.waitForTimeout(500);

  // Wait for validation and button to be enabled
  await page.waitForSelector('.btn-submit:not([disabled])', { state: 'visible', timeout: 5000 });

  // Take screenshot with validation success
  await page.screenshot({ path: path.join(screenshotsDir, '06b_team_naming_validated.png'), fullPage: false });

  // Click "Create Team" button (now enabled)
  await page.click('.btn-submit');
  await page.waitForTimeout(1000);

  // Screen 7: Completion screen
  console.log('  7/7 - Completion screen');
  await page.waitForSelector('.completion-screen', { state: 'visible' });
  await page.screenshot({ path: path.join(screenshotsDir, '07_completion.png'), fullPage: false });
  await page.waitForTimeout(500);

  await browser.close();

  console.log(`\n✅ Screenshots saved to '${screenshotsDir}' directory`);
  console.log('📁 Files created:');
  const files = fs.readdirSync(screenshotsDir).filter(f => f.endsWith('.png')).sort();
  files.forEach(filename => {
    const filePath = path.join(screenshotsDir, filename);
    const stats = fs.statSync(filePath);
    const fileSize = (stats.size / 1024).toFixed(1);
    console.log(`   - ${filename} (${fileSize} KB)`);
  });
}

captureAllScreens().catch(console.error);
