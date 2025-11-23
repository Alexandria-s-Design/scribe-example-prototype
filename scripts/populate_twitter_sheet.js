/**
 * Populate X/Twitter Google Sheet with posts and imgbb URLs
 * Posting schedule: Monday and Thursday, starting Nov 25, 2024
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// Load credentials
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

// Paths to data files
const POSTS_JSON = 'C:\\Users\\MarieLexisDad\\Modelit-Twitter\\modelit_x_posts.json';
const IMGBB_URLS_JSON = 'C:\\Users\\MarieLexisDad\\scripts\\twitter_imgbb_urls.json';

// X/Twitter Sheet ID
const SPREADSHEET_ID = '1PN3cqv3Pbu7SdnK0W-bTZMwDwDkCHELerjReUzIWMfA';

/**
 * Generate posting dates (Mondays and Thursdays)
 */
function generatePostingDates(startDate, numPosts) {
  const dates = [];
  const start = new Date(startDate);

  // Ensure we start on Monday
  while (start.getDay() !== 1) {
    start.setDate(start.getDate() + 1);
  }

  let currentDate = new Date(start);

  for (let i = 0; i < numPosts; i++) {
    dates.push(new Date(currentDate));

    // Alternate between Monday (+3 days to Thu) and Thursday (+4 days to Mon)
    if (currentDate.getDay() === 1) {
      currentDate.setDate(currentDate.getDate() + 3); // Monday -> Thursday
    } else {
      currentDate.setDate(currentDate.getDate() + 4); // Thursday -> Monday
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
  console.log('🐦 Populating X/Twitter Google Sheet');
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

  // Generate dates starting Nov 25, 2024 (Monday)
  const dates = generatePostingDates('2024-11-25', posts.length);

  // Build rows for Google Sheets
  const rows = [];

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const postNumber = post.post_number || (i + 1);
    const date = formatDate(dates[i]);
    const imageUrl = imageUrls[postNumber] || '';

    // Use full_post which already includes category, main_text, hashtags, and links
    const fullPost = post.full_post || '';

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
  console.log('✅ X/Twitter sheet populated!');
  console.log(`   ${rows.length} posts added`);
  console.log(`   Start date: ${formatDate(dates[0])}`);
  console.log(`   End date: ${formatDate(dates[dates.length - 1])}`);
  console.log(`   URL: https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit`);
  console.log('='.repeat(70));
}

// Run
main().catch(console.error);
