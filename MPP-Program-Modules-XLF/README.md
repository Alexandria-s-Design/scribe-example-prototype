# MPP Program Modules XLF Transformation System

**Automated XLF transformation system with HTML formatting preservation for DoD Mentor-Protégé Program eLearning modules.**

## 🎯 What This System Does

Transforms XLF (XLIFF 1.2) translation files from Articulate Rise 360 courses while:
- ✅ Preserving ALL HTML formatting (bullets, lists, text styling)
- ✅ Applying MPP-specific terminology corrections
- ✅ Converting perspective to Program Manager viewpoint
- ✅ Dual AI verification (Grok MPP accuracy + eLearning SOP compliance)
- ✅ Generating comprehensive quality reports

## 📊 Production Results (Module 1)

- **568 total units** processed
- **185 substantive units** transformed
- **89 units modified** (terminology corrections)
- **24/185 units** (13%) fully approved by dual AI checks
- **100% formatting preservation** (all bullets, lists, styling intact)

## 🚀 Quick Start

### Prerequisites

1. **Export from Articulate Rise 360:**
   - Go to course → Translate → Export for Translation
   - ✅ **CHECK** "Include HTML formatting" (CRITICAL!)
   - Download the XLF file

2. **Python dependencies:**
   ```bash
   pip install openai chromadb sentence-transformers lxml
   ```

3. **Environment variables** (`.env` file):
   ```
   GROK_API_KEY=your_grok_api_key_here
   ```

### Running the Full Production

```bash
python scripts/xlf_formatted_production_orchestrator.py
```

**Edit these paths in the script first:**
- `input_xlf`: Your HTML-formatted XLF file from Rise
- `output_xlf`: Where to save transformed XLF
- `report_path`: Where to save the quality report

**Processing time:** ~20-30 minutes for 185 substantive units

## 📁 Project Structure

```
MPP-Program-Modules-XLF/
├── scripts/
│   ├── xlf_formatted_production_orchestrator.py  # Main production script
│   ├── xlf_writer_formatted.py                   # Formatting-preserving writer
│   ├── xlf_parser.py                             # XLF parser
│   ├── transformation_engine.py                  # MPP transformation rules
│   ├── grok_dual_check_verifier.py              # AI verification (MPP + SOP)
│   ├── test_formatted_xlf_writer.py             # Test script
│   └── examine_formatted_xlf.py                 # Diagnostic tool
├── docs/
│   └── XLF-FORMATTING-PRESERVATION-GUIDE.md     # Complete guide
└── README.md
```

## 🔧 How It Works

### Phase 1: Parse XLF with Formatting
- Reads XLF file exported WITH HTML formatting
- Identifies substantive vs non-substantive units
- Preserves all `<g>` tag structure (bullets, lists, styling)

### Phase 2: Apply Transformations
- Capitalizes "Mentor" and "Protégé"
- Expands first-mention acronyms (e.g., "DoD Mentor-Protégé Program (MPP)")
- Converts perspective to Program Manager viewpoint
- Fixes "federal" vs "Federal Government" usage

### Phase 3: Grok Dual-Check Verification
- **Check 1:** MPP accuracy (with RAG context from source documents)
- **Check 2:** eLearning SOP compliance (clarity, learner-friendliness)
- Processes in batches of 10 units
- Generates pass/fail for each check

### Phase 4: Write XLF with Formatting Preservation
- Clones entire `<g>` tag tree from source to target
- Applies transformed text to leaf nodes
- Preserves all `id`, `ctype`, and `style` attributes

### Phase 5: Generate Comprehensive Report
- Summary statistics
- Formatting preservation verification
- Units needing review (with AI feedback)
- Detailed results for all units

## 📋 Import Back to Rise

1. Open your course in Articulate Rise 360
2. Click **Translate** → **Import Translation**
3. Select the transformed XLF file (e.g., `Module-1-MPP-TRANSFORMED-FORMATTED-FINAL.xlf`)
4. Rise will apply all transformations with formatting intact

## ✅ Verification Checklist

Before importing to Rise:
- [ ] Input XLF was exported WITH "Include HTML formatting"
- [ ] Output file name ends with `*-FORMATTED-FINAL.xlf`
- [ ] Report shows formatting preserved (UL/LI tag counts match)
- [ ] No errors in Phase 4 (Writing XLF)

After importing to Rise:
- [ ] Bullet lists appear correctly
- [ ] Numbered lists are intact
- [ ] Text styling (bold, colors, font sizes) preserved
- [ ] Transformations applied correctly

## 🛠️ Troubleshooting

### "Formatting lost after import to Rise"
**Solution:** Re-export from Rise WITH "Include HTML formatting" checkbox.

### "Output file size much smaller than input"
**Red flag:** Formatting may have been stripped. Check that:
1. Input has `<g>` tags with `ctype="x-html-*"` attributes
2. Output has similar number of `<g>` tags
3. Script used `xlf_writer_formatted.py`

### "Some units show warnings in report"
**Normal:** Grok verification flags units that may need human review. Not all warnings mean errors - they're suggestions for quality assurance.

## 📖 Documentation

See `docs/XLF-FORMATTING-PRESERVATION-GUIDE.md` for:
- Complete workflow documentation
- Troubleshooting guide
- Lessons learned
- How to use for future modules

## 🎓 Key Learnings

1. **Always export with HTML formatting** in Articulate Rise 360
2. **Element tree cloning** preserves `<g>` tag structure
3. **Dual AI verification** catches both accuracy and clarity issues
4. **This workflow is reusable** for all 6 MPP course modules

## 📞 Support

For issues or questions, refer to the comprehensive guide in `docs/XLF-FORMATTING-PRESERVATION-GUIDE.md`.

---

**Last Updated:** November 3, 2025
**Module 1 Status:** ✅ Completed and verified in production
**Next Steps:** Apply to Modules 2-6 using same workflow
