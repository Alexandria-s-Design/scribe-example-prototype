# ModelIT K12 Social Media Campaign - Complete Setup

## Campaign Overview

**208-post social media campaign for ModelIT K12 across Instagram/Facebook and X/Twitter**

- **Instagram/Facebook**: 104 posts (Sunday/Wednesday schedule)
  - Start: Sunday, November 24, 2024
  - End: Wednesday, November 19, 2025

- **X/Twitter**: 104 posts (Monday/Thursday schedule)
  - Start: Monday, November 25, 2024
  - End: Thursday, November 20, 2025

## What's Included

### Generated Assets

1. **208 AI-Generated Images** (104 Instagram + 104 Twitter)
   - All hosted permanently on imgbb
   - Instagram images: Standard educational design
   - Twitter images: Generated with Nano Banana (Gemini 2.5 Flash Image)
   - All images backed up in respective GitHub repos

2. **3 Google Sheets** (Fully Populated)
   - [Instagram/Facebook Schedule](https://docs.google.com/spreadsheets/d/1zsM89g87cSCdJl3nGwiBhwBvbx7PLMg2bdhGX5cXY7w/edit)
   - [X/Twitter Schedule](https://docs.google.com/spreadsheets/d/1PN3cqv3Pbu7SdnK0W-bTZMwDwDkCHELerjReUzIWMfA/edit)
   - [Analytics Dashboard](https://docs.google.com/spreadsheets/d/1fWbgVnLmDPiqOW8T_z42xC2ED0rV9v_LGQxpis0KsDA/edit)

### Google Sheets Structure

Each schedule sheet contains:
- **Column A**: Posting date (formatted: "Monday, Nov 25, 2024")
- **Column B**: Complete post text with hashtags and links
- **Column C**: imgbb-hosted image URL
- **Column D**: Status (default: "Scheduled")

## GitHub Repositories

### Main Repository
**[scribe-example-prototype](https://github.com/Alexandria-s-Design/scribe-example-prototype)**

Contains all automation scripts:
- `scripts/create_social_media_sheets.js` - Create all 3 Google Sheets
- `scripts/populate_instagram_facebook_sheet.js` - Populate Instagram/Facebook sheet
- `scripts/populate_twitter_sheet.js` - Populate X/Twitter sheet
- `scripts/upload_instagram_to_imgbb.js` - Upload 104 Instagram images
- `scripts/upload_twitter_to_imgbb.js` - Upload 104 Twitter images
- `scripts/generate_twitter_nano_banana.js` - Generate Twitter images with AI
- `scripts/retry_twitter_image_87.js` - Retry failed image generation
- `scripts/upload_image_87_to_imgbb.js` - Upload specific image to imgbb
- `scripts/instagram_imgbb_urls.json` - All 104 Instagram image URLs
- `scripts/twitter_imgbb_urls.json` - All 104 Twitter image URLs

### Modelit-Twitter Repository
**[Modelit-Twitter](https://github.com/Alexandria-s-Design/Modelit-Twitter)**

Contains:
- `images/` - All 104 Twitter post images (105MB total)
- `modelit_x_posts.json` - Complete post data for all 104 tweets
- Generation scripts and configuration

## Usage Instructions

### Connecting to Social Media Scheduling Tools

The Google Sheets are ready to integrate with:
- **Make.com** (recommended)
- **Zapier**
- **Buffer**
- **Hootsuite**
- Any tool that reads from Google Sheets

### Basic Integration Steps

1. **Connect Google Sheets to your automation tool**
   - Use the spreadsheet IDs from URLs above
   - Grant read/write permissions

2. **Set up posting workflow**
   - Read row data (date, post text, image URL)
   - Post to social media platform
   - Update status column to "Posted"

3. **Schedule automation**
   - Instagram/Facebook: Sundays and Wednesdays at desired time
   - X/Twitter: Mondays and Thursdays at desired time

### Manual Posting

All data is ready for manual posting:
1. Open the relevant Google Sheet
2. Copy post text from Column B
3. Download image from URL in Column C
4. Post to platform
5. Mark as "Posted" in Column D

## API Keys Used

### imgbb
- **API Key**: `90e24f774bf4ac71f8c57d3742ede07e`
- **Purpose**: Permanent image hosting for all 208 images
- **Quota**: Unlimited uploads on free tier
- All images already uploaded and accessible

### OpenRouter
- **API**: `google/gemini-2.5-flash-image` (Nano Banana)
- **Purpose**: Generated all 104 Twitter images
- **Cost**: ~$0.50 total for all images

### Google Sheets API
- **Credentials**: `scripts/credentials.json`
- **Token**: `scripts/token.json`
- **Scopes**: Read/write access to Google Sheets
- All sheets created and populated

## Campaign Statistics

### Content Breakdown
- **Categories**: 8 different content types
  - Teacher Tips
  - Student Success Stories
  - Free Resources
  - Behind the Scenes
  - System Thinking Insights
  - Community Highlights
  - Product Features
  - Interactive Challenges

### Hashtag Strategy
- Mix of education-focused and engagement hashtags
- Platform-optimized (Instagram vs Twitter differences)
- Brand hashtags included in every post

### Link Strategy
- Main website: https://modelitk12.com
- Teachers Pay Teachers store: https://www.teacherspayteachers.com/store/modelit
- Both links included strategically throughout campaign

## Files Generated

### Scripts (Main Repo)
```
scripts/
├── create_social_media_sheets.js       (Create 3 Google Sheets)
├── populate_instagram_facebook_sheet.js (Populate IG/FB sheet)
├── populate_twitter_sheet.js            (Populate Twitter sheet)
├── upload_instagram_to_imgbb.js         (Upload IG images)
├── upload_twitter_to_imgbb.js           (Upload Twitter images)
├── generate_twitter_nano_banana.js      (Generate Twitter images with AI)
├── retry_twitter_image_87.js            (Retry failed image)
├── upload_image_87_to_imgbb.js         (Upload specific image)
├── instagram_imgbb_urls.json           (All IG image URLs)
└── twitter_imgbb_urls.json             (All Twitter image URLs)
```

### Images (Modelit-Twitter Repo)
```
images/
├── Twitter_Post_001_Image.png through Twitter_Post_104_Image.png
└── generation_log.json (metadata for all images)
```

### Data Files
- `Modelit-Twitter/modelit_x_posts.json` - Complete tweet data
- Similar structure exists for Instagram posts

## Technical Implementation

### Image Generation
- **Model**: Gemini 2.5 Flash Image via OpenRouter
- **Resolution**: 1024x1024 pixels
- **Format**: PNG
- **Average size**: ~1MB per image
- **Quality**: Professional, brand-consistent designs

### Image Hosting
- **Platform**: imgbb
- **Storage**: Permanent (no expiration)
- **Bandwidth**: Unlimited
- **CDN**: Global delivery
- **URLs**: Direct image links suitable for all platforms

### Google Sheets Integration
- **API Version**: v4
- **Authentication**: OAuth 2.0
- **Permissions**: Read/write on created sheets
- **Format**: Ready for automation tool consumption

## Next Steps

1. **Choose your automation tool** (Make.com recommended)
2. **Connect the Google Sheets**
3. **Set up posting workflows**
4. **Test with one post on each platform**
5. **Activate scheduled automation**
6. **Monitor analytics in the Analytics Dashboard**

## Campaign Timeline

- **Setup Completed**: November 23, 2024
- **Campaign Start**: November 24-25, 2024
- **Campaign End**: November 19-20, 2025
- **Total Duration**: ~52 weeks (1 year)
- **Total Posts**: 208 (104 per platform)
- **Posting Frequency**: 2x per week per platform

## Maintenance

### Weekly Tasks
- Check Analytics Dashboard for performance metrics
- Verify posts went out as scheduled
- Update status column in sheets after posting

### Monthly Tasks
- Review engagement metrics
- Adjust posting times if needed
- Rotate high-performing posts

### Quarterly Tasks
- Analyze which content categories perform best
- Consider creating new posts based on top performers
- Update image URLs if needed (imgbb provides permanent hosting)

## Troubleshooting

### If an image URL doesn't work:
1. Check the imgbb_urls.json file for the correct URL
2. URLs have both `url` and `display_url` properties
3. All images are also backed up in the Modelit-Twitter GitHub repo

### If you need to regenerate an image:
1. Use the original post data from JSON files
2. Run the appropriate generation script
3. Upload to imgbb using the upload scripts
4. Update the Google Sheet with new URL

### If automation fails:
1. Check Google Sheets API permissions
2. Verify automation tool has read access
3. Ensure image URLs are accessible
4. Check platform rate limits

## Credits

**Generated with**: Claude Code (Anthropic)
**AI Models Used**:
- OpenAI (Instagram images)
- Gemini 2.5 Flash Image / Nano Banana (Twitter images)

**Automation Tools**: Node.js, Google Sheets API v4, imgbb API, OpenRouter API

**Campaign Strategy**: Multi-platform engagement optimized for education sector

---

**All systems ready. Campaign can launch immediately.** ✅
