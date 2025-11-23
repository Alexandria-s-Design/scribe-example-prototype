/**
 * Populate Instagram/Facebook Google Sheet with posts and imgbb URLs
 * Posting schedule: Sunday and Wednesday, starting Nov 24, 2024
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// Load credentials
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

// Paths to data files
const POSTS_JSON = 'C:\\Users\\MarieLexisDad\\modelit-facebook\\data\\ModelIT_Instagram_104_Posts_Complete.json';
const IMGBB_URLS_JSON = 'C:\\Users\\MarieLexisDad\\scripts\\instagram_imgbb_urls.json';

// Instagram/Facebook Sheet ID
const SPREADSHEET_ID = '1zsM89g87cSCdJl3nGwiBhwBvbx7PLMg2bdhGX5cXY7w';

/**
 * Generate posting dates (Sundays and Wednesdays)
 */
function generatePostingDates(startDate, numPosts) {
  const dates = [];
  const start = new Date(startDate);

  // Ensure we start on Sunday
  while (start.getDay() !== 0) {
    start.setDate(start.getDate() + 1);
  }

  let currentDate = new Date(start);

  for (let i = 0; i < numPosts; i++) {
    dates.push(new Date(currentDate));

    // Alternate between Sunday (+3 days to Wed) and Wednesday (+4 days to Sun)
    if (currentDate.getDay() === 0) {
      currentDate.setDate(currentDate.getDate() + 3); // Sunday -> Wednesday
    } else {
      currentDate.setDate(currentDate.getDate() + 4); // Wednesday -> Sunday
    }
  }

  return dates;
}

/**
 * Format date for Google Sheets
 */
function formatDate(date) {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  const dayName = days[date.getDay()];
  const month = months[date.getMonth()];
  const day = date.getDate();
  const year = date.getFullYear();

  return `${dayName}, ${month} ${day}, ${year}`;
}

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
 * Main population function
 */
async function main() {
  console.log('📸 Populating Instagram/Facebook Google Sheet');
  console.log('='.repeat(70));

  // Load post data
  const postsData = JSON.parse(fs.readFileSync(POSTS_JSON, 'utf8'));
  const posts = postsData.posts || [];

  // Load imgbb URLs
  const imgbbData = JSON.parse(fs.readFileSync(IMGBB_URLS_JSON, 'utf8'));
  const imageUrls = {};

  imgbbData.images.forEach(img => {
    imageUrls[img.post_number] = img.url;
  });

  console.log(`Loaded ${posts.length} posts`);
  console.log(`Loaded ${Object.keys(imageUrls).length} imgbb URLs\n`);

  // Generate dates starting Nov 24, 2024 (Sunday)
  const dates = generatePostingDates('2024-11-24', posts.length);

  // Build rows for Google Sheets
  const rows = [];

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const postNumber = post.post_number || (i + 1);
    const date = formatDate(dates[i]);
    const imageUrl = imageUrls[postNumber] || '';

    // Caption already includes hashtags, use it directly
    const fullPost = post.caption || '';

    rows.push([
      date,
      fullPost,
      imageUrl,
      'Scheduled'
    ]);
  }

  // Authorize and update sheet
  console.log('Authorizing Google Sheets API...');
  const sheets = await authorize();

  console.log('Updating spreadsheet...');

  // Clear existing data (except headers)
  await sheets.spreadsheets.values.clear({
    spreadsheetId: SPREADSHEET_ID,
    range: 'A2:Z1000'
  });

  // Write new data
  await sheets.spreadsheets.values.update({
    spreadsheetId: SPREADSHEET_ID,
    range: 'A2',
    valueInputOption: 'RAW',
    resource: {
      values: rows
    }
  });

  console.log('\n' + '='.repeat(70));
  console.log('✅ Instagram/Facebook sheet populated!');
  console.log(`   ${rows.length} posts added`);
  console.log(`   Start date: ${formatDate(dates[0])}`);
  console.log(`   End date: ${formatDate(dates[dates.length - 1])}`);
  console.log(`   URL: https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit`);
  console.log('='.repeat(70));
}

// Run
main().catch(console.error);
