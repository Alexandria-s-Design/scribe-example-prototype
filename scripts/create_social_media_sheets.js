/**
 * Create three Google Sheets for social media campaigns
 * 1. Instagram/Facebook Master Tracker
 * 2. X/Twitter Master Tracker
 * 3. Social Media Analytics Dashboard
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// Load credentials
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

/**
 * Authorize and get Google Sheets client
 */
async function authorize() {
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));

  const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

  oAuth2Client.setCredentials(token);
  return google.sheets({ version: 'v4', auth: oAuth2Client });
}

/**
 * Create Instagram/Facebook sheet
 */
async function createInstagramSheet(sheets) {
  console.log('Creating Instagram/Facebook Master Tracker...');

  const resource = {
    properties: {
      title: 'ModelIT Instagram/Facebook 2025-2026'
    },
    sheets: [{
      properties: {
        title: 'Posts',
        gridProperties: {
          frozenRowCount: 1
        }
      },
      data: [{
        rowData: [{
          values: [
            { userEnteredValue: { stringValue: 'Date' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Post Content' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Image URL' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Status' }, userEnteredFormat: { textFormat: { bold: true } } }
          ]
        }]
      }]
    }]
  };

  const response = await sheets.spreadsheets.create({ resource });
  const spreadsheetId = response.data.spreadsheetId;
  const sheetId = response.data.sheets[0].properties.sheetId;

  // Set column widths
  await sheets.spreadsheets.batchUpdate({
    spreadsheetId,
    resource: {
      requests: [{
        updateDimensionProperties: {
          range: {
            sheetId: sheetId,
            dimension: 'COLUMNS',
            startIndex: 0,
            endIndex: 4
          },
          properties: {
            pixelSize: 200
          },
          fields: 'pixelSize'
        }
      }]
    }
  });

  console.log(`✅ Instagram/Facebook sheet created: ${spreadsheetId}`);
  return spreadsheetId;
}

/**
 * Create X/Twitter sheet
 */
async function createTwitterSheet(sheets) {
  console.log('Creating X/Twitter Master Tracker...');

  const resource = {
    properties: {
      title: 'ModelIT X/Twitter 2025-2026'
    },
    sheets: [{
      properties: {
        title: 'Posts',
        gridProperties: {
          frozenRowCount: 1
        }
      },
      data: [{
        rowData: [{
          values: [
            { userEnteredValue: { stringValue: 'Date' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Post Content' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Image URL' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Status' }, userEnteredFormat: { textFormat: { bold: true } } }
          ]
        }]
      }]
    }]
  };

  const response = await sheets.spreadsheets.create({ resource });
  const spreadsheetId = response.data.spreadsheetId;
  const sheetId = response.data.sheets[0].properties.sheetId;

  // Set column widths
  await sheets.spreadsheets.batchUpdate({
    spreadsheetId,
    resource: {
      requests: [{
        updateDimensionProperties: {
          range: {
            sheetId: sheetId,
            dimension: 'COLUMNS',
            startIndex: 0,
            endIndex: 4
          },
          properties: {
            pixelSize: 200
          },
          fields: 'pixelSize'
        }
      }]
    }
  });

  console.log(`✅ X/Twitter sheet created: ${spreadsheetId}`);
  return spreadsheetId;
}

/**
 * Create Analytics Dashboard
 */
async function createAnalyticsSheet(sheets) {
  console.log('Creating Analytics Dashboard...');

  const resource = {
    properties: {
      title: 'ModelIT Social Media Analytics 2025-2026'
    },
    sheets: [{
      properties: {
        title: 'Overview',
        gridProperties: {
          frozenRowCount: 1
        }
      },
      data: [{
        rowData: [{
          values: [
            { userEnteredValue: { stringValue: 'Metric' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Instagram/Facebook' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'X/Twitter' }, userEnteredFormat: { textFormat: { bold: true } } },
            { userEnteredValue: { stringValue: 'Total' }, userEnteredFormat: { textFormat: { bold: true } } }
          ]
        }]
      }]
    }]
  };

  const response = await sheets.spreadsheets.create({ resource });
  const spreadsheetId = response.data.spreadsheetId;

  console.log(`✅ Analytics Dashboard created: ${spreadsheetId}`);
  return spreadsheetId;
}

/**
 * Main function
 */
async function main() {
  console.log('🎯 Creating Google Sheets for Social Media Campaigns');
  console.log('='.repeat(70));

  const sheets = await authorize();

  const instagramId = await createInstagramSheet(sheets);
  const twitterId = await createTwitterSheet(sheets);
  const analyticsId = await createAnalyticsSheet(sheets);

  // Save IDs to file for population scripts
  const ids = {
    instagram_facebook: instagramId,
    twitter: twitterId,
    analytics: analyticsId,
    created_at: new Date().toISOString()
  };

  fs.writeFileSync(
    path.join(__dirname, 'sheet_ids.json'),
    JSON.stringify(ids, null, 2)
  );

  console.log('\n' + '='.repeat(70));
  console.log('✅ All sheets created successfully!');
  console.log('='.repeat(70));
  console.log('\n📊 Spreadsheet Links:');
  console.log(`\n1. Instagram/Facebook:`);
  console.log(`   https://docs.google.com/spreadsheets/d/${instagramId}/edit`);
  console.log(`\n2. X/Twitter:`);
  console.log(`   https://docs.google.com/spreadsheets/d/${twitterId}/edit`);
  console.log(`\n3. Analytics Dashboard:`);
  console.log(`   https://docs.google.com/spreadsheets/d/${analyticsId}/edit`);
  console.log('\n' + '='.repeat(70));
  console.log('📄 Sheet IDs saved to: sheet_ids.json');
  console.log('='.repeat(70));
}

// Run
main().catch(console.error);
