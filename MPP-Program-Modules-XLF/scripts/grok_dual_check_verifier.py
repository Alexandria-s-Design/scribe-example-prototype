"""
Grok-Only Dual-Check Verification System
=========================================
Uses Grok for BOTH checks simultaneously:
1. MPP accuracy (with direct RAG context)
2. eLearning SOP compliance

Both queries run in parallel for maximum speed
"""
import os
import sys
import asyncio
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Add MPP backend to path for RAG access
sys.path.insert(0, str(Path(__file__).parent.parent / "MPP-SOP-Appendix-I-Chat-2" / "backend"))
from services.rag_service import RAGService

load_dotenv()

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class GrokDualCheckVerifier:
    """
    Uses Grok for BOTH MPP and SOP checks in parallel

    Flow:
    1. Query RAGService directly for relevant MPP context
    2. Grok Query 1: MPP accuracy with RAG context
    3. Grok Query 2: eLearning SOP compliance
    4. Both run simultaneously for speed
    """

    def __init__(self, chroma_db_path: str = None):
        # Initialize RAG Service
        if chroma_db_path:
            os.environ['CHROMA_DB_PATH'] = chroma_db_path

        # Change to MPP directory for ChromaDB access
        original_dir = os.getcwd()
        mpp_dir = Path(__file__).parent.parent / "MPP-SOP-Appendix-I-Chat-2"
        os.chdir(mpp_dir)

        self.rag_service = RAGService()
        doc_count = self.rag_service.get_document_count()
        print(f"✓ ChromaDB connected: {doc_count} document chunks loaded")

        # Return to original directory
        os.chdir(original_dir)

        # Initialize Grok
        grok_key = os.getenv("GROK_API_KEY")
        if not grok_key:
            raise ValueError("GROK_API_KEY not found in .env")

        self.grok_client = OpenAI(
            api_key=grok_key,
            base_url="https://api.x.ai/v1"
        )
        print("✓ Grok API initialized")

    async def grok_mpp_check(
        self,
        unit_id: str,
        text: str,
        context: str = ""
    ) -> Dict:
        """
        Grok MPP accuracy check WITH direct RAG context
        """
        # Query RAG for relevant context
        rag_results = self.rag_service.query(text, n_results=3)
        rag_context = "\n\n".join([
            f"[{r['source']}] {r['text'][:300]}..."
            for r in rag_results
        ])

        prompt = f"""MPP ACCURACY CHECK for Program Manager training:

TEXT TO VERIFY: "{text}"

RELEVANT MPP DOCUMENTATION:
{rag_context}

Your role: MPP content expert. Check ONLY:
1. Factual accuracy per MPP SOP/DFARS Appendix I (use doc citations above)
2. Program Manager perspective (not Mentor/Protégé POV)
3. Terminology: Mentor/Protégé capitalized, federal lowercase (except Federal Government)

Respond with:
- ✓ ACCURATE or ✗ NEEDS CORRECTION
- Confidence: X%
- Issues: [specific problems or "None"]
- Corrections: [with citations if needed]

Be direct and concise."""

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.grok_client.chat.completions.create(
                    model="grok-4-0709",
                    messages=[
                        {"role": "system", "content": "You are an MPP content expert with access to official documentation."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.2
                )
            )

            return {
                'success': True,
                'role': 'MPP_ACCURACY',
                'checker': 'Grok + RAG',
                'response': response.choices[0].message.content,
                'unit_id': unit_id,
                'rag_sources': [r['source'] for r in rag_results]
            }
        except Exception as e:
            return {'success': False, 'role': 'MPP_ACCURACY', 'error': str(e)}

    async def grok_sop_check(
        self,
        unit_id: str,
        text: str,
        original: str = ""
    ) -> Dict:
        """
        Grok eLearning SOP compliance check - COMPREHENSIVE
        """
        prompt = f"""eLEARNING SOP COMPLIANCE CHECK:

TEXT: {text}

Your role: eLearning content quality expert. Check ALL of these:

1. **Bullets & Lists**:
   - Complete sentences with capital + period?
   - Parallel structure (all bullets same grammatical form)?
   - Numbered lists for procedures?

2. **Grammar**:
   - Proper sentence construction?
   - No fragments (unless short labels/titles)?
   - Consistent verb tense?

3. **Punctuation & Capitalization**:
   - Correct punctuation throughout?
   - Proper capitalization (Mentor, Protégé, Federal Government)?
   - No missing periods or commas?

4. **Clarity & Tone**:
   - Clear for Program Manager audience?
   - Concise and professional?
   - Appropriate level of detail?
   - Active voice preferred?

5. **PM Learner Perspective**:
   - If text addresses PM learners directly ("you", "your"), is it appropriate?
   - Learning objectives properly formatted?
   - Instructional language clear?

6. **Parallel Structure**:
   - Do list items follow same pattern?
   - Are verb forms consistent?
   - Are sentence structures balanced?

Respond with:
- ✓ SOP COMPLIANT or ✗ SOP ISSUES
- Issues: [specific problems or "None"]
- Fixes: [exact corrections needed with line references]
- Confidence: X%

Be direct, thorough, and actionable."""

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.grok_client.chat.completions.create(
                    model="grok-4-0709",
                    messages=[
                        {"role": "system", "content": "You are an eLearning SOP compliance expert."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.2
                )
            )

            return {
                'success': True,
                'role': 'ELEARNING_SOP',
                'checker': 'Grok',
                'response': response.choices[0].message.content,
                'unit_id': unit_id
            }
        except Exception as e:
            return {'success': False, 'role': 'ELEARNING_SOP', 'error': str(e)}

    async def verify_unit(
        self,
        unit_id: str,
        transformed_text: str,
        original_text: str = "",
        context: str = ""
    ) -> Dict:
        """
        Verify ONE unit with Grok doing BOTH checks in parallel
        """
        # Both Grok checks run in parallel on DIFFERENT aspects
        mpp_task = self.grok_mpp_check(unit_id, transformed_text, context)
        sop_task = self.grok_sop_check(unit_id, transformed_text, original_text)

        mpp_result, sop_result = await asyncio.gather(mpp_task, sop_task)

        # Determine overall pass
        mpp_passed = mpp_result.get('success', False) and '✓' in mpp_result.get('response', '')
        sop_passed = sop_result.get('success', False) and '✓' in sop_result.get('response', '')

        return {
            'unit_id': unit_id,
            'mpp_accuracy': mpp_result,
            'elearning_sop': sop_result,
            'mpp_passed': mpp_passed,
            'sop_passed': sop_passed,
            'overall_pass': mpp_passed and sop_passed
        }

    async def verify_batch(self, units: List[Dict]) -> List[Dict]:
        """
        Process multiple units with parallel Grok checks
        """
        print(f"\n{'='*80}")
        print("GROK DUAL-CHECK VERIFICATION (MPP + SOP)")
        print(f"{'='*80}")
        print(f"Units: {len(units)}")
        print(f"Grok Check 1 → MPP accuracy (with direct RAG context)")
        print(f"Grok Check 2 → eLearning SOP compliance")
        print(f"Mode: Both checks run in parallel for each unit")
        print(f"{'='*80}\n")

        results = []
        # Process in batches of 5 units (10 Grok queries per batch)
        batch_size = 5
        for i in range(0, len(units), batch_size):
            batch = units[i:i+batch_size]
            tasks = []

            for j, unit in enumerate(batch):
                # Build context from surrounding units
                global_idx = i + j
                context_before = units[global_idx-1].get('transformed', '') if global_idx > 0 else ""
                context_after = units[global_idx+1].get('transformed', '') if global_idx < len(units)-1 else ""
                context = f"Previous: {context_before[:100]}... Next: {context_after[:100]}..."

                task = self.verify_unit(
                    unit_id=unit.get('unit_id', f'unit_{global_idx}'),
                    transformed_text=unit.get('transformed', ''),
                    original_text=unit.get('original', ''),
                    context=context
                )
                tasks.append(task)

            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            # Print progress
            for result in batch_results:
                print(f"  [{result['unit_id'][:30]}...]")
                print(f"    Grok MPP: {'✓ PASS' if result['mpp_passed'] else '✗ ISSUES'}")
                print(f"    Grok SOP: {'✓ PASS' if result['sop_passed'] else '✗ ISSUES'}")

        print(f"\n{'='*80}")
        print("VERIFICATION COMPLETE")
        print(f"{'='*80}")

        return results


def verify_units_grok_dual(
    units: List[Dict],
    chroma_db_path: str = None
) -> List[Dict]:
    """
    Synchronous wrapper for Grok dual-check verification

    Args:
        units: List with 'unit_id', 'transformed', 'original'
        chroma_db_path: Optional path to ChromaDB

    Returns:
        List of results with separate MPP and SOP assessments
    """
    verifier = GrokDualCheckVerifier(chroma_db_path)

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    return asyncio.run(verifier.verify_batch(units))


# CLI Test
if __name__ == "__main__":
    test_units = [{
        'unit_id': 'test_grok_dual',
        'original': 'mentors provide assistance',
        'transformed': 'Program Managers (PMs) oversee Mentors who provide developmental assistance to Protégés per MPP SOP requirements.'
    }]

    print("Testing Grok Dual-Check Verification...")
    results = verify_units_grok_dual(test_units)

    print("\nRESULTS:")
    for r in results:
        print(f"\nUnit: {r['unit_id']}")
        print(f"MPP Check (Grok+RAG): {'PASS' if r['mpp_passed'] else 'ISSUES'}")
        print(f"  RAG Sources: {r['mpp_accuracy'].get('rag_sources', [])}")
        print(f"SOP Check (Grok): {'PASS' if r['sop_passed'] else 'ISSUES'}")
        print(f"Overall: {'APPROVED' if r['overall_pass'] else 'NEEDS WORK'}")
