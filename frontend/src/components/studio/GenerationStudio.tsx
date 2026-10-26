"use client";

import React, { useState } from "react";
import { api } from "../../lib/api";
import { GenerationResponse, ThemeMood } from "../../types";

const THEME_OPTIONS: { label: string; value: ThemeMood | "AUTO" }[] = [
  { label: "✨ Auto-Detect Topic", value: "AUTO" },
  { label: "🩺 Medicine & Clinical", value: ThemeMood.MEDICINE_CLINICAL },
  { label: "🚀 Space & Astronomy", value: ThemeMood.SPACE_ASTRONOMY },
  { label: "⚡ AI & Machine Learning", value: ThemeMood.AI_ML_TECH },
  { label: "⚖️ Law & Judiciary", value: ThemeMood.LAW_JUDICIARY },
  { label: "🏛️ Architecture & Design", value: ThemeMood.ARCHITECTURE_DESIGN },
  { label: "📈 Finance & Business", value: ThemeMood.FINANCE_BUSINESS },
  { label: "🎓 Academic & Education", value: ThemeMood.EDUCATION_ACADEMIC },
  { label: "⚙️ Engineering & Systems", value: ThemeMood.ENGINEERING_TECHNICAL },
];

export default function GenerationStudio() {
  const [activeTab, setActiveTab] = useState<"topic" | "pdf" | "paste">("topic");
  const [topic, setTopic] = useState("");
  const [pastedContent, setPastedContent] = useState("");
  const [numSlides, setNumSlides] = useState(15);
  const [selectedTheme, setSelectedTheme] = useState<ThemeMood | "AUTO">("AUTO");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState("");
  const [result, setResult] = useState<GenerationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      if (!f.name.toLowerCase().endsWith(".pdf")) {
        setError("Only PDF documents are supported.");
        return;
      }
      setSelectedFile(f);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setIsGenerating(true);

    try {
      setGenerationStep("Analyzing domain & document structure...");
      await new Promise((r) => setTimeout(r, 600));

      setGenerationStep("Extracting key metrics, comparison tables & cases...");
      await new Promise((r) => setTimeout(r, 800));

      setGenerationStep("Rendering 100% native DrawingML vector cards & tables...");

      let res: GenerationResponse;
      const themeParam = selectedTheme === "AUTO" ? undefined : selectedTheme;

      if (activeTab === "pdf") {
        if (!selectedFile) {
          throw new Error("Please select a PDF file to upload.");
        }
        res = await api.generateFromPDF(selectedFile, "guest_user", numSlides, themeParam);
      } else {
        const promptTopic = activeTab === "topic" ? topic : "Comprehensive Analysis";
        const promptContent = activeTab === "paste" ? pastedContent : topic;

        if (!promptContent.trim()) {
          throw new Error("Please enter a topic or paste content.");
        }

        res = await api.generateFromTopic({
          topic: promptTopic,
          content_text: promptContent,
          num_slides: numSlides,
          theme_override: themeParam,
          user_id: "guest_user",
        });
      }

      setGenerationStep("Finalizing publication-grade presenter speaker notes...");
      await new Promise((r) => setTimeout(r, 400));

      setResult(res);
    } catch (err: any) {
      setError(err.message || "Presentation generation failed. Please try again.");
    } finally {
      setIsGenerating(false);
      setGenerationStep("");
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-10 shadow-2xl">
      {/* Mode Switcher Tabs */}
      <div className="flex border-b border-slate-800 mb-8 pb-3 gap-2 sm:gap-4 overflow-x-auto">
        <button
          type="button"
          onClick={() => setActiveTab("topic")}
          className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
            activeTab === "topic"
              ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30"
              : "text-slate-400 hover:text-white"
          }`}
        >
          💡 Describe Topic / Prompt
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("pdf")}
          className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
            activeTab === "pdf"
              ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30"
              : "text-slate-400 hover:text-white"
          }`}
        >
          📄 Upload PDF Document
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("paste")}
          className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
            activeTab === "paste"
              ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30"
              : "text-slate-400 hover:text-white"
          }`}
        >
          📋 Paste Raw Text / Notes
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Tab 1: Topic */}
        {activeTab === "topic" && (
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              What should this presentation be about?
            </label>
            <textarea
              rows={4}
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Systemic Arterial Hypertension management per Harrison's Internal Medicine Ch. 277, or Transformer Architecture in Machine Learning, or The James Webb Space Telescope discoveries..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 text-sm"
            />
          </div>
        )}

        {/* Tab 2: PDF Upload */}
        {activeTab === "pdf" && (
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              Upload PDF Document (up to 25 MB)
            </label>
            <div className="border-2 border-dashed border-slate-700 hover:border-cyan-500 rounded-xl p-8 text-center bg-slate-950/50 transition-all cursor-pointer relative">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              <div className="space-y-2">
                <span className="text-3xl">📥</span>
                <p className="text-sm font-medium text-slate-300">
                  {selectedFile ? selectedFile.name : "Drop your PDF paper, syllabus, or report here"}
                </p>
                <p className="text-xs text-slate-500">
                  {selectedFile
                    ? `${(selectedFile.size / (1024 * 1024)).toFixed(2)} MB ready for processing`
                    : "Supports papers, textbooks, contracts, clinical guidelines, and reports"}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Paste Content */}
        {activeTab === "paste" && (
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              Paste Outline, Lecture Notes, or Article Text
            </label>
            <textarea
              rows={6}
              value={pastedContent}
              onChange={(e) => setPastedContent(e.target.value)}
              placeholder="Paste raw notes, research abstract, or outline here. The engine will synthesize key points, structure cards, and generate comparison tables automatically."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 text-sm"
            />
          </div>
        )}

        {/* Deck Configuration Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          {/* Slide Count */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Number of Slides
            </label>
            <select
              value={numSlides}
              onChange={(e) => setNumSlides(Number(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              <option value={7}>7 Slides (Quick Executive Pitch)</option>
              <option value={10}>10 Slides (Standard Briefing)</option>
              <option value={15}>15 Slides (Comprehensive Masterclass - Free Tier)</option>
            </select>
          </div>

          {/* Theme Mood */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Visual Palette & Typography
            </label>
            <select
              value={selectedTheme}
              onChange={(e) => setSelectedTheme(e.target.value as any)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              {THEME_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-4 bg-rose-950/50 border border-rose-800/80 rounded-xl text-rose-300 text-sm flex items-start gap-3">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Progress State */}
        {isGenerating && (
          <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
            <div className="flex items-center gap-3">
              <div className="w-5 h-5 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
              <span className="text-sm font-semibold text-cyan-400">Building Native DrawingML Presentation...</span>
            </div>
            <p className="text-xs text-slate-400 pl-8">{generationStep}</p>
          </div>
        )}

        {/* Result & Download Box */}
        {result && (
          <div className="p-6 bg-emerald-950/40 border border-emerald-800/80 rounded-xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-base font-bold text-emerald-400">🎉 Presentation Generated Successfully!</h4>
                <p className="text-xs text-slate-300 mt-1">
                  {result.slide_count} slides ready • 100% Native vector shapes • Includes deep speaker notes
                </p>
              </div>
              <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-full text-xs font-semibold">
                Available for 48 Hours
              </span>
            </div>

            <div className="pt-2">
              <a
                href={api.getDownloadUrl(result.job_id)}
                download
                className="inline-flex items-center justify-center gap-2 w-full sm:w-auto px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-sm transition-all shadow-lg shadow-emerald-500/20"
              >
                📥 Download Native PowerPoint (.pptx)
              </a>
            </div>
          </div>
        )}

        {/* Submit Button */}
        {!result && (
          <button
            type="submit"
            disabled={isGenerating}
            className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-base transition-all shadow-xl shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isGenerating ? "Engine Generating..." : "⚡ Generate Executive Presentation (Instant Free Download)"}
          </button>
        )}
      </form>
    </div>
  );
}
