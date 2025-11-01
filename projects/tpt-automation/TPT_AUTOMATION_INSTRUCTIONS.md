# TPT Automation - Complete Step-by-Step Instructions

**Purpose**: Create Teachers Pay Teachers products automatically with AI-generated images and professional layouts.

**Time to Complete**: 20-30 minutes per product
**Cost**: $0.00 (FREE image generation with Gemini)
**Difficulty**: Beginner-friendly

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [One-Time Setup](#one-time-setup)
3. [Creating Your First Product](#creating-your-first-product)
4. [Product Type: Coloring Sheet](#product-type-coloring-sheet)
5. [Product Type: Word Search](#product-type-word-search)
6. [Validation & Quality Check](#validation--quality-check)
7. [Upload & Share](#upload--share)
8. [Scaling to 100+ Products](#scaling-to-100-products)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

**Required:**
- Python 3.11+ installed
- Google API key (FREE from https://aistudio.google.com/apikey)
- Google Workspace access (for Drive uploads)
- PowerPoint or access to view PPTX files

**Optional:**
- Microsoft Office 365 (for native PowerPoint editing)
- Teachers Pay Teachers seller account
- Graphics editing software (for advanced customization)

---

## One-Time Setup

### Step 1: Install Python Libraries

```bash
pip install google-genai python-pptx google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**What each does:**
- `google-genai` - Google Gemini image generation (FREE)
- `python-pptx` - Create PowerPoint files
- `google-*` - Upload to Google Drive

### Step 2: Get Google Gemini API Key

1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIzaSy...`)
4. Add to `.env` file:

```bash
# Open or create .env file in project root
# Add this line:
GOOGLE_API_KEY=your_api_key_here
```

### Step 3: Verify Google Drive Access

Your Google Workspace OAuth tokens should already be configured at:
```
C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/token-personal.json
```

**Test it:**
```bash
python upload_to_onedrive.py
```

If you get an authentication error, re-authenticate via Google Workspace MCP.

### Step 4: Create Project Directory

```bash
cd C:/Users/MarieLexisDad/projects
mkdir -p tpt-automation/ecosystem-artwork
cd tpt-automation
```

---

## Creating Your First Product

**Workflow:**
1. Generate AI images (FREE with Gemini)
2. Create PowerPoint layout
3. Validate quality
4. Upload & share

**Total time**: 20-30 minutes

---

## Product Type: Coloring Sheet

### Step 1: Generate Images with Gemini

```bash
cd C:/Users/MarieLexisDad/projects/tpt-automation
python generate_gemini_official.py
```

**What happens:**
- Generates 8 black & white line art images
- Perfect for 3rd grade coloring
- Saves to `ecosystem-artwork/` directory
- **Cost**: $0.00 (FREE!)

**Output files:**
```
ecosystem-artwork/
├── oak_tree.png
├── deer.png
├── rabbit.png
├── mushrooms.png
├── sun.png
├── rocks.png
├── pond.png
└── grass_flowers.png
```

**Customization:**

Edit `generate_gemini_official.py` to change:
- **Topics**: Change ecosystem to any theme (space, ocean, animals)
- **Grade level**: Adjust complexity in prompts
- **Number of images**: Add/remove from `ELEMENTS` list
- **Aspect ratio**: Change `aspect_ratio="1:1"` to `"16:9"`, `"9:16"`, etc.

**Example custom prompt:**
```python
prompt = f"""Create a simple black and white line art coloring page of a
{your_subject}. Clean black outlines only, white background, no shading.
Suitable for {grade_level} coloring. Large, clear shapes easy to color.
Professional educational worksheet quality."""
```

### Step 2: Create PowerPoint Layout

```bash
python create_pptx_coloring_sheet.py
```

**What it creates:**
- US Letter size PowerPoint (8.5" × 11")
- 4×2 grid of images (1.5" × 1.5" each)
- Title: "Ecosystem Coloring Sheet - 3rd Grade"
- Student info section (Name, Date)
- Instructions
- Vocabulary footer

**Output:**
```
Ecosystem_Coloring_Sheet.pptx (4.1 MB)
```

**Layout details:**
- Images: 0.5" left margin, 2.0" top for first row, 4.5" top for second row
- Spacing: 0.25" between images horizontally
- Labels: Below each image with name

**Customization:**

Edit `create_pptx_coloring_sheet.py`:

```python
# Change image size
IMAGE_SIZE = 1.5  # Change to 2.0 for larger images

# Change positions
IMAGES = [
    {"file": "oak_tree.png", "left": 0.5, "top": 2.0, "name": "Oak Tree"},
    # Adjust 'left' and 'top' values for custom positioning
]

# Change title
title_frame.text = "Your Custom Title Here"
```

### Step 3: Upload to Drive

```bash
python upload_to_onedrive.py
```

**Output:**
- View link: https://docs.google.com/...
- Download link: https://drive.google.com/uc?...

**Opens in:**
- Google Slides (view/edit in browser)
- PowerPoint (download and edit)
- Export to PDF (for printing)

---

## Product Type: Word Search

### Step 1: Create Word Search

```bash
python create_word_search.py
```

**What it creates:**
- 15×15 letter grid
- 10 vocabulary words hidden (across, down, diagonal)
- Forest green professional theme
- Checkboxes for tracking found words
- Student info section

**Default words:**
```
ANIMAL, CHAIN, CONSUMER, DECOMPOSER, ECOSYSTEM,
ENERGY, FOOD, HABITAT, PLANT, PRODUCER
```

**Output:**
```
Ecosystem_Word_Search.pptx (34.5 KB)
```

**Customization:**

Edit `create_word_search.py`:

```python
# Change words
WORDS = [
    "YOUR_WORD_1",
    "YOUR_WORD_2",
    # ... up to 10 words
]

# Change grid size
GRID_SIZE = 15  # Make larger/smaller (12-20 recommended)

# Change colors
header_bg.fill.fore_color.rgb = RGBColor(34, 139, 34)  # Forest green
# Change to: RGBColor(R, G, B) for any color
```

**Theme ideas:**
- Ocean (blue theme): WHALE, OCEAN, CORAL, FISH, etc.
- Space (dark blue/black): PLANET, STAR, MOON, GALAXY, etc.
- Animals (brown theme): LION, TIGER, BEAR, etc.

### Step 2: Upload to Drive

```bash
python upload_word_search.py
```

**Output:**
- View link: https://docs.google.com/...
- Download link: https://drive.google.com/uc?...

---

## Validation & Quality Check

### Why Validate?

Ensure your product meets TPT marketplace standards:
- Correct page size (8.5" × 11")
- Images properly sized (not too small)
- Text readable (not overlapping)
- Print-ready quality

### Run Validation

```bash
cd validation
python analyze_slides_layout.py
```

**Checks performed:**
1. **Page size**: Must be US Letter (8.5" × 11")
2. **Image sizes**: Between 1" and 3" (optimal for coloring)
3. **Image positions**: Within printable margins (0.5" minimum)
4. **Text boxes**: No overlapping, proper sizing
5. **Print readiness**: All elements within safe area

**Example output:**
```
Page Size: 8.50" × 11.00" ✓
Images: 8 found
  - All images 1.50" × 1.50" ✓
  - All within margins ✓
Text Boxes: 4 found
  - All readable ✓

VALIDATION PASSED: Ready for TPT
```

### Fix Issues

If validation fails:

```bash
python fix_slides_images_only.py
```

**What it fixes:**
- Removes duplicate images
- Resizes images to optimal dimensions
- Repositions images within margins
- Clears overlapping elements

**Re-validate:**
```bash
python analyze_slides_layout.py
```

### Quality Standards

See `validation/tpt_quality_standards.md` for complete list of 56 quality standards.

**Key standards:**
- Page size exactly 8.5" × 11"
- Minimum 0.5" margins all sides
- Text font size 11pt minimum
- Images between 1" and 3"
- No overlapping elements
- Consistent spacing
- Professional appearance

---

## Upload & Share

### Option 1: Google Drive (Recommended)

```bash
python upload_to_onedrive.py  # For coloring sheet
python upload_word_search.py   # For word search
```

**Benefits:**
- Anyone with link can view
- Open in Google Slides (browser)
- Open in PowerPoint (desktop)
- Direct download available

**Output:**
```
View in Browser:
https://docs.google.com/presentation/d/.../edit

Direct Download:
https://drive.google.com/uc?id=...&export=download
```

### Option 2: Export to PDF

**In PowerPoint:**
1. Open PPTX file
2. File → Save As → PDF
3. Upload PDF to TPT marketplace

**In Google Slides:**
1. Open view link in browser
2. File → Download → PDF Document
3. Upload to TPT

### Option 3: Native PowerPoint

**Local file:**
```
C:/Users/MarieLexisDad/projects/tpt-automation/Ecosystem_Coloring_Sheet.pptx
```

**Open directly in:**
- Microsoft PowerPoint
- LibreOffice Impress
- Google Slides (upload first)

---

## Scaling to 100+ Products

### Strategy

**Batch Processing:**
1. Create 10 product ideas
2. Generate 80 images (8 per product) in one session (FREE!)
3. Create 10 PowerPoint files
4. Validate all 10 in batch
5. Upload all 10 at once

**Time estimate:**
- 10 products: 3-4 hours
- 50 products: 15-20 hours
- 100 products: 30-40 hours

### Templates

Create reusable templates for each product type:

**Coloring Sheet Template:**
```python
def create_coloring_sheet(theme, grade, images, title):
    """
    theme: "Ecosystem", "Ocean", "Space", etc.
    grade: "2nd", "3rd", "4th"
    images: List of 8 image file paths
    title: Custom title
    """
    # Use create_pptx_coloring_sheet.py as base
    # Pass parameters instead of hardcoded values
```

**Word Search Template:**
```python
def create_word_search(theme, grade, words, color_theme):
    """
    theme: Topic name
    grade: Target grade
    words: List of 10 vocabulary words
    color_theme: RGB color tuple
    """
    # Use create_word_search.py as base
    # Parameterize everything
```

### Batch Script Example

```python
# batch_create_tpt_products.py

products = [
    {
        "type": "coloring",
        "theme": "Ocean",
        "grade": "3rd",
        "images": [...],
        "title": "Ocean Life Coloring Sheet"
    },
    {
        "type": "word_search",
        "theme": "Space",
        "grade": "4th",
        "words": ["PLANET", "STAR", ...],
        "color": (0, 0, 128)  # Navy blue
    },
    # ... 98 more products
]

for product in products:
    if product["type"] == "coloring":
        create_coloring_sheet(**product)
    elif product["type"] == "word_search":
        create_word_search(**product)

    validate_product(product)
    upload_product(product)
```

### Revenue Tracking

Track all products in JSON:

```python
# products_tracker.json
{
    "products": [
        {
            "id": 1,
            "name": "Ecosystem Coloring Sheet",
            "type": "coloring",
            "price": 5.00,
            "sales": 0,
            "revenue": 0,
            "created": "2025-11-01",
            "file_url": "https://drive.google.com/...",
            "tpt_url": ""
        }
    ]
}
```

Update after each sale:
```python
def update_sales(product_id, sales_count, revenue):
    # Update JSON tracker
    # Calculate total revenue
    # Generate monthly reports
```

---

## Troubleshooting

### Issue: Images Generated as 0 KB Files

**Cause**: Using wrong library (`google-generativeai` instead of `google-genai`)

**Fix:**
```bash
pip uninstall google-generativeai
pip install google-genai
```

**Verify:**
```python
from google import genai  # Correct
# NOT: import google.generativeai as genai  # Wrong
```

### Issue: Google Slides Images Show as 0.03"

**Cause**: Google Slides API doesn't properly support image sizing on creation

**Fix**: Use PowerPoint instead of Google Slides
```bash
python create_pptx_coloring_sheet.py  # Creates PPTX
# NOT: Google Slides API scripts
```

### Issue: API Key Not Found

**Cause**: `.env` file not loaded or API key not set

**Fix:**
```bash
# Check .env file exists
cat .env

# Should show:
GOOGLE_API_KEY=AIzaSy...

# If missing, create it:
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Issue: Permission Denied on Upload

**Cause**: Google OAuth tokens expired

**Fix:**
1. Re-authenticate with Google Workspace MCP
2. Or manually refresh token at: `C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/token-personal.json`

### Issue: Word Search Words Don't Fit

**Cause**: Words too long for 15×15 grid

**Fix:**
```python
# In create_word_search.py

# Option 1: Increase grid size
GRID_SIZE = 20  # Was 15

# Option 2: Use shorter words
WORDS = ["SHORT", "WORDS", "ONLY"]  # 5-8 letters max
```

### Issue: Layout Looks Different in PowerPoint vs Google Slides

**Cause**: Different rendering engines

**Fix**: Always preview in target format before uploading to TPT
- Export to PDF for final version
- PDF renders identically everywhere

### Issue: Validation Script Says "Elements Out of Bounds"

**Cause**: Images or text extending past 8.5" × 11" page

**Fix:**
```bash
python fix_slides_images_only.py
```

Or adjust manually in PowerPoint:
1. Select all elements
2. Drag within margins (0.5" from edges)
3. Re-save

---

## Advanced Customization

### Change Image Generation Model

Currently using: `gemini-2.5-flash-image` (FREE)

**Available models:**
- `gemini-2.5-flash-image` - Fast, free, high quality
- `gemini-2.0-flash-image` - Older, still free
- `gemini-pro-vision` - More expensive, not recommended

**To change:**
```python
# In generate_gemini_official.py
response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # Change here
    ...
)
```

### Add More Product Types

**Flashcards:**
```python
# create_flashcards.py
def create_flashcard_set(words, definitions, images):
    prs = Presentation()
    # Create one slide per flashcard
    # Front: word + image
    # Back: definition
```

**Posters:**
```python
# create_poster.py
def create_educational_poster(title, facts, images):
    prs = Presentation()
    prs.slide_width = Inches(11)   # Wider
    prs.slide_height = Inches(17)  # Taller
    # Add title, facts grid, images
```

**Worksheets (Word):**
```python
from docx import Document

def create_worksheet(title, questions, images):
    doc = Document()
    # Add title
    # Add questions with fill-in-blanks
    # Add images
    doc.save("worksheet.docx")
```

### Custom Themes

Create theme files:

```python
# themes.py
THEMES = {
    "ocean": {
        "color": RGBColor(0, 119, 190),  # Ocean blue
        "accent": RGBColor(0, 166, 81),  # Sea green
        "font": "Arial Rounded MT Bold"
    },
    "space": {
        "color": RGBColor(25, 25, 112),  # Midnight blue
        "accent": RGBColor(255, 215, 0),  # Gold
        "font": "Century Gothic"
    },
    "forest": {
        "color": RGBColor(34, 139, 34),   # Forest green
        "accent": RGBColor(139, 69, 19),  # Brown
        "font": "Calibri"
    }
}

# Apply in scripts:
theme = THEMES["ocean"]
header_bg.fill.fore_color.rgb = theme["color"]
```

---

## Checklist: Before Uploading to TPT

- [ ] All images high quality (not pixelated)
- [ ] Page size exactly 8.5" × 11"
- [ ] Minimum 0.5" margins all sides
- [ ] Text readable (font size 11pt+)
- [ ] No spelling errors
- [ ] Professional appearance
- [ ] Tested print on actual printer
- [ ] Exported to PDF format
- [ ] Grade level appropriate
- [ ] Follows TPT content guidelines
- [ ] Unique (not duplicate of existing products)

---

## Quick Reference Commands

```bash
# Generate images (FREE)
python generate_gemini_official.py

# Create coloring sheet
python create_pptx_coloring_sheet.py

# Create word search
python create_word_search.py

# Validate quality
cd validation && python analyze_slides_layout.py

# Fix issues
python fix_slides_images_only.py

# Upload to Drive
python upload_to_onedrive.py  # Coloring sheet
python upload_word_search.py   # Word search
```

---

## Resources

**Documentation:**
- Main README: `README.md`
- Process docs: `PROCESS_DOCUMENTATION.md`
- Quality standards: `validation/tpt_quality_standards.md`
- Validation workflow: `validation/REUSABLE_VALIDATION_WORKFLOW.md`

**Google Gemini:**
- API docs: https://ai.google.dev/gemini-api/docs
- Get API key: https://aistudio.google.com/apikey
- Model info: https://ai.google.dev/gemini-api/docs/models

**Python Libraries:**
- python-pptx: https://python-pptx.readthedocs.io/
- google-genai: https://github.com/googleapis/python-genai

**TPT Marketplace:**
- Seller guide: https://www.teacherspayteachers.com/Sell-Content
- Quality standards: https://www.teacherspayteachers.com/Uploads
- Best practices: https://www.teacherspayteachers.com/Sellers

---

## Next Steps

1. **Create your first product** following this guide
2. **Test print** to verify quality
3. **Upload to TPT** and set pricing
4. **Create 10 products** to build catalog
5. **Scale to 100 products** using batch processing
6. **Track revenue** and optimize best-sellers

---

**Ready to create passive income with TPT automation!** 🚀

Start with: `python generate_gemini_official.py`
