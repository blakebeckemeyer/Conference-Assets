import { useState } from "react";
import { FileX2, FileText, ShieldAlert, BookMarked, Package } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import {
  PRODUCTS,
  REQUIREMENTS,
  SOURCES,
  LISTING_RULES,
  BANNED_CLAIMS,
  REVIEW_POLICY,
  PACKAGE_DOCS,
  type Product,
  type Requirement,
  type SourceId,
} from "@/data/launch";

type Tone = "pending" | "failed" | "inactive" | "info";

const TONE: Record<Tone, string> = {
  pending:
    "bg-amber-100 text-amber-900 border-amber-300 dark:bg-amber-950 dark:text-amber-100 dark:border-amber-800",
  failed:
    "bg-red-100 text-red-900 border-red-300 dark:bg-red-950 dark:text-red-100 dark:border-red-800",
  inactive:
    "bg-zinc-100 text-zinc-900 border-zinc-300 dark:bg-zinc-800 dark:text-zinc-100 dark:border-zinc-600",
  info: "bg-blue-100 text-blue-900 border-blue-300 dark:bg-blue-950 dark:text-blue-100 dark:border-blue-800",
};

function ToneBadge({ tone, children }: { tone: Tone; children: React.ReactNode }) {
  return (
    <Badge variant="outline" className={cn("gap-1.5 font-medium forced-colors:border-[CanvasText]", TONE[tone])}>
      <span aria-hidden="true" className="size-1.5 rounded-full bg-current" />
      {children}
    </Badge>
  );
}

function SourceRef({ id, section }: { id: SourceId; section: string }) {
  return (
    <span className="font-mono text-[11px] text-muted-foreground">
      {id} · {section}
    </span>
  );
}

function isMissing(p: Product, r: Requirement) {
  if (r.field === "imageAssets") return p.imageAssets.length === 0;
  return p[r.field] === null;
}

function Missing({ note }: { note: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded border border-dashed border-red-400 px-1.5 py-0.5 text-sm text-red-800 dark:border-red-700 dark:text-red-200">
      <span className="font-semibold">Missing</span>
      <span className="text-foreground">— {note}</span>
    </span>
  );
}

function GateDiagram({ product }: { product: Product }) {
  const rows = REQUIREMENTS.map((r, i) => ({ r, y: 40 + i * 64, missing: isMissing(product, r) }));
  const missingCount = rows.filter((x) => x.missing).length;
  return (
    <figure className="flex flex-col gap-2">
      <svg
        viewBox="0 0 640 230"
        className="w-full"
        role="img"
        aria-labelledby="gate-title gate-desc"
      >
        <title id="gate-title">Submission gate for {product.sku}</title>
        <desc id="gate-desc">
          {missingCount} of {REQUIREMENTS.length} required fields are missing: GTIN, approved images and warranty
          terms. The package is held at human review with status needs_review and approvedBy null. External
          submission has no integration in this app.
        </desc>
        {rows.map(({ r, y, missing }) => (
          <g key={r.field}>
            <path
              d={`M 200 ${y} C 250 ${y}, 250 115, 300 115`}
              fill="none"
              className="stroke-border"
              strokeWidth={2}
              strokeDasharray={missing ? "5 5" : undefined}
            />
            <rect x={10} y={y - 22} width={190} height={44} rx={6}
              className={missing ? "fill-red-50 stroke-red-500 dark:fill-red-950 dark:stroke-red-700" : "fill-card stroke-border"}
              strokeWidth={1.5} strokeDasharray={missing ? "4 3" : undefined} />
            <text x={24} y={y - 3} className="fill-foreground text-[13px] font-semibold">{r.label}</text>
            <text x={24} y={y + 13} className="fill-red-800 font-mono text-[10.5px] dark:fill-red-200">
              {missing ? r.code : "supplied"}
            </text>
            <g transform={`translate(176 ${y})`} aria-hidden="true">
              <line x1={-5} y1={-5} x2={5} y2={5} className="stroke-red-700 dark:stroke-red-300" strokeWidth={2} />
              <line x1={5} y1={-5} x2={-5} y2={5} className="stroke-red-700 dark:stroke-red-300" strokeWidth={2} />
            </g>
          </g>
        ))}
        <rect x={300} y={78} width={160} height={74} rx={6}
          className="fill-amber-50 stroke-amber-500 dark:fill-amber-950 dark:stroke-amber-600" strokeWidth={1.5} />
        <text x={314} y={102} className="fill-foreground text-[13px] font-semibold">Human review</text>
        <text x={314} y={120} className="fill-amber-900 font-mono text-[11px] dark:fill-amber-100">needs_review</text>
        <text x={314} y={138} className="fill-foreground font-mono text-[11px]">approvedBy: null</text>
        <line x1={460} y1={115} x2={500} y2={115} className="stroke-border" strokeWidth={2} strokeDasharray="5 5" />
        <rect x={500} y={84} width={130} height={62} rx={6} className="fill-muted stroke-border" strokeWidth={1.5} strokeDasharray="4 3" />
        <text x={512} y={108} className="fill-foreground text-[13px] font-semibold">Retailer</text>
        <text x={512} y={126} className="fill-foreground text-[11px]">submission: none</text>
      </svg>
      <figcaption className="text-xs text-muted-foreground">
        {missingCount} of {REQUIREMENTS.length} submission fields missing · {product.retailerCategory}
      </figcaption>
    </figure>
  );
}

function Section({ id, title, icon: Icon, count, children }: {
  id: string; title: string; icon: React.ElementType; count?: string; children: React.ReactNode;
}) {
  return (
    <section aria-labelledby={id} className="rounded-md border bg-card">
      <header className="flex items-center gap-2 border-b px-4 py-2.5">
        <Icon aria-hidden="true" className="size-4 text-muted-foreground" />
        <h2 id={id} className="text-sm font-semibold">{title}</h2>
        {count && <span className="ml-auto text-xs text-muted-foreground">{count}</span>}
      </header>
      <div className="p-4">{children}</div>
    </section>
  );
}

export function HomePage() {
  const [selectedId, setSelectedId] = useState(PRODUCTS[0].productId);
  const p = PRODUCTS.find((x) => x.productId === selectedId) ?? PRODUCTS[0];
  const missing = REQUIREMENTS.filter((r) => isMissing(p, r));

  return (
    <div className="flex h-full flex-col">
      <a href="#review" className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:rounded focus:bg-background focus:px-3 focus:py-2 focus:ring-2 focus:ring-ring">
        Skip to product review
      </a>
      <header className="border-b bg-card">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-x-6 gap-y-3 px-5 py-3">
          <div className="flex items-center gap-3">
            <span className="text-base font-semibold tracking-tight">Launch Review</span>
            <span
              className="rounded border-2 border-amber-600 bg-amber-100 px-2 py-0.5 font-mono text-[11px] font-bold tracking-wider text-amber-950 dark:bg-amber-950 dark:text-amber-100 forced-colors:border-[CanvasText]"
            >
              SYNTHETIC CONFERENCE DATA
            </span>
          </div>
          <nav aria-label="Products" className="flex flex-wrap gap-2 sm:ml-auto">
            {PRODUCTS.map((x) => {
              const active = x.productId === p.productId;
              return (
                <button
                  key={x.productId}
                  type="button"
                  aria-pressed={active}
                  onClick={() => setSelectedId(x.productId)}
                  className={cn(
                    "flex flex-col items-start rounded-md border px-3 py-1.5 text-left transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                    active ? "border-primary bg-primary text-primary-foreground" : "bg-background hover:bg-accent",
                  )}
                >
                  <span className="text-sm font-medium">{x.name}</span>
                  <span className={cn("font-mono text-xs", active ? "text-primary-foreground" : "text-muted-foreground")}>
                    SKU {x.sku}
                  </span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      <div id="review" tabIndex={-1} className="mx-auto w-full max-w-7xl flex-1 px-5 py-5 outline-none">
        <div className="mb-5 flex flex-wrap items-end gap-x-6 gap-y-2">
          <div>
            <p className="text-xs text-muted-foreground">{p.brand} · {p.productId}</p>
            <h1 className="text-xl font-semibold tracking-tight">{p.name}</h1>
          </div>
          <dl className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm">
            <div className="flex items-center gap-2"><dt className="text-muted-foreground">Status</dt><dd><ToneBadge tone="pending">needs_review</ToneBadge></dd></div>
            <div className="flex items-center gap-2"><dt className="text-muted-foreground">approvedBy</dt><dd className="font-mono">null</dd></div>
            <div className="flex items-center gap-2"><dt className="text-muted-foreground">Target launch</dt><dd className="font-mono">{p.targetLaunchDate}</dd></div>
            <div className="flex items-center gap-2"><dt className="text-muted-foreground">Blockers</dt><dd><ToneBadge tone="failed">{missing.length} missing</ToneBadge></dd></div>
          </dl>
        </div>

        <div className="grid gap-5 lg:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)]">
          <div className="flex flex-col gap-5">
            <Section id="missing-h" title="Missing requirements" icon={ShieldAlert} count={`${missing.length} of ${REQUIREMENTS.length}`}>
              <GateDiagram product={p} />
              <ul className="mt-4 divide-y border-t">
                {REQUIREMENTS.map((r) => (
                  <li key={r.field} className="grid gap-1 py-3 sm:grid-cols-[9rem_1fr]">
                    <div className="flex flex-col gap-1">
                      <span className="text-sm font-medium">{r.label}</span>
                      {isMissing(p, r) ? <ToneBadge tone="failed">{r.code}</ToneBadge> : <ToneBadge tone="info">supplied</ToneBadge>}
                    </div>
                    <div className="flex flex-col gap-1 text-sm">
                      <div><span className="font-mono text-xs text-muted-foreground">{r.field}: </span>
                        <span className="font-mono">{r.field === "imageAssets" ? "[]" : "null"}</span></div>
                      <Missing note={p.missingNotes[r.field]} />
                      <p>{r.policy}</p>
                      <SourceRef id="retailer-requirements-v1" section="Required for submission" />
                      <SourceRef id="manufacturer-products-v1" section="Missing onboarding information" />
                    </div>
                  </li>
                ))}
              </ul>
            </Section>

            <Section id="pkg-h" title="Launch package contents" icon={Package} count={`0 of ${PACKAGE_DOCS.length} available`}>
              <ul className="grid gap-2 sm:grid-cols-2">
                {PACKAGE_DOCS.map((d) => (
                  <li key={d.key} className="flex items-start gap-3 rounded-md border border-dashed p-3">
                    <FileX2 aria-hidden="true" className="mt-0.5 size-4 shrink-0 text-muted-foreground" />
                    <div className="flex flex-col gap-1">
                      <span className="text-sm font-medium">{d.label}</span>
                      <ToneBadge tone="inactive">Unavailable</ToneBadge>
                      <span className="text-xs text-foreground">Document not supplied; cannot be opened. No link.</span>
                    </div>
                  </li>
                ))}
              </ul>
              <div className="mt-4 rounded-md border p-3">
                <h3 className="mb-2 text-sm font-semibold">Review record fields</h3>
                <dl className="grid grid-cols-[8rem_1fr] gap-x-3 gap-y-1.5 text-sm">
                  <dt className="text-muted-foreground">productId</dt><dd className="font-mono">{p.productId}</dd>
                  <dt className="text-muted-foreground">status</dt><dd className="font-mono">{p.status}</dd>
                  <dt className="text-muted-foreground">approvedBy</dt><dd className="font-mono">null</dd>
                  <dt className="text-muted-foreground">blockers</dt><dd className="font-mono">{missing.map((r) => r.code).join(", ")}</dd>
                  <dt className="text-muted-foreground">Category reviewer</dt><dd><Missing note="not named in supplied data" /></dd>
                  <dt className="text-muted-foreground">Fact owner</dt><dd><Missing note="not named in supplied data" /></dd>
                </dl>
                <p className="mt-3 text-sm">{REVIEW_POLICY}</p>
                <div className="mt-1"><SourceRef id="retailer-requirements-v1" section="Human review and disposition" /></div>
              </div>
            </Section>
          </div>

          <div className="flex flex-col gap-5">
            <Section id="facts-h" title="Fact sheet" icon={FileText}>
              <dl className="grid grid-cols-[9rem_1fr] gap-x-3 gap-y-2 text-sm">
                <dt className="text-muted-foreground">SKU</dt><dd className="font-mono">{p.sku}</dd>
                <dt className="text-muted-foreground">Manufacturer MSRP</dt>
                <dd>
                  <span className="font-mono text-base font-semibold">{p.msrp.currency} {p.msrp.amount}</span>
                  <span className="ml-2 text-xs">({p.msrp.note})</span>
                </dd>
                <dt className="text-muted-foreground">Retailer selling price</dt><dd><Missing note="not supplied" /></dd>
                <dt className="text-muted-foreground">Manufacturer</dt><dd>{p.manufacturer}</dd>
                <dt className="text-muted-foreground">Mfr. category</dt><dd>{p.manufacturerCategory}</dd>
                <dt className="text-muted-foreground">Retailer category</dt><dd>{p.retailerCategory}</dd>
                <dt className="text-muted-foreground">Audience</dt><dd>{p.audience}</dd>
                <dt className="text-muted-foreground">GTIN</dt><dd><Missing note={p.missingNotes.gtin} /></dd>
                <dt className="text-muted-foreground">Warranty</dt><dd><Missing note={p.missingNotes.warrantyTerms} /></dd>
              </dl>
              <div className="mt-1"><SourceRef id="manufacturer-products-v1" section={p.name} /></div>

              <table className="mt-4 w-full text-sm">
                <caption className="mb-1 text-left text-sm font-semibold">Specifications</caption>
                <thead>
                  <tr className="border-b text-left text-xs text-muted-foreground">
                    <th scope="col" className="py-1.5 font-medium">Specification</th>
                    <th scope="col" className="py-1.5 text-right font-medium">Value</th>
                    <th scope="col" className="py-1.5 pl-3 font-medium">Unit</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {p.specs.map((s) => (
                    <tr key={s.label}>
                      <th scope="row" className="py-1.5 text-left font-normal">{s.label}</th>
                      <td className="py-1.5 text-right font-mono tabular-nums">{s.value}</td>
                      <td className="py-1.5 pl-3 font-mono">{s.unit ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <div>
                  <h3 className="mb-1 text-sm font-semibold">In the box</h3>
                  <ul className="list-disc pl-5 text-sm">{p.inTheBox.map((i) => <li key={i}>{i}</li>)}</ul>
                </div>
                <div>
                  <h3 className="mb-1 text-sm font-semibold">Approved images</h3>
                  <Missing note={p.missingNotes.imageAssets} />
                </div>
              </div>

              <h3 className="mb-1 mt-4 text-sm font-semibold">Approved listing bullets ({p.approvedBullets.length})</h3>
              <ol className="list-decimal pl-5 text-sm">{p.approvedBullets.map((b) => <li key={b}>{b}</li>)}</ol>
              <div className="mt-1"><SourceRef id="manufacturer-products-v1" section="Approved listing bullets" /></div>
            </Section>

            <Section id="src-h" title="Evidence and sources" icon={BookMarked} count={`${SOURCES.length} sources`}>
              <ul className="flex flex-col gap-3">
                {SOURCES.map((s) => (
                  <li key={s.id} className="rounded-md border p-3 text-sm">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-xs font-semibold">{s.id}</span>
                      <span className="rounded border border-amber-600 px-1.5 font-mono text-[10px] font-bold text-amber-900 dark:text-amber-100">{s.classification}</span>
                    </div>
                    <p className="mt-1 font-medium">{s.title}</p>
                    <p className="text-xs">{s.fileName} · schema {s.schemaVersion} · {s.owner}</p>
                    <p className="mt-1 text-xs">{s.disclaimer}</p>
                  </li>
                ))}
              </ul>
              <h3 className="mb-1 mt-4 text-sm font-semibold">Listing format</h3>
              <ul className="list-disc pl-5 text-sm">{LISTING_RULES.map((r) => <li key={r}>{r}</li>)}</ul>
              <h3 className="mb-1 mt-3 text-sm font-semibold">Prohibited claims</h3>
              <ul className="flex flex-wrap gap-1.5">
                {BANNED_CLAIMS.map((c) => (
                  <li key={c}><ToneBadge tone="failed">{c}</ToneBadge></li>
                ))}
              </ul>
              <div className="mt-1"><SourceRef id="retailer-requirements-v1" section="Listing format · Copy policy" /></div>
            </Section>
          </div>
        </div>
      </div>
    </div>
  );
}
