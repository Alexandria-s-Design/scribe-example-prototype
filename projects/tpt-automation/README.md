# TPT Automation System - Teachers Pay Teachers Product Generator

**Status**: ✅ Fully Operational | **Cost**: FREE (using Google Gemini)

Complete automation system for creating Teachers Pay Teachers (TPT) educational products using AI image generation, PowerPoint/Word, and validation workflows.

## 🎯 What This System Does

Creates production-ready TPT products in **20-30 minutes** with:
- FREE AI-generated images (Google Gemini 2.5 Flash Image)
- Professional PowerPoint/Word layouts
- Automated validation and quality checks
- Beautiful, print-ready designs

## 📊 Current Products Created

### 1. Ecosystem Coloring Sheet - 3rd Grade
- **8 AI-generated images** (Oak tree, Deer, Rabbit, Mushrooms, Sun, Rocks, Pond, Grass)
- 4×2 grid layout, 1.5" × 1.5" images
- Professional formatting, ready to print
- **Cost**: $0.00 (images generated FREE)

### 2. Ecosystem Word Search - 3rd Grade
- **15×15 grid** with 10 ecosystem vocabulary words
- Forest green theme, professional design
- Checkbox tracking, helpful instructions
- 2-column word list layout

## 🚀 Quick Start - Create a TPT Product

### Step 1: Generate AI Images with Gemini (FREE!)

```bash
cd C:/Users/MarieLexisDad/projects/tpt-automation
python generate_gemini_official.py
```

**What it does:**
- Generates images using Google Gemini 2.5 Flash Image API
- Completely FREE (no cost per image)
- Creates high-quality coloring sheet artwork
- Saves to `ecosystem-artwork/` directory

**Requirements:**
- `pip install google-genai`
- Google API key in `.env` as `GOOGLE_API_KEY`
- Get API key: https://aistudio.google.com/apikey

**Script generates:**
- Black & white line art for coloring
- Perfect for 3rd grade level
- Educational, age-appropriate
- TPT marketplace ready

### Step 2: Create PowerPoint Product

**Option A: Coloring Sheet**
```bash
python create_pptx_coloring_sheet.py
```

**Option B: Word Search**
```bash
python create_word_search.py
```

**What it creates:**
- Professional PowerPoint (PPTX) file
- US Letter size (8.5" × 11")
- Perfect spacing and layout
- Print-ready design

### Step 3: Upload and Share

```bash
python upload_to_onedrive.py  # For coloring sheet
python upload_word_search.py   # For word search
```

**Output:**
- Shareable Google Drive link
- Direct download link
- Can be opened in PowerPoint or Google Slides

## 📁 Project Structure

```
tpt-automation/
├── README.md                           # This file
├── TPT_AUTOMATION_INSTRUCTIONS.md      # Detailed step-by-step guide
├── PROCESS_DOCUMENTATION.md            # Complete automation workflow
│
├── generate_gemini_official.py         # ✅ WORKING - Generate FREE images
├── create_pptx_coloring_sheet.py      # Create coloring sheet PowerPoint
├── create_word_search.py              # Create word search PowerPoint
├── upload_to_onedrive.py              # Upload to Drive/OneDrive
├── upload_word_search.py              # Upload word search
│
├── check_current_slides_state.py      # Validation: Check slide layout
├── rebuild_slides_correctly.py        # Fix broken slide layouts
│
├── ecosystem-artwork/                  # Generated images directory
│   ├── oak_tree.png
│   ├── deer.png
│   ├── rabbit.png
│   ├── mushrooms.png
│   ├── sun.png
│   ├── rocks.png
│   ├── pond.png
│   └── grass_flowers.png
│
└── validation/                         # Validation system (from agent)
    ├── analyze_slides_layout.py
    ├── fix_slides_images_only.py
    ├── tpt_quality_standards.md
    └── REUSABLE_VALIDATION_WORKFLOW.md
```

## 🎨 Image Generation - Google Gemini 2.5 Flash Image

**Why Gemini?**
- **100% FREE** (vs $0.04/image with OpenAI DALL-E)
- State-of-the-art quality (released August 2025)
- Perfect for TPT products (coloring pages, illustrations)
- Unlimited variations at no cost

**Verified Working Script:**
```python
from google import genai
from google.genai import types
import os

os.environ['GEMINI_API_KEY'] = os.getenv('GOOGLE_API_KEY')
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],  # CRITICAL
        image_config=types.ImageConfig(aspect_ratio="1:1")
    )
)

for part in response.parts:
    if part.inline_data:
        image = part.as_image()  # Returns PIL Image
        image.save("output.png")
```

**Available Aspect Ratios:**
- `1:1` - Square (1024×1024) - Social media, TPT products
- `16:9` - Landscape - Course covers, presentations
- `9:16` - Portrait - Mobile, stories
- `4:3`, `3:4`, `3:2`, `2:3`, `16:10`, `10:16`, `21:9`

## 💰 Revenue Model

**Current TPT Pricing:**
- Coloring sheets: $3-8 each
- Word searches: $2-5 each
- Bundles: $10-25

**Cost Breakdown:**
- Image generation: **$0.00** (FREE with Gemini)
- Design time: 20-30 minutes
- Profit margin: **100%** (zero production cost)

**Scaling to 100 Products:**
- 100 products × $5 average × 10 sales/month = **$5,000/month**
- Total production cost: **$0.00**
- Time investment: 30-50 hours (one-time)

## 🔧 Scripts Explained

### `generate_gemini_official.py`
- **Status**: ✅ VERIFIED WORKING
- Uses official `google-genai` library
- Generates 8 ecosystem images
- Outputs to `ecosystem-artwork/`
- **Cost**: FREE

### `create_pptx_coloring_sheet.py`
- Creates PowerPoint coloring sheet
- Adds 8 images in 4×2 grid
- Professional formatting
- US Letter size (8.5" × 11")

### `create_word_search.py`
- Generates 15×15 word search puzzle
- 10 ecosystem vocabulary words
- Beautiful forest green theme
- Checkboxes for tracking

### `upload_to_onedrive.py` / `upload_word_search.py`
- Upload to Google Drive
- Make shareable (anyone with link)
- Returns view + download links

### `check_current_slides_state.py`
- Validation script
- Checks image sizes, positions
- Verifies page dimensions
- Identifies layout issues

### `rebuild_slides_correctly.py`
- Fixes broken slide layouts
- Deletes duplicate images
- Repositions elements
- Ensures TPT quality standards

## 🧪 Validation System

Created by **production-validator agent** for quality assurance.

**Run validation:**
```bash
cd validation
python analyze_slides_layout.py
```

**Checks:**
- Page size (8.5" × 11" US Letter)
- Image sizes (not too small/large)
- Image positions (within margins)
- Text readability
- Print-readiness

**See:** `validation/tpt_quality_standards.md` for 56 quality standards

## 🎓 Bob Ross Image 3D Makers Agent

Updated agent instructions: `.claude/agents/bob-ross-image-3d-makers.md`

**Key Updates:**
- Switched from OpenAI ($0.04/image) to Gemini (FREE)
- Updated profit margins from 99% to **100%**
- Added verified working code examples
- TPT-specific prompt templates

**Example prompts:**
```
For coloring pages:
"Create a simple black and white line art coloring page of [subject].
Clean black outlines only, white background, no shading or gray tones.
Suitable for [grade level] coloring. Large, clear shapes easy to color
within the lines. Professional educational worksheet quality."

For course covers:
"Professional educational course cover design for [topic]. Modern,
clean layout with vibrant colors. Include elements: [specific elements].
Title text: [exact title]. Professional, inspiring, educational."
```

## 📝 Lessons Learned

### What Worked
✅ **PowerPoint over Google Slides** - Better API control, proper image sizing
✅ **Gemini for image generation** - FREE, high quality, perfect for TPT
✅ **python-pptx library** - Reliable, full control over layout
✅ **Validation scripts** - Caught 20+ layout issues automatically

### What Didn't Work
❌ **Google Slides API** - Poor image sizing support, creates 0.03" images
❌ **OpenRouter for images** - Doesn't support image generation
❌ **google-generativeai library** - Wrong library, created empty files

### Best Practices
1. **Always use PowerPoint for TPT products** (not Google Slides)
2. **Generate images with Gemini directly** (not through proxies)
3. **Validate before uploading** (use validation scripts)
4. **Test print one copy** before publishing to TPT
5. **Keep prompts in version control** for reproducibility

## 🚀 Scaling to 100+ Products

**Automation Strategy:**

1. **Batch Image Generation**
   - Create prompt templates for each product type
   - Generate 10-20 images at once (still FREE)
   - Store in organized directories

2. **Template System**
   - Create PowerPoint templates for each product type
   - Reuse layouts with new content/images
   - Consistent branding across products

3. **Validation Pipeline**
   - Run automated validation on all products
   - Fix issues programmatically
   - Ensure consistent quality

4. **Upload & Tracking**
   - Automated upload to Drive/OneDrive
   - Track all products in JSON file
   - Monitor revenue per product

**See:** `PROCESS_DOCUMENTATION.md` for complete workflow

## 🔑 API Keys Required

**Google Gemini API** (for image generation):
- Get key: https://aistudio.google.com/apikey
- Add to `.env` as `GOOGLE_API_KEY`
- Cost: FREE with generous limits

**Google Workspace API** (for Drive upload):
- OAuth tokens already configured
- Location: `C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/token-personal.json`
- No action needed

## 📚 Additional Documentation

- **`TPT_AUTOMATION_INSTRUCTIONS.md`** - Step-by-step guide for creating products
- **`PROCESS_DOCUMENTATION.md`** - Complete automation workflow
- **`validation/tpt_quality_standards.md`** - 56 quality standards for TPT
- **`validation/REUSABLE_VALIDATION_WORKFLOW.md`** - Scaling validation to 100+ products

## 🎯 Future Enhancements

- [ ] Create templates for other product types (worksheets, flashcards, posters)
- [ ] Add Word document generation for printable worksheets
- [ ] Automated TPT upload API integration
- [ ] Revenue tracking dashboard
- [ ] Batch processing for 10+ products at once
- [ ] A/B testing for different designs
- [ ] Customer review monitoring

## 💡 Quick Tips

**For best results:**
1. Generate multiple image variations (it's FREE!)
2. Test print before uploading to TPT
3. Use consistent branding across products
4. Follow TPT marketplace guidelines
5. Price competitively ($3-8 for single products)

**Common issues:**
- Images too small? Use PowerPoint, not Google Slides
- Layout broken? Run validation scripts
- Images not loading? Check file paths
- Poor quality? Refine Gemini prompts

## 📞 Support

**Documentation:**
- Main README: This file
- Instructions: `TPT_AUTOMATION_INSTRUCTIONS.md`
- Validation: `validation/REUSABLE_VALIDATION_WORKFLOW.md`

**Scripts:**
- All scripts have inline documentation
- Run with `python script_name.py` for usage

## 🏆 Success Metrics

**Current Achievement:**
- ✅ 2 TPT products created in 1 hour
- ✅ $0.00 production cost
- ✅ Professional quality validated
- ✅ Ready for TPT marketplace

**Next Milestone:**
- 🎯 10 products in TPT store
- 🎯 $500/month passive income
- 🎯 Automated batch processing

---

**Built with:** Google Gemini 2.5 Flash Image (FREE) | Python | PowerPoint | Love for Education ❤️

**Created:** November 2025
**Status:** Production-ready automation system
**Cost:** $0.00 per product
