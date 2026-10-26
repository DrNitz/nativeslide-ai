import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "NativeSlide AI — 100% Native Editable PowerPoint Decks in Seconds",
  description:
    "Transform any PDF, research paper, or topic into a fully editable, executive-grade PowerPoint presentation with native DrawingML vector cards and deep speaker notes.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-950 text-slate-100 font-sans">
        {children}
      </body>
    </html>
  );
}
