import Link from "next/link";
import GenerationStudio from "../../components/studio/GenerationStudio";

export const metadata = {
  title: "Generation Studio — NativeSlide AI",
  description: "Generate 100% editable DrawingML PowerPoint decks from PDF or topic prompts.",
};

export default function StudioPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950">
      <header className="border-b border-slate-900/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-black text-slate-950 text-base">
              N
            </div>
            <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              NativeSlide<span className="text-cyan-400">.ai</span>
            </span>
          </Link>

          <div className="flex items-center gap-4">
            <span className="hidden sm:inline-block text-xs font-semibold px-3 py-1 bg-cyan-950/60 border border-cyan-800/60 text-cyan-400 rounded-full">
              ✦ 100% Native Vector DrawingML
            </span>
            <Link
              href="/"
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg transition-all"
            >
              ← Back to Home
            </Link>
          </div>
        </div>
      </header>

      <section className="pt-12 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center mb-8 space-y-2">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
            Native Presentation Studio
          </h1>
          <p className="text-sm text-slate-400">
            Generate publication-ready DrawingML slides with custom domain theming and presenter notes.
          </p>
        </div>
        <GenerationStudio />
      </section>

      <footer className="border-t border-slate-900 py-6 px-6 text-center text-xs text-slate-500">
        <p>© 2026 NativeSlide AI. Built under Business Source License 1.1 (BUSL-1.1).</p>
      </footer>
    </main>
  );
}
