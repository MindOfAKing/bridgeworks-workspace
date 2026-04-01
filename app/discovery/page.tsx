"use client";

import { useState, useRef } from "react";
import { Zap, ChevronRight, CheckCircle, Printer, Copy, Check } from "lucide-react";

// ── Types ──────────────────────────────────────────────────────────────────

interface FormData {
  // Section 1
  fullName: string;
  company: string;
  role: string;
  website: string;
  oneLiner: string;
  stage: string;
  // Section 2
  market: string;
  idealCustomer: string;
  geography: string;
  marketSize: string;
  problemSolved: string;
  // Section 3
  knownCompetitors: string;
  competitorStrengths: string;
  competitorWeaknesses: string;
  landscapeFamiliarity: string;
  // Section 4
  goals: string[];
  keyDecision: string;
  focusArea: string;
  // Section 5
  urgency: string;
  toolsUsed: string;
  additionalContext: string;
}

const EMPTY: FormData = {
  fullName: "", company: "", role: "", website: "", oneLiner: "", stage: "",
  market: "", idealCustomer: "", geography: "", marketSize: "", problemSolved: "",
  knownCompetitors: "", competitorStrengths: "", competitorWeaknesses: "", landscapeFamiliarity: "",
  goals: [], keyDecision: "", focusArea: "",
  urgency: "", toolsUsed: "", additionalContext: "",
};

const STAGE_OPTIONS = [
  "Idea / Pre-product",
  "Building MVP",
  "Launched, early users",
  "Scaling / Growing",
  "Established business",
];

const GOAL_OPTIONS = [
  "Understand who I'm up against",
  "Find underserved gaps to target",
  "Sharpen my positioning & messaging",
  "Validate my idea / market",
  "Inform product roadmap decisions",
  "Prepare for investor conversations",
  "Ongoing market monitoring",
];

const URGENCY_OPTIONS = ["This week (urgent)", "This month", "No hard deadline"];

const TOOLS_OPTIONS = [
  "No, this is new to me",
  "Tried free tools (Google, manual)",
  "Used paid tools (SimilarWeb, SEMrush, etc.)",
  "Hired a researcher / agency",
];

// ── Sub-components ─────────────────────────────────────────────────────────

function SectionHeader({ number, title, subtitle }: { number: number; title: string; subtitle?: string }) {
  return (
    <div
      className="flex items-center gap-3 mb-5 pb-3"
      style={{ borderBottom: "1px solid var(--border-subtle)" }}
    >
      <div
        className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-md text-xs font-bold text-white"
        style={{ backgroundColor: "var(--accent-blue)" }}
      >
        {number}
      </div>
      <span className="font-semibold text-sm" style={{ color: "var(--text-primary)" }}>
        {title}
      </span>
      {subtitle && (
        <span className="ml-auto text-xs" style={{ color: "var(--text-muted)" }}>
          {subtitle}
        </span>
      )}
    </div>
  );
}

function Label({ children, required }: { children: React.ReactNode; required?: boolean }) {
  return (
    <label className="mb-2 block text-xs font-medium" style={{ color: "var(--text-secondary)" }}>
      {children}
      {required && <span style={{ color: "var(--accent-blue)", marginLeft: 2 }}>*</span>}
    </label>
  );
}

function TextInput({
  value, onChange, placeholder,
}: { value: string; onChange: (v: string) => void; placeholder?: string }) {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full rounded-lg px-3 py-2 text-sm outline-none transition-colors"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        color: "var(--text-primary)",
      }}
      onFocus={(e) => (e.currentTarget.style.borderColor = "var(--accent-blue)")}
      onBlur={(e) => (e.currentTarget.style.borderColor = "var(--border-subtle)")}
    />
  );
}

function TextArea({
  value, onChange, placeholder, rows = 3,
}: { value: string; onChange: (v: string) => void; placeholder?: string; rows?: number }) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={rows}
      className="w-full resize-y rounded-lg px-3 py-2 text-sm outline-none transition-colors"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        color: "var(--text-primary)",
        minHeight: `${rows * 22}px`,
      }}
      onFocus={(e) => (e.currentTarget.style.borderColor = "var(--accent-blue)")}
      onBlur={(e) => (e.currentTarget.style.borderColor = "var(--border-subtle)")}
    />
  );
}

function RadioGroup({
  name, options, value, onChange,
}: { name: string; options: string[]; value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((opt) => (
        <button
          key={opt}
          type="button"
          onClick={() => onChange(opt)}
          className="rounded-full px-3 py-1 text-xs font-medium transition-all"
          style={{
            background: value === opt ? "var(--accent-blue)" : "var(--bg-elevated)",
            border: `1px solid ${value === opt ? "var(--accent-blue)" : "var(--border-subtle)"}`,
            color: value === opt ? "#fff" : "var(--text-secondary)",
          }}
        >
          {opt}
        </button>
      ))}
    </div>
  );
}

function CheckboxGroup({
  options, value, onChange,
}: { options: string[]; value: string[]; onChange: (v: string[]) => void }) {
  const toggle = (opt: string) => {
    onChange(value.includes(opt) ? value.filter((x) => x !== opt) : [...value, opt]);
  };
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((opt) => {
        const checked = value.includes(opt);
        return (
          <button
            key={opt}
            type="button"
            onClick={() => toggle(opt)}
            className="flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium transition-all"
            style={{
              background: checked ? "rgba(59,130,246,0.15)" : "var(--bg-elevated)",
              border: `1px solid ${checked ? "var(--accent-blue)" : "var(--border-subtle)"}`,
              color: checked ? "var(--accent-blue-bright)" : "var(--text-secondary)",
            }}
          >
            {checked && <Check className="h-3 w-3" />}
            {opt}
          </button>
        );
      })}
    </div>
  );
}

function ScaleInput({
  value, onChange,
}: { value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs" style={{ color: "var(--text-muted)" }}>Not at all</span>
      <div className="flex gap-2">
        {["1", "2", "3", "4", "5"].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            className="h-9 w-9 rounded-lg text-sm font-semibold transition-all"
            style={{
              background: value === n ? "var(--accent-blue)" : "var(--bg-elevated)",
              border: `1px solid ${value === n ? "var(--accent-blue)" : "var(--border-subtle)"}`,
              color: value === n ? "#fff" : "var(--text-secondary)",
            }}
          >
            {n}
          </button>
        ))}
      </div>
      <span className="text-xs" style={{ color: "var(--text-muted)" }}>Very well</span>
    </div>
  );
}

// ── Completion summary ─────────────────────────────────────────────────────

function CompletionView({ data, onReset }: { data: FormData; onReset: () => void }) {
  const [copied, setCopied] = useState(false);

  const summary = `BRIDGEWORKS Discovery Questionnaire
Completed: ${new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}

--- ABOUT YOU ---
Name: ${data.fullName}
Company: ${data.company}
Role: ${data.role}
Website: ${data.website}
One-liner: ${data.oneLiner}
Stage: ${data.stage}

--- MARKET ---
Market/Niche: ${data.market}
Ideal Customer: ${data.idealCustomer}
Geography: ${data.geography}
Market Size: ${data.marketSize}
Problem Solved: ${data.problemSolved}

--- COMPETITIVE LANDSCAPE ---
Known Competitors: ${data.knownCompetitors}
Competitor Strengths: ${data.competitorStrengths}
Competitor Weaknesses: ${data.competitorWeaknesses}
Landscape Familiarity: ${data.landscapeFamiliarity}/5

--- GOALS ---
Objectives: ${data.goals.join(", ")}
Key Decision: ${data.keyDecision}
Focus Area: ${data.focusArea}

--- CONTEXT ---
Urgency: ${data.urgency}
Tools Used: ${data.toolsUsed}
Additional Context: ${data.additionalContext}
`.trim();

  const handleCopy = () => {
    navigator.clipboard.writeText(summary).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handlePrint = () => window.print();

  return (
    <div
      className="rounded-xl p-8 text-center"
      style={{
        background: "var(--bg-surface)",
        border: "1px solid var(--border-subtle)",
        borderLeft: "3px solid var(--accent-blue)",
      }}
    >
      <div
        className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full"
        style={{ background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)" }}
      >
        <CheckCircle className="h-7 w-7" style={{ color: "var(--success)" }} />
      </div>
      <h2 className="mb-2 text-xl font-bold" style={{ color: "var(--text-primary)" }}>
        Questionnaire complete
      </h2>
      <p className="mb-6 text-sm" style={{ color: "var(--text-secondary)" }}>
        Thanks, {data.fullName.split(" ")[0] || "there"}. Your answers are ready — share them below or print for your records.
      </p>

      <div
        className="mb-6 rounded-lg p-4 text-left text-xs font-mono whitespace-pre-wrap overflow-auto max-h-64"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          color: "var(--text-secondary)",
        }}
      >
        {summary}
      </div>

      <div className="flex flex-wrap justify-center gap-3">
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-all"
          style={{
            background: copied ? "rgba(16,185,129,0.15)" : "var(--bg-elevated)",
            border: `1px solid ${copied ? "rgba(16,185,129,0.4)" : "var(--border-subtle)"}`,
            color: copied ? "var(--success)" : "var(--text-secondary)",
          }}
        >
          {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
          {copied ? "Copied!" : "Copy to clipboard"}
        </button>

        <button
          onClick={handlePrint}
          className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-all"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
            color: "var(--text-secondary)",
          }}
        >
          <Printer className="h-4 w-4" />
          Print / Save PDF
        </button>

        <button
          onClick={onReset}
          className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-all"
          style={{
            background: "var(--accent-blue)",
            border: "1px solid var(--accent-blue)",
            color: "#fff",
          }}
        >
          Start over
        </button>
      </div>
    </div>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────

export default function DiscoveryPage() {
  const [data, setData] = useState<FormData>(EMPTY);
  const [submitted, setSubmitted] = useState(false);
  const topRef = useRef<HTMLDivElement>(null);

  const set = (key: keyof FormData) => (value: string | string[]) =>
    setData((prev) => ({ ...prev, [key]: value }));

  const canSubmit = data.fullName.trim() !== "" && data.oneLiner.trim() !== "" && data.market.trim() !== "";

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    topRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleReset = () => {
    setData(EMPTY);
    setSubmitted(false);
    topRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div style={{ backgroundColor: "var(--bg-base)", minHeight: "100vh" }}>
      {/* Nav */}
      <header
        className="sticky top-0 z-10 border-b backdrop-blur-sm"
        style={{ backgroundColor: "rgba(10, 15, 30, 0.85)", borderColor: "var(--border-subtle)" }}
      >
        <div className="mx-auto flex max-w-3xl items-center justify-between px-4 py-3 sm:px-6">
          <a href="/" className="flex items-center gap-2 no-underline">
            <div
              className="flex h-7 w-7 items-center justify-center rounded-md"
              style={{ backgroundColor: "var(--accent-blue)" }}
            >
              <Zap className="h-4 w-4 text-white" />
            </div>
            <span className="font-bold tracking-tight" style={{ color: "var(--text-primary)" }}>
              BRIDGE<span style={{ color: "var(--accent-blue)" }}>WORKS</span>
            </span>
          </a>
          <span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
            Discovery Questionnaire
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6" ref={topRef}>
        {/* Intro */}
        <div
          className="mb-8 rounded-xl p-6"
          style={{
            background: "var(--bg-surface)",
            border: "1px solid var(--border-subtle)",
            borderLeft: "3px solid var(--accent-blue)",
          }}
        >
          <h1 className="mb-2 text-2xl font-bold tracking-tight" style={{ color: "var(--text-primary)" }}>
            Let&apos;s understand your{" "}
            <span style={{ color: "var(--accent-blue-bright)" }}>competitive landscape</span>
          </h1>
          <p className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
            This short questionnaire helps us tailor your BRIDGEWORKS experience so your first report hits the ground running.
            There are no right or wrong answers — the more context you give, the sharper the intelligence.
          </p>
        </div>

        {submitted ? (
          <CompletionView data={data} onReset={handleReset} />
        ) : (
          <form onSubmit={handleSubmit} className="space-y-8">

            {/* Section 1: About You */}
            <div
              className="rounded-xl p-6"
              style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}
            >
              <SectionHeader number={1} title="About You & Your Business" subtitle="~5 min" />
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <Label required>Full name</Label>
                  <TextInput value={data.fullName} onChange={set("fullName")} placeholder="Jane Smith" />
                </div>
                <div>
                  <Label>Company / Project name</Label>
                  <TextInput value={data.company} onChange={set("company")} placeholder="Acme Labs" />
                </div>
                <div>
                  <Label>Role / Title</Label>
                  <TextInput value={data.role} onChange={set("role")} placeholder="Founder & CEO" />
                </div>
                <div>
                  <Label>Website (if live)</Label>
                  <TextInput value={data.website} onChange={set("website")} placeholder="acmelabs.io" />
                </div>
              </div>
              <div className="mt-4">
                <Label required>In one sentence, what does your product or service do?</Label>
                <TextArea
                  value={data.oneLiner}
                  onChange={set("oneLiner")}
                  placeholder="e.g. We build AI-powered scheduling tools for independent personal trainers."
                  rows={2}
                />
              </div>
              <div className="mt-4">
                <Label required>What stage are you at?</Label>
                <RadioGroup name="stage" options={STAGE_OPTIONS} value={data.stage} onChange={set("stage")} />
              </div>
            </div>

            {/* Section 2: Market */}
            <div
              className="rounded-xl p-6"
              style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}
            >
              <SectionHeader number={2} title="Your Market & Niche" subtitle="~5 min" />
              <div className="space-y-4">
                <div>
                  <Label required>How would you describe your market or niche? <span style={{ color: "var(--text-muted)", fontStyle: "italic", fontWeight: 400 }}>(be as specific as possible)</span></Label>
                  <TextArea
                    value={data.market}
                    onChange={set("market")}
                    placeholder="e.g. Project management software for remote-first design agencies with 5–30 employees."
                  />
                </div>
                <div>
                  <Label>Who is your ideal customer? Describe them.</Label>
                  <TextArea
                    value={data.idealCustomer}
                    onChange={set("idealCustomer")}
                    placeholder="e.g. Founders or ops leads at Series A SaaS companies who are frustrated with Notion's lack of reporting..."
                  />
                </div>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div>
                    <Label>What geography are you targeting?</Label>
                    <TextInput value={data.geography} onChange={set("geography")} placeholder="e.g. US & UK, or Global" />
                  </div>
                  <div>
                    <Label>Estimated market size (rough is fine)</Label>
                    <TextInput value={data.marketSize} onChange={set("marketSize")} placeholder="e.g. ~$2B TAM" />
                  </div>
                </div>
                <div>
                  <Label>What problem does your customer have that your product solves?</Label>
                  <TextArea
                    value={data.problemSolved}
                    onChange={set("problemSolved")}
                    placeholder="Describe the pain in the customer's own words if you can..."
                  />
                </div>
              </div>
            </div>

            {/* Section 3: Competitive Landscape */}
            <div
              className="rounded-xl p-6"
              style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}
            >
              <SectionHeader number={3} title="Competitive Landscape" subtitle="~5 min" />
              <div className="space-y-4">
                <div>
                  <Label>List the competitors or alternatives you're aware of <span style={{ color: "var(--text-muted)", fontStyle: "italic", fontWeight: 400 }}>(names, URLs, or descriptions)</span></Label>
                  <TextArea
                    value={data.knownCompetitors}
                    onChange={set("knownCompetitors")}
                    placeholder="e.g. Notion, Linear, Asana — also a few indie tools like Height.app..."
                  />
                </div>
                <div>
                  <Label>What do your competitors do well? What do customers like about them?</Label>
                  <TextArea
                    value={data.competitorStrengths}
                    onChange={set("competitorStrengths")}
                    placeholder="Be honest — this helps us identify real gaps, not just spin..."
                  />
                </div>
                <div>
                  <Label>Where do your competitors fall short? What complaints do you hear?</Label>
                  <TextArea
                    value={data.competitorWeaknesses}
                    onChange={set("competitorWeaknesses")}
                    placeholder="e.g. Too complex for small teams, pricing jumps too fast, missing a specific feature..."
                  />
                </div>
                <div>
                  <Label>How familiar are you with your competitive landscape right now?</Label>
                  <ScaleInput value={data.landscapeFamiliarity} onChange={set("landscapeFamiliarity")} />
                </div>
              </div>
            </div>

            {/* Section 4: Goals */}
            <div
              className="rounded-xl p-6"
              style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}
            >
              <SectionHeader number={4} title="Goals & What You're Looking For" subtitle="~3 min" />
              <div className="space-y-4">
                <div>
                  <Label>What are you hoping to get from competitive intelligence? <span style={{ color: "var(--text-muted)", fontStyle: "italic", fontWeight: 400 }}>(select all that apply)</span></Label>
                  <CheckboxGroup options={GOAL_OPTIONS} value={data.goals} onChange={(v) => set("goals")(v)} />
                </div>
                <div>
                  <Label>What's the most important decision you're trying to make right now?</Label>
                  <TextArea
                    value={data.keyDecision}
                    onChange={set("keyDecision")}
                    placeholder="e.g. Whether to pivot our ICP, or how to position against Competitor X in sales conversations..."
                  />
                </div>
                <div>
                  <Label>Is there a specific competitor, trend, or segment you most want to understand?</Label>
                  <TextArea
                    value={data.focusArea}
                    onChange={set("focusArea")}
                    placeholder="e.g. We keep losing to Competitor Y — we want to understand why and what to say..."
                  />
                </div>
              </div>
            </div>

            {/* Section 5: Context */}
            <div
              className="rounded-xl p-6"
              style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}
            >
              <SectionHeader number={5} title="Context & Constraints" subtitle="~2 min" />
              <div className="space-y-4">
                <div>
                  <Label>How urgently do you need this intelligence?</Label>
                  <RadioGroup name="urgency" options={URGENCY_OPTIONS} value={data.urgency} onChange={set("urgency")} />
                </div>
                <div>
                  <Label>Have you used any market research or competitive intelligence tools before?</Label>
                  <RadioGroup name="toolsUsed" options={TOOLS_OPTIONS} value={data.toolsUsed} onChange={set("toolsUsed")} />
                </div>
                <div>
                  <Label>Anything else we should know before our call? <span style={{ color: "var(--text-muted)", fontStyle: "italic", fontWeight: 400 }}>(constraints, sensitivities, context)</span></Label>
                  <TextArea
                    value={data.additionalContext}
                    onChange={set("additionalContext")}
                    placeholder="e.g. We're pre-launch and in stealth — please keep all info confidential..."
                    rows={3}
                  />
                </div>
              </div>
            </div>

            {/* Submit */}
            <div className="flex items-center justify-between">
              <p className="text-xs" style={{ color: "var(--text-muted)" }}>
                Fields marked <span style={{ color: "var(--accent-blue)" }}>*</span> are required.
              </p>
              <button
                type="submit"
                disabled={!canSubmit}
                className="flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-semibold transition-all disabled:opacity-40"
                style={{
                  background: canSubmit ? "var(--accent-blue)" : "var(--bg-elevated)",
                  border: "1px solid var(--accent-blue)",
                  color: canSubmit ? "#fff" : "var(--text-muted)",
                  cursor: canSubmit ? "pointer" : "not-allowed",
                }}
              >
                Submit questionnaire
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>

          </form>
        )}
      </main>

      {/* Footer */}
      <footer
        className="mt-16 border-t px-4 py-6 text-center text-xs"
        style={{ borderColor: "var(--border-subtle)", color: "var(--text-muted)" }}
      >
        <strong style={{ color: "var(--text-secondary)" }}>
          BRIDGE<span style={{ color: "var(--accent-blue)" }}>WORKS</span>
        </strong>
        {" · "}Competitive Intelligence, Powered by AI
        {" · "}Confidential
      </footer>
    </div>
  );
}
