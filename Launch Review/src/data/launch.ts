// Values transcribed verbatim from the two supplied source files.
// Unknown values are kept as null / empty arrays; nothing is inferred.

export type SourceId = "manufacturer-products-v1" | "retailer-requirements-v1";

export interface SourceDoc {
  id: SourceId;
  fileName: string;
  title: string;
  schemaVersion: string;
  owner: string;
  classification: string;
  disclaimer: string;
}

export const SOURCES: SourceDoc[] = [
  {
    id: "manufacturer-products-v1",
    fileName: "manufacturer-products.txt",
    title: "Manufacturer product specifications",
    schemaVersion: "1.0",
    owner: "Lakeshore Motion Tools · Grand Rapids, Michigan",
    classification: "SYNTHETIC CONFERENCE DATA",
    disclaimer:
      "Fictional conference data. Not a real offer, performance test, certification or safety instruction.",
  },
  {
    id: "retailer-requirements-v1",
    fileName: "retailer-requirements.txt",
    title: "Retailer onboarding requirements",
    schemaVersion: "1.0",
    owner: "Great Lakes Home & Hardware (great-lakes-home)",
    classification: "SYNTHETIC CONFERENCE DATA",
    disclaimer: "Fictional retailer onboarding policy, not a real retailer's requirements.",
  },
];

export interface Spec {
  label: string;
  value: string;
  unit: string | null;
}

export interface Product {
  productId: string;
  name: string;
  sku: string;
  brand: string;
  manufacturer: string;
  manufacturerCategory: string;
  retailerCategory: string;
  targetLaunchDate: string;
  audience: string;
  msrp: { currency: string; amount: string; note: string };
  specs: Spec[];
  inTheBox: string[];
  approvedBullets: string[];
  gtin: string | null;
  imageAssets: string[];
  warrantyTerms: string | null;
  missingNotes: { gtin: string; imageAssets: string; warrantyTerms: string };
  status: "needs_review";
  approvedBy: null;
}

export const PRODUCTS: Product[] = [
  {
    productId: "drill-kit",
    name: "Huron 18V Cordless Drill Kit",
    sku: "LM-D1820-K2",
    brand: "Lakeshore Motion",
    manufacturer: "Lakeshore Motion Tools",
    manufacturerCategory: "Cordless drill kits",
    retailerCategory: "Tools > Power Tools > Drills > Drill Kits",
    targetLaunchDate: "2027-03-15",
    audience: "DIY customers assembling furniture and completing household projects",
    msrp: { currency: "USD", amount: "129.00", note: "not retailer selling price" },
    specs: [
      { label: "Nominal voltage", value: "18", unit: "V" },
      { label: "Battery capacity per battery", value: "2", unit: "Ah" },
      { label: "Battery count", value: "2", unit: null },
      { label: "Maximum speed", value: "1700", unit: "rpm" },
      { label: "Maximum torque", value: "50", unit: "Nm" },
      { label: "Tool holder", value: "13 mm keyless chuck", unit: null },
      { label: "Mass with battery", value: "1.6", unit: "kg" },
    ],
    inTheBox: ["Drill", "Two 2.0 Ah batteries", "Charger", "Carry bag"],
    approvedBullets: [
      "18V nominal battery platform.",
      "Includes two 2.0 Ah batteries and a charger.",
      "Maximum speed: 1,700 rpm.",
      "13 mm keyless chuck.",
      "Includes a carry bag.",
    ],
    gtin: null,
    imageAssets: [],
    warrantyTerms: null,
    missingNotes: {
      gtin: "unknown; manufacturer must supply a verified identifier",
      imageAssets: "none supplied",
      warrantyTerms: "unknown; approved terms required",
    },
    status: "needs_review",
    approvedBy: null,
  },
  {
    productId: "impact-driver-kit",
    name: "Huron 18V Cordless Impact Driver Kit",
    sku: "LM-I1820-K2",
    brand: "Lakeshore Motion",
    manufacturer: "Lakeshore Motion Tools",
    manufacturerCategory: "Cordless impact driver kits",
    retailerCategory: "Tools > Power Tools > Impact Drivers > Driver Kits",
    targetLaunchDate: "2027-03-15",
    audience: "DIY customers planning screw-fastening projects",
    msrp: { currency: "USD", amount: "139.00", note: "not retailer selling price" },
    specs: [
      { label: "Nominal voltage", value: "18", unit: "V" },
      { label: "Battery capacity per battery", value: "2", unit: "Ah" },
      { label: "Battery count", value: "2", unit: null },
      { label: "Maximum speed", value: "2800", unit: "rpm" },
      { label: "Maximum torque", value: "190", unit: "Nm" },
      { label: "Tool holder", value: "6.35 mm hex collet", unit: null },
      { label: "Mass with battery", value: "1.4", unit: "kg" },
    ],
    inTheBox: ["Impact driver", "Two 2.0 Ah batteries", "Charger", "Carry bag"],
    approvedBullets: [
      "18V nominal battery platform.",
      "Includes two 2.0 Ah batteries and a charger.",
      "Maximum speed: 2,800 rpm.",
      "6.35 mm hex collet.",
      "Includes a carry bag.",
    ],
    gtin: null,
    imageAssets: [],
    warrantyTerms: null,
    missingNotes: {
      gtin: "unknown; manufacturer must supply a verified identifier",
      imageAssets: "none supplied",
      warrantyTerms: "unknown; approved terms required",
    },
    status: "needs_review",
    approvedBy: null,
  },
];

export interface Requirement {
  field: "gtin" | "imageAssets" | "warrantyTerms";
  label: string;
  code: string;
  policy: string;
}

export const REQUIREMENTS: Requirement[] = [
  {
    field: "gtin",
    label: "GTIN",
    code: "MISSING_GTIN",
    policy: "Manufacturer must supply a verified product GTIN; never invent one.",
  },
  {
    field: "imageAssets",
    label: "Approved images",
    code: "MISSING_IMAGES",
    policy: "Manufacturer must supply approved product images and usage rights.",
  },
  {
    field: "warrantyTerms",
    label: "Warranty terms",
    code: "MISSING_WARRANTY",
    policy: "Manufacturer must supply approved warranty terms.",
  },
];

export const LISTING_RULES = [
  "Title: brand + product name; maximum 80 characters.",
  "Bullets: exactly 5; maximum 160 characters each.",
  "Currency: USD. Manufacturer MSRP is not retailer selling price.",
];

export const BANNED_CLAIMS = ["certified", "safest", "best-in-class", "OSHA approved", "UL listed"];

export const REVIEW_POLICY =
  "Every package remains needs_review. A human category reviewer and manufacturer fact owner must review before any external submission. This foundation has no approval or submission integration.";

// Draft launch package documents. None of these files were supplied, so each
// carries no location and renders as unavailable.
export interface PackageDoc {
  key: string;
  label: string;
  location: string | null;
}

export const PACKAGE_DOCS: PackageDoc[] = [
  { key: "brief", label: "Launch brief", location: null },
  { key: "csv", label: "Listing CSV", location: null },
  { key: "email", label: "Email draft (unsent)", location: null },
  { key: "record", label: "Package and review record", location: null },
];
