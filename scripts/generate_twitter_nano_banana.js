/**
 * Generate 104 X/Twitter images using Nano Banana (Gemini 2.5 Flash Image)
 * via OpenRouter API
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;

if (!OPENROUTER_API_KEY) {
  console.error('❌ OPENROUTER_API_KEY not found in .env');
  process.exit(1);
}

// Paths
const POSTS_JSON = 'C:\\Users\\MarieLexisDad\\Modelit-Twitter\\modelit_x_posts.json';
const OUTPUT_DIR = 'C:\\Users\\MarieLexisDad\\Modelit-Twitter\\images';
const LOG_FILE = path.join(OUTPUT_DIR, 'generation_log.json');

/**
 * Generate image using Nano Banana via OpenRouter
 */
function generateNanoBananaImage(prompt) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      model: 'google/gemini-2.5-flash-image',
      modalities: ['image', 'text'],
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const options = {
      hostname: 'openrouter.ai',
      port: 443,
      path: '/api/v1/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://modelitk12.com',
        'X-Title': 'ModelIT X/Twitter Image Generator',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 120000
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);

          // Extract image from response
          const images = result.choices?.[0]?.message?.images;

          if (!images || images.length === 0) {
            reject(new Error('No images in response'));
            return;
          }

          const imgData = images[0];
          let imgUrl = '';

          // Handle different response formats
          if (typeof imgData === 'object') {
            imgUrl = imgData.image_url?.url || imgData.url || '';
          } else if (typeof imgData === 'string') {
            imgUrl = imgData;
          }

          // Decode base64 image
          if (imgUrl && imgUrl.startsWith('data:image')) {
            const base64Data = imgUrl.split(',')[1];
            const imageBuffer = Buffer.from(base64Data, 'base64');
            resolve(imageBuffer);
          } else {
            reject(new Error(`Invalid image URL format: ${imgUrl}`));
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    req.write(payload);
    req.end();
  });
}

/**
 * Create image prompt for Twitter post
 */
function createTwitterPrompt(post) {
  const category = post.category || 'General';
  const mainText = (post.main_text || '').substring(0, 200);

  return `Create a bold, eye-catching square image (1024x1024) optimized for Twitter/X social media.

Content Category: ${category}
Post Topic: ${mainText}

Design Requirements:
- Modern, professional design for Twitter/X feed
- High contrast for mobile viewing
- Deep blue (#0f6de6) as primary brand color
- Clean white or light background
- Bold, minimalist aesthetic
- Scientific/educational theme
- Abstract visual elements: interconnected systems, modeling, STEM concepts
- Professional enough for educators
- Engaging enough for social media
- Square 1024x1024px format
- NO TEXT in the image (text will be in the tweet)

Style: Modern minimalist, scientific illustration, educational technology aesthetic, Twitter-optimized`;
}

/**
 * Sleep for rate limiting
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main generation function
 */
async function main() {
  console.log('📱 X/Twitter Image Generation with Nano Banana');
  console.log('='.repeat(70));

  // Create output directory
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  // Load posts
  const data = JSON.parse(fs.readFileSync(POSTS_JSON, 'utf8'));
  const posts = data.posts || [];

  console.log(`Found ${posts.length} X/Twitter posts\n`);

  const results = [];
  const failed = [];

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const postNumber = post.post_number || (i + 1);
    const filename = `Twitter_Post_${String(postNumber).padStart(3, '0')}_Image.png`;
    const filepath = path.join(OUTPUT_DIR, filename);

    // Skip if exists
    if (fs.existsSync(filepath)) {
      console.log(`[${i + 1}/${posts.length}] ${filename} already exists ✓`);
      results.push({
        post_number: postNumber,
        filename: filename,
        status: 'already_exists'
      });
      continue;
    }

    process.stdout.write(`[${i + 1}/${posts.length}] Generating ${filename}... `);

    try {
      // Create prompt
      const prompt = createTwitterPrompt(post);

      // Generate image
      const imageBuffer = await generateNanoBananaImage(prompt);

      // Save image
      fs.writeFileSync(filepath, imageBuffer);

      console.log('✅');

      results.push({
        post_number: postNumber,
        filename: filename,
        status: 'generated',
        filepath: filepath
      });

      // Rate limiting - 5 second delay
      if (i < posts.length - 1) {
        await sleep(5000);
      }
    } catch (error) {
      console.log(`❌ Failed: ${error.message}`);
      failed.push({
        post_number: postNumber,
        filename: filename,
        error: error.message
      });
    }
  }

  // Save log
  const logData = {
    total_posts: posts.length,
    successful: results.length,
    failed: failed.length,
    results: results,
    failures: failed
  };

  fs.writeFileSync(LOG_FILE, JSON.stringify(logData, null, 2));

  console.log('\n' + '='.repeat(70));
  console.log('✅ Generation complete!');
  console.log(`   Successful: ${results.length}/${posts.length}`);
  console.log(`   Failed: ${failed.length}`);
  console.log(`   Log saved to: ${LOG_FILE}`);
  console.log('='.repeat(70));
}

// Run
main().catch(console.error);
