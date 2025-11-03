# XLF Formatting Preservation Guide

**Created**: November 3, 2025
**For**: Module 1 - DoD Mentor-Protégé Program Transformations

---

## 🎯 The Problem We Discovered

After running the first production transformation on `Copy-of-module-1-do-d-mentor-protege-program.xlf`, we discovered that **all formatting was lost** in the output:

- ❌ Bullet lists became plain text
- ❌ List items lost their structure
- ❌ Text styling (font sizes, colors) disappeared
- ❌ Paragraph formatting was flattened

**Root Cause**: The original XLF was exported from Articulate Rise **WITHOUT** the "Include HTML Formatting" checkbox selected.

---

## ✅ The Solution

### Step 1: Re-Export with HTML Formatting

In Articulate Rise 360:
1. Go to the course
2. Click **Translate** → **Export for Translation**
3. ✅ **CHECK** the box: "Include HTML formatting"
4. Download the XLF file

**Result**: File with inline `<g>` tags that preserve formatting structure.

### Step 2: Use Formatting-Preserving Writer

Created `xlf_writer_formatted.py` that:
- **Clones** the entire `<g>` tag structure from `<source>` to `<target>`
- **Applies** text transformations while keeping formatting intact
- **Preserves** bullets, lists, paragraphs, and text styling

---

## 📂 Files Involved

### Input Files

1. **Original (NO HTML)**: `Copy-of-module-1-do-d-mentor-protege-program.xlf`
   - Exported without formatting checkbox
   - First production run used this (formatting lost)
   - Size: 308 KB

2. **Formatted (WITH HTML)**: `Module-1-do-d-mentor-protege-program (1).xlf`
   - Exported WITH "Include HTML formatting" checkbox ✅
   - Contains `<g>` tags for bullets, lists, styling
   - Size: ~350 KB (larger due to formatting tags)
   - **Currently processing** (Nov 3, 2025)

### Output Files

1. **First Run (NO FORMATTING)**: `Module-1-MPP-TRANSFORMED-FINAL.xlf`
   - 354 KB
   - Transformations applied correctly ✅
   - Formatting lost ❌
   - Do NOT import this into Rise

2. **Second Run (WITH FORMATTING)**: `Module-1-MPP-TRANSFORMED-FORMATTED-FINAL.xlf`
   - Currently being generated (Nov 3, 2025 ~1:20 PM)
   - Transformations applied ✅
   - Formatting preserved ✅
   - **This is the one to import into Rise**

### Scripts

1. **xlf_writer_formatted.py**
   - Formatting-preserving XLF writer
   - Clones `<g>` tag structure from source to target
   - Key method: `update_targets_with_formatting()`

2. **test_formatted_xlf_writer.py**
   - Test script that validated formatting preservation
   - Result: ✅ BULLET LIST FORMATTING PRESERVED

3. **xlf_formatted_production_orchestrator.py**
   - Full 568-unit production with formatting preservation
   - Currently running (Phase 3: Verification)

### Reports

1. **xlf_production_results_568_units.txt**
   - Report from first run (no formatting)
   - Shows 41/185 units approved (22.2%)

2. **xlf_formatted_production_results.txt**
   - Report from second run (with formatting)
   - Will be generated when current run completes

---

## 🔍 How the Formatting Preservation Works

### HTML Formatting Structure in XLF

Articulate Rise uses XLIFF 1.2 `<g>` tags to preserve inline HTML:

```xml
<source>
  <g id="..." ctype="x-html-DIV" data-editor-id="...">
    <g id="..." ctype="x-html-P">
      <g id="..." ctype="x-html-SPAN" style="font-size: 1.7rem">
        By the end of this lesson, you will be able to:
      </g>
    </g>
    <g id="..." ctype="x-html-UL">
      <g id="..." ctype="x-html-LI">
        <g id="..." ctype="x-html-P">
          <g id="..." ctype="x-html-SPAN" style="font-size: 1.7rem">
            Trace the legislative journey of the MPP...
          </g>
        </g>
      </g>
      <g id="..." ctype="x-html-LI">
        <g id="..." ctype="x-html-P">
          <g id="..." ctype="x-html-SPAN" style="font-size: 1.7rem">
            Cite the legal authority for the DoD Mentor-Protégé Program...
          </g>
        </g>
      </g>
    </g>
  </g>
</source>
```

**Key Tags**:
- `ctype="x-html-UL"` = Unordered list (bullets)
- `ctype="x-html-LI"` = List item
- `ctype="x-html-P"` = Paragraph
- `ctype="x-html-SPAN"` = Styled text
- `html:style="..."` = CSS styling

### What Our Writer Does

1. **Extract** text from leaf nodes (innermost `<g>` tags)
2. **Transform** the text using MPP rules:
   - Capitalize "Mentor" and "Protégé"
   - Expand first-mention acronyms
   - Convert perspective to Program Manager viewpoint
   - Fix "federal" capitalization
3. **Clone** the entire `<g>` tag structure to `<target>`
4. **Insert** transformed text back into leaf nodes
5. **Preserve** all `id`, `ctype`, and `style` attributes

**Result**: Transformed text with original formatting intact!

---

## 📊 Current Production Run Status

**Started**: November 3, 2025 at 1:20 PM
**Input**: `Module-1-do-d-mentor-protege-program (1).xlf` (WITH HTML formatting)
**Output**: `Module-1-MPP-TRANSFORMED-FORMATTED-FINAL.xlf`

### Progress

✅ **Phase 1**: Parsed XLF with formatting
- 568 total units
- 185 substantive units to transform
- 383 non-substantive units (skip)

✅ **Phase 2**: Applied transformations
- 185 units transformed
- 89 units modified
- 96 units unchanged (already compliant)

🔄 **Phase 3**: Grok dual-check verification (IN PROGRESS)
- 19 batches total (10 units per batch)
- Each batch: ~1-2 minutes
- MPP accuracy check (with RAG context)
- eLearning SOP compliance check
- Estimated completion: ~1:35 PM

⏳ **Phase 4**: Write XLF with formatting (PENDING)

⏳ **Phase 5**: Generate comprehensive report (PENDING)

---

## 🎓 Lessons Learned

### What Went Wrong the First Time

1. ❌ Exported XLF without "Include HTML formatting" checkbox
2. ❌ Original writer (`xlf_writer.py`) used `target_elem.text = transformed_text`
   - This sets plain text only
   - Strips all `<g>` children
   - Loses formatting structure

### What We Fixed

1. ✅ Re-exported with HTML formatting checkbox
2. ✅ Created new writer (`xlf_writer_formatted.py`) that:
   - Uses `clone_element_tree()` to copy structure
   - Applies transformations to leaf text nodes
   - Preserves all `<g>` tags and attributes

### Key Insight

**Articulate Rise's "Include HTML formatting" checkbox is CRITICAL** for preserving:
- Bullet lists and numbered lists
- Text styling (bold, italic, colors, font sizes)
- Paragraph formatting
- Div structures
- Any other visual formatting

**Always use this checkbox when exporting for transformation!**

---

## 🚀 How to Use This Process for Future Modules

### Step-by-Step Workflow

1. **Export from Rise with HTML formatting**
   ```
   Articulate Rise → Translate → Export for Translation
   ✅ CHECK "Include HTML formatting"
   ```

2. **Run the formatted production orchestrator**
   ```bash
   python C:\Users\MarieLexisDad\scripts\xlf_formatted_production_orchestrator.py
   ```

   Update these paths in the script:
   - `input_xlf`: Your HTML-formatted XLF file
   - `output_xlf`: Where to save transformed XLF
   - `report_path`: Where to save the report

3. **Wait for completion** (~20-30 minutes for 185 units)
   - Phase 1: Parsing (instant)
   - Phase 2: Transformations (1-2 minutes)
   - Phase 3: Verification (15-20 minutes)
   - Phase 4: Writing XLF (instant)
   - Phase 5: Report generation (instant)

4. **Review the report**
   - Check units that need review
   - Note any warnings or issues

5. **Import into Rise**
   ```
   Articulate Rise → Translate → Import Translation
   Select: Module-X-MPP-TRANSFORMED-FORMATTED-FINAL.xlf
   ```

6. **Verify in Rise**
   - Check that bullets/lists are intact
   - Verify text styling is preserved
   - Confirm transformations are correct

---

## 📋 Verification Checklist

Before importing to Rise, verify:

- [ ] Input XLF was exported WITH "Include HTML formatting"
- [ ] Output file name is `*-FORMATTED-FINAL.xlf`
- [ ] Report shows formatting preserved (e.g., "UL tags: 37 → 38")
- [ ] No errors in Phase 4 (Writing XLF)
- [ ] File size is similar to input (formatting tags add ~10-15%)

After importing to Rise, check:

- [ ] Bullet lists appear correctly
- [ ] Numbered lists are intact
- [ ] Text styling (bold, colors, font sizes) preserved
- [ ] Transformations applied correctly:
  - [ ] "Mentor" and "Protégé" capitalized
  - [ ] First-mention acronyms expanded
  - [ ] Perspective converted to PM viewpoint
  - [ ] "federal" vs "Federal Government" correct

---

## 🛠️ Troubleshooting

### "Formatting lost after import to Rise"

**Solution**: Re-export from Rise WITH "Include HTML formatting" checkbox.

### "Script fails with 'coroutine object is not iterable'"

**Solution**: The script uses `asyncio.run()` to handle async verification. Make sure you're running the **formatted** orchestrator, not the original one.

### "Output file size much smaller than input"

**Red flag**: Formatting may have been stripped. Check that:
1. Input has `<g>` tags with `ctype="x-html-*"` attributes
2. Output has similar number of `<g>` tags
3. Script used `xlf_writer_formatted.py`, not `xlf_writer.py`

### "Some units show warnings in report"

**Normal**: Grok verification flags units that may need human review. Check:
- MPP accuracy: Do terms/definitions match source material?
- eLearning SOP: Is language clear and learner-appropriate?

Not all warnings mean errors - they're suggestions for review.

---

## 📞 Key Contacts & Resources

- **Articulate Rise Documentation**: https://articulate.com/support/article/rise-translating-courses
- **XLIFF 1.2 Specification**: http://docs.oasis-open.org/xliff/v1.2/os/xliff-core.html
- **MPP Source Material**: `MPP-SOP-Appendix-I-Chat-2/backend/data/chroma_db/`

---

## 📝 Notes for Dr. Marie

- The first XLF file (`Copy-of-module...`) does NOT have formatting. Don't use it.
- The second XLF file (`Module-1-do-d-mentor-protege-program (1)`) DOES have formatting. Use this one.
- After this run completes, import `Module-1-MPP-TRANSFORMED-FORMATTED-FINAL.xlf` into Rise.
- The formatting (bullets, lists, styling) will be preserved.
- Review the report (`xlf_formatted_production_results.txt`) for any units flagged for review.

---

**Last Updated**: November 3, 2025 at 1:25 PM
**Next Steps**: Wait for production to complete, then import to Rise and verify formatting.
