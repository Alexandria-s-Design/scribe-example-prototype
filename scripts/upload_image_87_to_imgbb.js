/**
 * Upload Twitter image #87 to imgbb and update Google Sheet
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { google } = require('googleapis');

const IMGBB_API_KEY = '90e24f774bf4ac71f8c57d3742ede07e';
const IMAGE_PATH = 'C:\\Users\\MarieLexisDad\\Modelit-Twitter\\images\\Twitter_Post_087_Image.png';
const SPREADSHEET_ID = '1PN3cqv3Pbu7SdnK0W-bTZMwDwDkCHELerjReUzIWMfA';
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

/**
 * Upload to imgbb
 */
function uploadToImgbb() {
  return new Promise((resolve, reject) => {
    const imageBuffer = fs.readFileSync(IMAGE_PATH);
    const base64Image = imageBuffer.toString('base64');

    const formData = `key=${IMGBB_API_KEY}&image=${encodeURIComponent(base64Image)}&name=Twitter-Post-087-Image`;

    const options = {
      hostname: 'api.imgbb.com',
      port: 443,
      path: '/1/upload',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(formData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.success) {
            resolve(result.data.url);
          } else {
            reject(new Error(`imgbb upload failed: ${data}`));
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.write(formData);
    req.end();
  });
}

/**
 * Authorize Google Sheets
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
 * Update Google Sheet row 87 with image URL
 */
async function updateSheet(imageUrl) {
  const sheets = await authorize();

  // Row 87 is at index 88 (header row + 87 data rows)
  // Column C (Image URL) is the 3rd column
  await sheets.spreadsheets.values.update({
    spreadsheetId: SPREADSHEET_ID,
    range: 'C88',
    valueInputOption: 'RAW',
    resource: {
      values: [[imageUrl]]
    }
  });
}

/**
 * Main function
 */
async function main() {
  console.log('📤 Uploading Twitter Image #87');
  console.log('='.repeat(70));

  try {
    console.log('Uploading to imgbb...');
    const imageUrl = await uploadToImgbb();
    console.log(`✅ Uploaded: ${imageUrl}`);

    console.log('\nUpdating Google Sheet...');
    await updateSheet(imageUrl);
    console.log('✅ Sheet updated!');

    console.log('\n' + '='.repeat(70));
    console.log('✅ Image #87 complete!');
    console.log(`   URL: ${imageUrl}`);
    console.log('='.repeat(70));

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

// Run
main();
