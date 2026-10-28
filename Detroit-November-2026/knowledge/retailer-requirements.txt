# Retailer onboarding requirements

SYNTHETIC CONFERENCE DATA

Fictional retailer onboarding policy, not a real retailer's requirements.

Source ID: retailer-requirements-v1
Schema version: 1.0
Retailer: Great Lakes Home & Hardware
Retailer ID: great-lakes-home

## Listing format

- Title: brand + product name; maximum 80 characters.
- Bullets: exactly 5; maximum 160 characters each.
- Currency: USD. Manufacturer MSRP is not retailer selling price.

## Category mapping

- Cordless drill kits -> Tools > Power Tools > Drills > Drill Kits
- Cordless impact driver kits -> Tools > Power Tools > Impact Drivers > Driver Kits

## Required for submission

- gtin (MISSING_GTIN): Manufacturer must supply a verified product GTIN; never invent one.
- imageAssets (MISSING_IMAGES): Manufacturer must supply approved product images and usage rights.
- warrantyTerms (MISSING_WARRANTY): Manufacturer must supply approved warranty terms.

## Copy policy

Facts only: yes.
Do not infer certifications, safety, compatibility beyond the stated platform, runtime, battery chemistry or warranty. MSRP is not the retailer's selling price. Preserve unknowns as null or empty arrays and record blockers.

Do not add these unsubstantiated claims:

- certified
- safest
- best-in-class
- OSHA approved
- UL listed

## Human review and disposition

Every package remains needs_review. A human category reviewer and manufacturer fact owner must review before any external submission. This foundation has no approval or submission integration.
