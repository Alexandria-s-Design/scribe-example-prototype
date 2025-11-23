/**
 * Retry generating Twitter image #87 using Nano Banana
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY || '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';
const OUTPUT_DIR = 'C:\\Users\\MarieLexisDad\\Modelit-Twitter\\images';
const POST_JSON = 'C:\\Users\\MarieLexisDad\\Modelit-Twitter\\modelit_x_posts.json';

// Post #87 details
const POST_NUMBER = 87;
const CATEGORY = 'Free Resources';
const MAIN_TEXT = "Unlock meaningful discovery in your classroom today with ModelIt K12's FREE library of ready-to-use lessons and interactive sample models. You can instantly explore engaging ways to make abstract concepts concrete—start transforming your teaching experience right now!";

const IMAGE_PROMPT = `Create a vibrant, professional Twitter/X social media post image (1024x1024) for ModelIT K12 educational platform.

Theme: ${CATEGORY}
Key Message: ${MAIN_TEXT}

Visual Style:
- Modern, clean design with educational theme
- Use bright, engaging colors (blues, greens, oranges)
- Include subtle illustrations of students, interactive models, or abstract learning concepts
- Professional typography with clear hierarchy
- Leave space for text overlay in the upper portion
- Background should be dynamic but not overwhelming
- Incorporate subtle geometric patterns or system diagrams
- Educational, inspiring, and professional aesthetic

The image should be eye-catching for social media while maintaining a professional educational brand identity. Focus on visual metaphors for discovery, learning, and hands-on education.`;

/**
 * Generate image using OpenRouter API
 */
function generateImage() {
  return new Promise((resolve, reject) => {
    const requestBody = JSON.stringify({
      model: "google/gemini-2.5-flash-image",
      modalities: ['image', 'text'],
      messages: [{
        role: "user",
        content: IMAGE_PROMPT
      }]
    });

    const options = {
      hostname: 'openrouter.ai',
      port: 443,
      path: '/api/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
        'HTTP-Referer': 'https://modelitk12.com',
        'X-Title': 'ModelIT K12 Twitter Image Generator',
        'Content-Length': Buffer.byteLength(requestBody)
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

          // Extract image from response (same as working script)
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
            resolve(base64Data);
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

    req.write(requestBody);
    req.end();
  });
}

/**
 * Main retry function
 */
async function main() {
  console.log('🔄 Retrying Twitter Image #87');
  console.log('='.repeat(70));
  console.log(`Category: ${CATEGORY}`);
  console.log(`Post: ${MAIN_TEXT.substring(0, 100)}...`);
  console.log('');

  try {
    console.log('Generating image with Nano Banana...');
    const imageData = await generateImage();

    // Save image
    const filename = `Twitter_Post_${String(POST_NUMBER).padStart(3, '0')}_Image.png`;
    const filepath = path.join(OUTPUT_DIR, filename);

    const buffer = Buffer.from(imageData, 'base64');
    fs.writeFileSync(filepath, buffer);

    console.log('');
    console.log('='.repeat(70));
    console.log('✅ Image #87 generated successfully!');
    console.log(`   Saved to: ${filepath}`);
    console.log(`   Size: ${(buffer.length / 1024).toFixed(2)} KB`);
    console.log('='.repeat(70));

  } catch (error) {
    console.error('');
    console.error('='.repeat(70));
    console.error('❌ Generation failed:', error.message);
    console.error('='.repeat(70));
    process.exit(1);
  }
}

// Run
main();
