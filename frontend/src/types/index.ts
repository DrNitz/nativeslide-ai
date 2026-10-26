/**
 * NativeSlide AI — Shared TypeScript Type Definitions
 */

export enum SlideLayout {
  TABLE_MATRIX = "TABLE_MATRIX",
  CARDS_3X2 = "CARDS_3X2",
  CASE_SCENARIOS = "CASE_SCENARIOS",
  METRICS_CALLOUT = "METRICS_CALLOUT",
  COMPARISON_2COL = "COMPARISON_2COL",
  PROCESS_STEPS = "PROCESS_STEPS",
  TITLE_HERO = "TITLE_HERO",
  SECTION_DIVIDER = "SECTION_DIVIDER",
}

export enum ThemeMood {
  MEDICINE_CLINICAL = "MEDICINE_CLINICAL",
  SPACE_ASTRONOMY = "SPACE_ASTRONOMY",
  AI_ML_TECH = "AI_ML_TECH",
  LAW_JUDICIARY = "LAW_JUDICIARY",
  ARCHITECTURE_DESIGN = "ARCHITECTURE_DESIGN",
  FINANCE_BUSINESS = "FINANCE_BUSINESS",
  EDUCATION_ACADEMIC = "EDUCATION_ACADEMIC",
  ENGINEERING_TECHNICAL = "ENGINEERING_TECHNICAL",
}

export interface MetricItem {
  value: string;
  label: string;
  description: string;
  accent_color?: string | null;
}

export interface CardItem {
  title: string;
  subtitle?: string | null;
  body: string;
  accent_color?: string | null;
}

export interface TableData {
  headers: string[];
  rows: string[][];
  column_widths?: number[] | null;
}

export interface SlideSpec {
  slide_number: number;
  layout: SlideLayout;
  title: string;
  kicker?: string | null;
  metrics?: MetricItem[] | null;
  cards?: CardItem[] | null;
  table?: TableData | null;
  body_text?: string | null;
  speaker_notes: string;
}

export interface DeckSpec {
  title: string;
  total_slides: number;
  theme_mood: ThemeMood;
  slides: SlideSpec[];
  generated_at: string;
}

export interface GenerationRequest {
  topic?: string;
  content_text?: string;
  num_slides?: number;
  theme_override?: ThemeMood;
  user_id?: string;
}

export interface GenerationResponse {
  job_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  download_url?: string | null;
  slide_count?: number | null;
  theme_used?: ThemeMood | null;
  created_at: string;
  expires_at: string;
}

export interface UserCredits {
  user_id: string;
  free_credits_remaining: number;
  trial_expires_at: string;
  is_pro: boolean;
}

export interface ApiError {
  status: number;
  message: string;
  detail?: string | null;
}
