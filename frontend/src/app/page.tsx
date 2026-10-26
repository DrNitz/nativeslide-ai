import Link from "next/link";
import GenerationStudio from "../components/studio/GenerationStudio";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950">
      {/* Navigation */}
      <header className="border-b border-slate-900/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-black text-slate-950 text-base">
              N
            </div>
            <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              NativeSlide<span className="text-cyan-400">.ai</span>
            </span>
          </div>

          <div className="flex items-center gap-4">
            <span className="hidden sm:inline-block text-xs font-semibold px-3 py-1 bg-cyan-950/60 border border-cyan-800/60 text-cyan-400 rounded-full">
              ✦ 100% Native Vector DrawingML
            </span>
            <Link
              href="#studio"
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg transition-all"
            >
              Start Free Trial
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-20 pb-16 px-6 text-center max-w-4xl mx-auto space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-300 text-xs font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Zero Raster Images • Fully Editable in Microsoft PowerPoint & Keynote
        </div>

        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
          Turn Any Paper, PDF, or Topic Into an{" "}
          <span className="bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-500 bg-clip-text text-transparent">
            Executive PowerPoint Deck
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Say goodbye to generic AI slides with flat screenshot images. NativeSlide generates{" "}
          <strong>true OpenXML vector cards, native data tables, and deep presenter speaker notes</strong> in under 30 seconds.
        </p>
      </section>

      {/* Interactive Creation Studio */}
      <section id="studio" className="px-6 pb-24">
        <GenerationStudio />
      </section>

      {/* The Differentiator: Comparison Section */}
      <section className="py-20 border-t border-slate-900 bg-slate-900/40 px-6">
        <div className="max-w-5xl mx-auto space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">
              Why Professionals & Academics Switch to NativeSlide
            </h2>
            <p className="text-sm text-slate-400">
              Built specifically for clinical fellows, engineers, lawyers, and founders who demand publication-grade presentations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-950 border border-slate-800 p-6 rounded-2xl space-y-3">
              <span className="text-3xl">📐</span>
              <h3 className="font-bold text-base text-slate-100">100% Native Vector Elements</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Every box is a real DrawingML rounded rectangle. Every table is a genuine PowerPoint table. Change fonts, re-color borders, or edit values without broken layouts.
              </p>
            </div>

            <div className="bg-slate-950 border border-slate-800 p-6 rounded-2xl space-y-3">
              <span className="text-3xl">🎭</span>
              <h3 className="font-bold text-base text-slate-100">Chameleon Theming Engine</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Astronomy papers receive a dark cosmic navy palette with electric cyan accents. Medical decks receive clinical slate with crisp teal. The 60-30-10 color rule applies automatically.
              </p>
            </div>

            <div className="bg-slate-950 border border-slate-800 p-6 rounded-2xl space-y-3">
              <span className="text-3xl">🎙️</span>
              <h3 className="font-bold text-base text-slate-100">Deep Clinical & Executive Notes</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Never present without context. Every slide embeds 3 to 5 sentences of rigorous speaker notes directly into PowerPoint Presenter View, ready for your lecture or board meeting.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing / Freemium Section */}
      <section className="py-20 px-6 border-t border-slate-900">
        <div className="max-w-4xl mx-auto space-y-12">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">Simple, Transparent Pricing</h2>
            <p className="text-sm text-slate-400">Start with our free trial. Upgrade only when you need high-volume generation.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {/* Free */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">Free Trial</span>
              <div className="text-3xl font-black text-white">$0</div>
              <p className="text-xs text-slate-400">Full access for 48 hours to create your first presentation.</p>
              <ul className="text-xs text-slate-300 space-y-2 pt-2 border-t border-slate-800">
                <li>✓ 1 Executive Deck (Up to 15 slides)</li>
                <li>✓ 100% Native DrawingML vector shapes</li>
                <li>✓ Full presenter speaker notes</li>
                <li>✓ 48-Hour download window</li>
              </ul>
            </div>

            {/* Day Pass */}
            <div className="bg-gradient-to-b from-cyan-950/40 to-slate-900 border-2 border-cyan-500/60 p-6 rounded-2xl space-y-4 relative shadow-xl shadow-cyan-950/50">
              <span className="absolute -top-3 right-4 px-2 py-0.5 bg-cyan-400 text-slate-950 text-[10px] font-black uppercase rounded-full tracking-wider">
                Most Popular
              </span>
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">24-Hour Day Pass</span>
              <div className="text-3xl font-black text-white">$3.99</div>
              <p className="text-xs text-slate-300">Need it tonight? Unlock 3 presentations today with zero watermarks.</p>
              <ul className="text-xs text-slate-200 space-y-2 pt-2 border-t border-slate-800">
                <li>✓ 3 Executive Decks (Up to 25 slides each)</li>
                <li>✓ Zero watermarks</li>
                <li>✓ Priority generation queue</li>
                <li>✓ PDF document upload up to 50 MB</li>
              </ul>
            </div>

            {/* Monthly Pro */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Pro Monthly</span>
              <div className="text-3xl font-black text-white">$12<span className="text-sm font-normal text-slate-500">/mo</span></div>
              <p className="text-xs text-slate-400">For professors, researchers, doctors, and active consultants.</p>
              <ul className="text-xs text-slate-300 space-y-2 pt-2 border-t border-slate-800">
                <li>✓ Unlimited presentation generations</li>
                <li>✓ Up to 40 slides per deck</li>
                <li>✓ Custom brand color hex overrides</li>
                <li>✓ Dedicated priority support</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-8 px-6 text-center text-xs text-slate-500">
        <p>© 2026 NativeSlide AI. Built under Business Source License 1.1 (BUSL-1.1). Powered by Python, FastAPI, and OpenXML.</p>
      </footer>
    </main>
  );
}
