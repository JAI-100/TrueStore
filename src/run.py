import asyncio
import json
import os
from datetime import datetime
from facilities import LINCOLN_FACILITIES
from extractor import fetch_all
from analyzer import analyze_all
from report_generator import generate_html_report

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

def save_results(results, label="lincoln"):
    """Save results to JSON and a simple readable summary."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Full JSON output
    json_path = os.path.join(OUTPUT_DIR, f"truestore_{label}_{timestamp}.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved: {json_path}")

    # Human-readable summary
    summary_path = os.path.join(OUTPUT_DIR, f"summary_{label}_{timestamp}.txt")
    with open(summary_path, 'w') as f:
        f.write(f"TrueStore Lincoln NE — Run: {timestamp}\n")
        f.write("=" * 60 + "\n\n")

        # Sort by transparency score
        scored = [r for r in results if r.get('transparency_score') and isinstance(r.get('transparency_score'), (int, float))]
        unscored = [r for r in results if r not in scored]
        scored.sort(key=lambda x: x['transparency_score'], reverse=True)

        f.write("RANKED BY TRANSPARENCY (highest = most honest pricing)\n")
        f.write("-" * 60 + "\n\n")

        for r in scored:
            f.write(f"[{r['transparency_score']}/10] {r['facility_name']}\n")
            f.write(f"  URL: {r['facility_url']}\n")
            f.write(f"  Promo Rate: {r.get('promo_rate', 'NOT FOUND')}\n")
            f.write(f"  Ongoing Rate Disclosed: {r.get('ongoing_rate_disclosed', 'NOT FOUND')}\n")
            f.write(f"  Smallest Unit: {r.get('smallest_unit_size', 'NOT FOUND')} @ {r.get('smallest_unit_price', 'NOT FOUND')}/mo\n")
            f.write(f"  Price Lock: {r.get('price_lock', 'NOT FOUND')}\n")
            f.write(f"  Admin Fee: {r.get('admin_fee', 'NOT FOUND')}\n")
            f.write(f"  Insurance Required: {r.get('insurance_required', 'NOT FOUND')} — Cost: {r.get('insurance_cost', 'NOT FOUND')}\n")
            f.write(f"  Credit Card Fee: {r.get('credit_card_fee', 'NOT FOUND')}\n")
            f.write(f"  Climate Control: {r.get('climate_control_available', 'NOT FOUND')}\n")
            f.write(f"  Access Hours: {r.get('access_hours', 'NOT FOUND')}\n")
            f.write(f"  Rate Increase Policy: {r.get('rate_increase_policy', 'NOT FOUND')}\n")
            if r.get('red_flags'):
                f.write(f"  RED FLAGS: {r.get('red_flags')}\n")
            if r.get('notes'):
                f.write(f"  Notes: {r.get('notes')}\n")
            f.write("\n")

        if unscored:
            f.write("\nFACILITIES WITH ERRORS OR NO DATA\n")
            f.write("-" * 60 + "\n")
            for r in unscored:
                f.write(f"  {r['facility_name']} — {r.get('error', 'No score')}\n")

    print(f"Summary saved: {summary_path}")
    return json_path, summary_path

def print_quick_summary(results):
    """Print a quick console summary while files save."""
    print("\n" + "=" * 60)
    print("TRUESTORE QUICK RESULTS — LINCOLN NE")
    print("=" * 60)

    scored = [r for r in results if r.get('transparency_score') and isinstance(r.get('transparency_score'), (int, float))]
    scored.sort(key=lambda x: x['transparency_score'], reverse=True)

    print(f"\nTransparency Rankings ({len(scored)} facilities scored):\n")
    for r in scored:
        score = r['transparency_score']
        name = r['facility_name']
        price = r.get('smallest_unit_price', '?')
        size = r.get('smallest_unit_size', '?')
        disclosed = r.get('ongoing_rate_disclosed', '?')
        emoji = "✅" if score >= 7 else "⚠️" if score >= 4 else "🔴"
        print(f"  {emoji} [{score}/10] {name}")
        print(f"       Smallest: {size} @ ${price}/mo | Rate Disclosed: {disclosed}")

    errors = [r for r in results if r.get('error')]
    if errors:
        print(f"\n  ⚫ {len(errors)} facilities could not be fetched")

async def main():
    print("=" * 60)
    print("TrueStore — Storage Price Transparency Agent")
    print(f"Target: Lincoln, NE ({len(LINCOLN_FACILITIES)} facilities)")
    print("=" * 60)

    # Step 1: Fetch all facility websites
    print(f"\nStep 1: Fetching {len(LINCOLN_FACILITIES)} facility websites...")
    print("(Simple fetch first, Playwright fallback for JS-heavy sites)\n")
    fetch_results = await fetch_all(LINCOLN_FACILITIES, max_concurrent=5)

    successful = sum(1 for r in fetch_results if r.get('success'))
    print(f"\nFetch complete: {successful}/{len(LINCOLN_FACILITIES)} successful\n")

    # Step 2: Analyze with Claude API
    print("Step 2: Analyzing content with Claude API...")
    print("(Extracting real rates, fees, red flags)\n")
    analyzed = analyze_all(fetch_results)

    # Step 3: Save and display
    print("\nStep 3: Saving results...")
    save_results(analyzed)
    print_quick_summary(analyzed)

    print("\nStep 4: Generating HTML report...")
    report_path = generate_html_report(analyzed)
    print(f"\nDone! Open your report: open {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
