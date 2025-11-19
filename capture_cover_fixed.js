/**
 * Capture updated cover screen screenshot after logo size fix (50px → 80px)
 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const htmlFile = path.resolve(__dirname, 'scribe-simulation.html');
  const screenshotPath = path.join(__dirname, 'validation_screenshots', '01_cover_screen_FIXED.png');

  console.log('📸 Capturing updated cover screen with 80px logo...');

  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  await page.goto(`file:///${htmlFile.replace(/\\/g, '/')}`);
  await page.waitForTimeout(1000);
  await page.waitForSelector('.btn-primary', { state: 'visible' });

  await page.screenshot({ path: screenshotPath });

  console.log(`✅ Screenshot saved: ${screenshotPath}`);
  await browser.close();
})();
