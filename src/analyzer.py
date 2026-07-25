import anthropic
import json
import os
from dotenv import load_dotenv

# Load .env from project root (one level up from src/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

client = anthropic.Anthropic(api_key=api_key)

# ── MANUAL OVERRIDES ──────────────────────────────────────────────────────────
# Applied site-by-site where we have verified data from manual research.
# These override the agent's score when the simple fetch missed JS-rendered pricing.
# Source: Manual research session June 26, 2026.

MANUAL_OVERRIDES = {
    "U-Haul North Lincoln": {
        "smallest_unit_size": "5x5",
        "smallest_unit_price": 69.95,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "OPTIONAL",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "YES - 1-Year Price Lock: Monthly price remains the same for your first 12 months",
        "rate_increase_policy": "Rate guaranteed for 12 months",
        "transparency_score": 8,
        "red_flags": [],
        "notes": "1930 Fletcher Ave. Full pricing disclosed. 1-year price lock standard. 5x5 $69.95, 5x10 $89.95, 10x10 $149.95, 10x15 $189.95, 10x20 $219.95. Climate and drive-up available.",
        "override": True
    },
    "U-Haul 48th and Vine": {
        "smallest_unit_size": "5x10",
        "smallest_unit_price": 104.95,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "OPTIONAL",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "YES - 1-Year Price Lock: Monthly price remains the same for your first 12 months",
        "rate_increase_policy": "Rate guaranteed for 12 months",
        "transparency_score": 8,
        "red_flags": [],
        "notes": "740 N 48th St. Full pricing disclosed. 1-year price lock standard. 5x10 $104.95, 10x10 $169.95, 10x15 $199.95, 10x20 $239.95. Climate and drive-up available.",
        "override": True
    },
    "Superior Street Storage": {
        "smallest_unit_size": "5x10",
        "smallest_unit_price": 89.0,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "Promo prices noted as permanent on some units",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 7,
        "red_flags": [],
        "notes": "Veteran-owned. Full pricing at superiorstreetstorage.storageunitsoftware.com. Non-climate: 5x10 $89, 10x20 $159, 10x25 $179. Climate: 10x5 $95, 10x9 $128, 8x10 $123, 11.6x10 $157, 10x14 $159 (summer special). Parking $89/mo.",
        "override": True
    },
    "Lincoln Self Storage": {
        "smallest_unit_size": "5x10",
        "smallest_unit_price": 85.0,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "OPTIONAL",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 8,
        "red_flags": [],
        "notes": "Full pricing at lincolnselfstore.storageunitsoftware.com. Drive-up: 5x10 $85, 10x10 $130, 10x15 $150, 10x20 $165, 10x20 w/outlet $180, 10x25 $190, 10x30 $235, 10x30 pull-thru $235, 10x40 pull-thru $330. Climate: 10x10 $140, 10x15 $160. Month-to-month stated.",
        "override": True
    },
    "Northwest Storage": {
        "smallest_unit_size": "5x8x8",
        "smallest_unit_price": 47.50,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "NO",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "Prices may reflect discount from longer term agreement",
        "transparency_score": 6,
        "red_flags": ["Prices may reflect a discount from a longer term agreement"],
        "notes": "Full pricing at nweststorage.storageunitsoftware.com. Wide range of unusual sizes. Indoor from $47.50 (5x8x8) to $236.55 (11x40x8). Outdoor parking from $35.15 (10x20) to $105.45 (14x70). Footnote about longer-term discounts is mild concern.",
        "override": True
    },
    "Dino's Storage Northern Lights": {
        "smallest_unit_size": "2x10",
        "smallest_unit_price": 36.0,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "YES",
        "drive_up_access": "NO",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "RECOMMENDED",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "Availability subject to change without notice",
        "transparency_score": 6,
        "red_flags": ["Availability subject to change without notice", "Three-tier pricing (Base/Best Value/Premium) can be confusing"],
        "notes": "1945 N 84th St. Climate-controlled only. Three-tier pricing: Base/Best Value/Premium. 2x10 $36-$59, 5x5 $46-$68, 5x10 $62-$86, 10x10 $109-$139, 10x15 $131-$165, 10x20 $173-$198, 10x25 $209-$234, 10x30 $248-$277.",
        "override": True
    },
    "Dino's Storage 601 J St": {
        "smallest_unit_size": "5x4",
        "smallest_unit_price": 41.0,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "YES",
        "drive_up_access": "NO",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "RECOMMENDED",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "Availability subject to change without notice",
        "transparency_score": 6,
        "red_flags": ["Availability subject to change without notice", "Three-tier pricing can be confusing"],
        "notes": "601 J St, downtown Lincoln. Climate-controlled + outdoor parking. Very wide unit variety. 5x4 $41-$62, 5x5 $47-$71, 5x10 $79-$102, 10x10 $135-$157, 10x15 $178-$202, 10x24 $271-$291, 10x26 $283-$309. Outdoor parking: 10x20 $32, 10x30 $48, 10x40 $57, 10x60 $74.",
        "override": True
    },
    "StorageMart Cornhusker": {
        "smallest_unit_size": "5x5",
        "smallest_unit_price": 55.0,
        "ongoing_rate_disclosed": "NO",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "YES",
        "insurance_cost": "$20/mo if not providing own",
        "credit_card_fee": "2.5%",
        "price_lock": "NO",
        "rate_increase_policy": "Prices subject to change at any time at our discretion. Rental rates may be increased with advance notice.",
        "transparency_score": 3,
        "red_flags": [
            "Rates subject to change at any time at our discretion",
            "2.5% credit card surcharge",
            "Mandatory insurance $20/mo if not providing own",
            "Introductory rates only - ongoing rate not disclosed",
            "Discounts on move-in month only"
        ],
        "notes": "6101 Cornhusker Hwy. Confirmed bait-and-switch language in footer fine print. Range $60-$316/mo per aggregators but these may be promotional. Two Lincoln locations with identical policies.",
        "override": True
    },
    "StorageMart West O Street": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": 35.0,
        "ongoing_rate_disclosed": "NO",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "YES",
        "insurance_cost": "$20/mo if not providing own",
        "credit_card_fee": "2.5%",
        "price_lock": "NO",
        "rate_increase_policy": "Prices subject to change at any time at our discretion. Rental rates may be increased with advance notice.",
        "transparency_score": 3,
        "red_flags": [
            "Rates subject to change at any time at our discretion",
            "2.5% credit card surcharge",
            "Mandatory insurance $20/mo if not providing own",
            "Introductory rates only - ongoing rate not disclosed",
            "Discounts on move-in month only"
        ],
        "notes": "2701 W O St. Identical policy to Cornhusker location. Parking spaces 10x18 to 10x38. Starting from $35/mo. Same bait-and-switch fine print as Cornhusker.",
        "override": True
    },
    "Kiss Self Storage": {
        "smallest_unit_size": "Small",
        "smallest_unit_price": 60.0,
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 5,
        "red_flags": ["Pricing tiers shown on homepage but full grid requires JS to load"],
        "notes": "6500 NW 42nd St. Homepage shows: Small from $60, Medium from $90, Large from $144. Full unit grid JS-rendered via Storedge. Drive-through units available. Pricing visible to consumers in browser.",
        "override": True
    },
    "Dillon Self Storage": {
        "smallest_unit_size": "Small",
        "smallest_unit_price": 85.0,
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 11:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 5,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "3839 Hohensee Dr (+ W O St location). Homepage shows: Small from $85, Medium from $125, Large from $165. New 3-story climate-controlled building open. Full grid JS-rendered via Storedge. Pricing visible to consumers in browser.",
        "override": True
    },
    "Mini Storage Space": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": 95.0,
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "NOT FOUND",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 5,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "2075 N 86th St. BBB A+ accredited. Pricing from aggregators: $95-$234/mo. Climate-controlled and drive-up available. Indoor vehicle storage (door 7ft 8in x 9ft wide). No boats or RVs. Month-to-month. Full grid JS-rendered.",
        "override": True
    },
    "Big Red Self Storage Van Dorn": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NO",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load - pricing exists but not extractable without browser"],
        "notes": "609 Van Dorn St. Heated drive-up units, covered vehicle storage. Locally owned. Pricing JS-rendered on bigredselfstorage.com - visible to consumers in browser. RentCafe shows $54-$425 range across Big Red locations.",
        "override": True
    },
    "Big Red Self Storage 46th St": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "540 N 46th St. Pricing JS-rendered. RentCafe shows $59-$289 range. Locally owned.",
        "override": True
    },
    "Big Red Self Storage Karl Ridge": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "8270 Karl Ridge Rd. Pricing JS-rendered. Locally owned.",
        "override": True
    },
    "Big Red Self Storage Custer": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "7001 Custer St. Pricing JS-rendered. Locally owned.",
        "override": True
    },
    "Big Red Self Storage Helen Witt": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "7080 Helen Witt Dr. Pricing JS-rendered. Locally owned.",
        "override": True
    },
    "Big Red Self Storage N 27th": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "4010 N 27th St. Pricing JS-rendered. RentCafe shows $54-$425 range. Locally owned.",
        "override": True
    },
    "Big Red Self Storage Yankee Woods": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "8233 Yankee Woods Dr. Pricing JS-rendered. Locally owned.",
        "override": True
    },
    "Big Red Self Storage S 14th": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "4911 S 14th St. Pricing JS-rendered. Locally owned.",
        "override": True
    },
    "Sasquatch Self Storage Coddington": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "201 S Coddington Ave. RV/car/boat parking available. Military discounts. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Sasquatch Self Storage NW 9th": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "2300 NW 9th St. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Sasquatch Self Storage Cheney": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "9520 First St, Cheney NE (near Lincoln). Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Aardvark Self Storage": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "5800 Arbor Rd. Vehicle/RV parking available. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "FreeUp Storage N 1st St": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": 62.0,
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "No refunds for early move-out",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load", "No refunds for early move-out per customer reviews"],
        "notes": "1909 N 1st St. Starting from $62/mo per aggregators. Interior and drive-up units. Climate-controlled available. No-refund policy on early move-out flagged in reviews. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "FreeUp Storage N Cotner Blvd": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": 65.0,
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "700 N Cotner Blvd. Starting from $65/mo per aggregators. Drive-up outdoor units. Truck parking also available. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Eagle's Nest Self Storage": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "YES",
        "access_hours": "7:00 AM - 11:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "3700 Adams Ste 1. Current special: free disc lock for new move-ins. Units have power. Free dollies/handcarts. Near UNL. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Five Star Storage Cornhusker": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "7:00 AM - 9:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load", "Up to 50% off first 3 months promo - ongoing rate unclear"],
        "notes": "5350 Cornhusker Hwy. Indoor parking available. Up to 50% off first 3 months promotion active. Pricing JS-rendered on custom CMS. Multi-state chain.",
        "override": True
    },
    "Five Star Storage Pioneers": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "YES",
        "access_hours": "7:00 AM - 9:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load", "Up to 50% off first 3 months promo - ongoing rate unclear"],
        "notes": "1801 Pioneers Blvd. Pricing JS-rendered on custom CMS. Multi-state chain.",
        "override": True
    },
    "Infinity Self Storage": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "YES",
        "drive_up_access": "NOT FOUND",
        "access_hours": "NOT FOUND",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load"],
        "notes": "1542 S 1st St. Summer student special May-Aug. RV/boat/vehicle storage. Climate-controlled available. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Always Safe Storage Eagle NE": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "PARTIAL",
        "climate_control_available": "NO",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 4,
        "red_flags": ["Full pricing grid requires JS to load", "Located in Eagle NE - ~20 miles from Lincoln"],
        "notes": "23910 Karl Dr, Eagle NE 68347 (~20 miles from Lincoln). Spring special: 50% off first month (3-month minimum). Indoor/outdoor RV/boat/vehicle storage. Drive-thru bays. 12-foot perimeter fencing, every door alarmed. 24/7 access. Pricing JS-rendered via Storedge.",
        "override": True
    },
    "Capitol City Storage": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "NO",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "NOT FOUND",
        "access_hours": "NOT FOUND",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 2,
        "red_flags": ["No online pricing - call for rates"],
        "notes": "3 locations: 2905 N 38th St, 3250 Huntington Ave, 6341 Burlington Ave. Family-owned since 1987. Explicitly says 'call for monthly rates'. No online pricing at all. Small independent operator - may be more flexible on price than chains. Ask: rate in month 4, price match policy.",
        "override": True
    },
    "Kimco Self Storage": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "NO",
        "climate_control_available": "NOT FOUND",
        "drive_up_access": "NOT FOUND",
        "access_hours": "6:00 AM - 10:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 2,
        "red_flags": ["No online pricing - call for rates"],
        "notes": "6000 S 56th St. U-Haul dealer on site. No pricing visible online. Call (402) 423-3003. Small independent - may be negotiable.",
        "override": True
    },
    "Stor-It 4 Less": {
        "smallest_unit_size": "8x10",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "NO",
        "climate_control_available": "NO",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 2,
        "red_flags": ["No online pricing - call for rates"],
        "notes": "4216 Progressive Ave. Family-owned. Units 8x10 to 12x30. 10% discount for advance payment and military. No online pricing. Call (402) 429-1713. Small independent - may be negotiable.",
        "override": True
    },
    "Spare Room Storage": {
        "smallest_unit_size": "NOT FOUND",
        "smallest_unit_price": "NOT FOUND",
        "ongoing_rate_disclosed": "NO",
        "climate_control_available": "NO",
        "drive_up_access": "YES",
        "access_hours": "7:00 AM - 8:00 PM daily",
        "admin_fee": "NOT FOUND",
        "insurance_required": "NOT FOUND",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 1,
        "red_flags": ["No online pricing available even via aggregators"],
        "notes": "4101 N 27th St. RentCafe says unit details not available - contact property directly. Phone (402) 437-8321. Drive-up, gated, security cameras. Unstaffed location.",
        "override": True
    },
    "Mammoth Mega Storage": {
        "smallest_unit_size": "15x25",
        "smallest_unit_price": 300.0,
        "ongoing_rate_disclosed": "YES",
        "climate_control_available": "NO",
        "drive_up_access": "YES",
        "access_hours": "24 hours",
        "admin_fee": "NOT FOUND",
        "insurance_required": "RECOMMENDED",
        "credit_card_fee": "NOT FOUND",
        "price_lock": "NOT FOUND",
        "rate_increase_policy": "NOT FOUND",
        "transparency_score": 7,
        "red_flags": [],
        "notes": "2223 Fletcher Ave. Large/mega units only - not standard self-storage. 15x25 $300, 15x30 $350, 17x30 $400, 17x50 $650, 21x40 $650, 21x50 $800. Month-to-month. RV/boat/trailer/vehicle/inventory focus. Not climate-controlled. Pro-rated first month.",
        "override": True
    },
}

EXTRACTION_PROMPT = """You are a data extraction specialist for TrueStore, a consumer price transparency platform for self-storage units.

Analyze the following text scraped from a storage facility website and extract the requested information.

IMPORTANT CONTEXT: Some storage websites use JavaScript to load their pricing dynamically. If the page content 
shows a loading placeholder (e.g. "Please wait while we are loading", "Loading Available Units") but also shows 
facility information like address, phone, amenities and hours, this means pricing EXISTS and IS visible to 
consumers in a real browser — it just could not be captured by our static scraper. In this case:
- Set ongoing_rate_disclosed to "PARTIAL" (not NO)
- Set transparency_score no lower than 4 (not 1 or 2)
- Note in red_flags that "Full pricing grid requires JS to load"
- Do NOT penalize the facility as if pricing is hidden — it is accessible to consumers

Only score 1-2 if there is genuinely NO pricing anywhere (no JS placeholder, no aggregator data, 
explicitly says "call for rates").

Be honest - if information is NOT present on the page, say "NOT FOUND" for that field.
Do NOT guess or make up prices. Only report what is explicitly stated.

Extract these fields:
1. promo_rate - Any advertised promotional/move-in rate (e.g. "first month free", "$1 first month")
2. ongoing_rate_disclosed - YES, PARTIAL, or NO - is the real ongoing monthly rate clearly stated?
3. smallest_unit_price - Price per month for smallest available unit (exact number if found)
4. smallest_unit_size - Size of smallest unit (e.g. "5x5", "5x10")
5. rate_increase_policy - Any language about rate increases after promo period
6. admin_fee - Any admin or setup fee mentioned
7. security_deposit - Any deposit required
8. insurance_required - YES, NO, OPTIONAL, RECOMMENDED, or NOT FOUND
9. insurance_cost - Monthly cost of required/optional insurance if stated
10. climate_control_available - YES or NO
11. drive_up_access - YES or NO
12. access_hours - Hours tenants can access their unit
13. credit_card_fee - Any surcharge for paying by credit card
14. price_lock - Any price lock or rate guarantee mentioned
15. transparency_score - Rate 1-10 how transparent this facility is about REAL ongoing pricing:
    10 = Full price grid with ongoing rates, no hidden fees, no rate-change language
    8-9 = Full pricing visible, minor caveats only
    6-7 = Pricing visible but some ambiguity (promo vs ongoing unclear, tier pricing)
    4-5 = Pricing exists and visible to consumers in browser but JS-rendered (not extractable by scraper)
    2-3 = Explicitly calls for rates, no pricing online at all
    1 = No pricing, no website, or completely opaque
16. red_flags - List any deceptive pricing language found (e.g. "subject to change", "introductory rate", "may vary")
17. notes - Anything else a consumer should know

Return ONLY a valid JSON object with these exact field names. No explanation, no markdown, just JSON.

FACILITY TEXT:
{content}"""

def analyze_facility(facility_result):
    name = facility_result['facility']['name']
    url = facility_result['facility']['url']

    # ── Apply manual override first — even if fetch failed ───────────────────
    if name in MANUAL_OVERRIDES:
        override_data = MANUAL_OVERRIDES[name].copy()
        override_data['facility_name'] = name
        override_data['facility_url'] = url
        override_data['fetch_method'] = facility_result.get('method', 'failed')
        override_data['data_source'] = 'manual_research'
        print(f"  Using manual override for: {name}")
        return override_data

    if not facility_result['success']:
        return {
            "facility_name": name,
            "facility_url": url,
            "error": "Could not fetch website",
            "transparency_score": None
        }

    content = facility_result['content']

    print(f"  Analyzing: {name}")

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": EXTRACTION_PROMPT.format(content=content)
                }
            ]
        )

        raw = message.content[0].text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        data = json.loads(raw)
        data['facility_name'] = name
        data['facility_url'] = url
        data['fetch_method'] = facility_result['method']
        data['data_source'] = 'agent'
        return data

    except json.JSONDecodeError as e:
        print(f"  JSON parse error for {name}: {e}")
        return {
            "facility_name": name,
            "facility_url": url,
            "error": f"JSON parse error: {e}",
            "transparency_score": None
        }
    except Exception as e:
        print(f"  Analysis error for {name}: {e}")
        return {
            "facility_name": name,
            "facility_url": url,
            "error": str(e),
            "transparency_score": None
        }

def analyze_all(facility_results):
    analyzed = []
    total = len(facility_results)
    for i, result in enumerate(facility_results, 1):
        print(f"[{i}/{total}] Analyzing {result['facility']['name']}...")
        data = analyze_facility(result)
        analyzed.append(data)
    return analyzed
