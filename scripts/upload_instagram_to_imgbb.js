/**
 * Upload all 104 Instagram images to imgbb
 * Node.js version - works in current environment
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// imgbb API key
const IMGBB_API_KEY = '90e24f774bf4ac71f8c57d3742ede07e';

// Paths
const IMAGES_DIR = 'C:\\Users\\MarieLexisDad\\modelit-facebook\\images';
const OUTPUT_FILE = 'C:\\Users\\MarieLexisDad\\scripts\\instagram_imgbb_urls.json';

/**
 * Upload single image to imgbb
 */
function uploadToImgbb(imagePath, imageName) {
  return new Promise((resolve, reject) => {
    // Read image file
    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString('base64');

    // Prepare form data
    const formData = `key=${IMGBB_API_KEY}&image=${encodeURIComponent(base64Image)}&name=${encodeURIComponent(imageName)}`;

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
            resolve({
              url: result.data.url,
              display_url: result.data.display_url,
              delete_url: result.data.delete_url,
              size: result.data.size,
              width: result.data.width,
              height: result.data.height
            });
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
 * Sleep function for rate limiting
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main upload function
 */
async function main() {
  console.log('📸 Instagram Image Upload to imgbb');
  console.log('='.repeat(70));

  // Get all image files
  const imageFiles = fs.readdirSync(IMAGES_DIR)
    .filter(f => f.match(/Post_\d+_Image\.png/))
    .sort();

  console.log(`Found ${imageFiles.length} Instagram images\n`);

  const results = [];
  const failed = [];

  for (let i = 0; i < imageFiles.length; i++) {
    const filename = imageFiles[i];
    const imagePath = path.join(IMAGES_DIR, filename);
    const postNumber = i + 1;

    process.stdout.write(`[${postNumber}/${imageFiles.length}] Uploading ${filename}... `);

    try {
      const result = await uploadToImgbb(imagePath, path.parse(filename).name);

      results.push({
        post_number: postNumber,
        filename: filename,
        url: result.url,
        display_url: result.display_url,
        delete_url: result.delete_url,
        size: result.size,
        width: result.width,
        height: result.height
      });

      console.log(`✅ ${result.url}`);

      // Rate limiting - 2 second delay
      if (i < imageFiles.length - 1) {
        await sleep(2000);
      }
    } catch (error) {
      console.log(`❌ Failed: ${error.message}`);
      failed.push({
        filename: filename,
        error: error.message
      });
    }
  }

  // Save results
  const outputData = {
    total_images: imageFiles.length,
    successful: results.length,
    failed: failed.length,
    images: results,
    failures: failed
  };

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(outputData, null, 2));

  console.log('\n' + '='.repeat(70));
  console.log('✅ Upload complete!');
  console.log(`   Successful: ${results.length}/${imageFiles.length}`);
  console.log(`   Failed: ${failed.length}`);
  console.log(`   Results saved to: ${OUTPUT_FILE}`);
  console.log('='.repeat(70));
}

// Run
main().catch(console.error);
