# TrueStore — Project Context Document
Last updated: June 26, 2026
Purpose: Paste this at the start of any new Claude chat inside the TrueStore project to restore full context instantly.

## What Is TrueStore?
TrueStore is a consumer price transparency platform for the self-storage industry. The core problem: facilities advertise low promotional web rates, then raise prices significantly after month 1-3. Fine print buried in leases allows rate increases "at any time at our discretion." Aggregators (SpareFoot, StorageCafe, RentCafe) are paid by facilities and show promotional rates only. Nobody is on the consumer's side.

TrueStore uses an AI-powered scraping agent to dig past landing pages into lease agreements, FAQ pages, checkout flows, and third-party pricing portals to extract real ongoing rates, hidden fees, and rate-increase language.

Name: TrueStore
Owner: John Arnold, Lincoln NE
GitHub org: JAI-100
Analogy: GasBuddy for storage but AI-powered, not crowdsourced.

## Business Model
- Free for consumers
- TrueStore Verified badge — facilities pay small fee for verified transparent status
- Data licensing to REITs and investors
- Carfax model — facilities pay for credibility, consumers get truth free
- Moat: adversarial/consumer-side, not aggregator-paid

## Tech Stack
Location on Mac Mini M4: ~/projects/truestore/

Files:
- src/facilities.py — Lincoln NE facility seed list
- src/extractor.py — Async fetch engine (aiohttp + Playwright fallback)
- src/analyzer.py — Claude API extraction (claude-sonnet-4-6)
- src/run.py — Main runner
- .env — ANTHROPIC_API_KEY stored here

Dependencies: requests, playwright (Chromium), anthropic, python-dotenv, aiohttp, beautifulsoup4, lxml, psycopg2-binary

To run: cd ~/projects/truestore && source venv/bin/activate && cd src && python run.py

## Critical Discovery: Third-Party Portal Blind Spot
Many small facilities use SaaS platforms for pricing — the marketing site has no prices but a separate domain does.

Known platforms to check:
- storageunitsoftware.com (most common in Lincoln)
- storedge.com
- sitelink.com
- storagesites.com
- storable.com

Discovery method: Search site:storageunitsoftware.com [city] [state] storage
This found: Northwest Storage, Lincoln Self Storage, Top Storage Lincoln West

## Lincoln NE Market
- Real facility count: 75-100+ (StorageCafe says 36 but misses small independents)
- Average rate: $164/mo
- Key finding: Only 2 of 20 scoreable facilities disclosed real ongoing rates upfront

## Scored Facilities

GREEN 8/10:
- U-Haul North Lincoln, 1930 Fletcher Ave, (402) 488-1930, 5x5 $69.95/mo, 1-year price lock
- U-Haul 48th & Vine, 740 N 48th St, (402) 467-7700, 5x10 $104.95/mo, 1-year price lock

GREEN 7/10 (recovered from failed list):
- Superior Street Storage, 4660 N 35th St, (402) 326-3381
  Portal: superiorstreetstorage.storageunitsoftware.com
  Drive-up 5x10 $89/mo, Climate 10x5 $95/mo, veteran-owned, no hidden fee language

AMBER 6/10:
- Five Star Storage Cornhusker, 5340 Cornhusker Hwy, 5x5 $27/mo (may be promo)
- Five Star Storage Pioneers, 1801 Pioneers Blvd, 5x10 $52/mo (may be promo)

RED 3/10:
- StorageMart Cornhusker, 6101 Cornhusker Hwy, (800) 264-9485
  Bait-and-switch confirmed: "rates subject to change at any time at our discretion"
  2.5% credit card surcharge buried in footer fine print
- Dillon Self Storage, 3839 Hohensee Dr
- Kiss Self Storage, Lincoln NE

RED 2/10:
- Dino's Storage
- FreeUp Storage N Cotner Blvd, 700 N Cotner Blvd
- FreeUp Storage N 1st St, 1909 N 1st St
- Eagles Nest Self Storage

RED 1/10:
- Big Red Self Storage (8 locations) — zero pricing online
- Lincoln Self Storage — portal: lincolnselfstore.storageunitsoftware.com (needs pricing pull)
- Mammoth Mega Storage, 2223 Fletcher Ave
- Sasquatch Self Storage
- Aardvark Self Storage
- Capitol City Mini Storage, 2905 N 38th St
- By-Pass Storage, 3130 S 6th St
- C and G Stor-Away, 2505 N 33rd St

PORTALS FOUND — NEEDS PRICING PULL:
- Northwest Storage, 6707 NW 48th St, (402) 470-3223
  Portal: nweststorage.storageunitsoftware.com
- Lincoln Self Storage, 801 S Coddington Ave
  Portal: lincolnselfstore.storageunitsoftware.com

NEW FACILITY DISCOVERED (not in original list):
- Top Storage Lincoln West: topstoragelincolnwest.storageunitsoftware.com

STILL NO WEBSITE:
- Budget Storage Pioneers
- Always Safe Storage
- Cornhusker Self Storage
- A Economy Self Storage
- A Kimco Self Storage
- Tower View Mini Storage
- Stor-It 4 Less
- Spare Room Storage (timed out)

## Consumer Messaging Nuance
Not all facilities without online pricing are hiding something.
- Bait-and-switch = prices shown but real rate buried or raised after promo (StorageMart)
- No online pricing = small independent that prefers direct conversation, may be MORE flexible
- Consumer tip: When calling, ask "What is my rate in month 4?" and "Do you price-match?"

## Output Files on Mac Mini
~/projects/truestore/output/
- truestore_lincoln_20260626_122137.json — PRIMARY RESULTS (20 scored facilities)
- summary_lincoln_20260626_122137.txt

Word report: TrueStore_Lincoln_Report.docx (needs rebuild with new data)

## Next Steps
1. John to provide remaining URLs for failed facilities
2. Pull pricing from Northwest Storage portal /pages/rent
3. Pull pricing from Lincoln Self Storage portal /pages/rent
4. Pull pricing from Top Storage Lincoln West portal
5. Update facilities.py with all portal URLs
6. Add third-party portal detection to extractor.py
7. Rebuild final Word report with all data and updated consumer messaging
8. Register truestore.io or truestore.app domain
9. File USPTO ITU trademark (~$350)
10. Expand agent to Omaha, then Kansas City

## Key Decisions
- Name: TrueStore
- Model: Consumer-free, facility-paid for verified status
- Tech: Python + Claude API + Playwright + PostgreSQL on Mac Mini M4
- Expansion: Lincoln to Omaha to Kansas City to national
