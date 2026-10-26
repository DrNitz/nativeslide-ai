/**
 * NativeSlide AI — Frontend API Client
 */
import { GenerationRequest, GenerationResponse, ThemeMood } from "../types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class NativeSlideAPI {
  private baseUrl: string;

  constructor(baseUrl: string = BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      Accept: "application/json",
      ...(options.headers || {}),
    };

    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      let errorDetail = "An unexpected error occurred.";
      try {
        const body = await res.json();
        errorDetail = body.detail || body.message || errorDetail;
      } catch {
        errorDetail = await res.text();
      }
      throw new Error(`API Error [${res.status}]: ${errorDetail}`);
    }

    return res.json() as Promise<T>;
  }

  async generateFromTopic(req: GenerationRequest): Promise<GenerationResponse> {
    return this.request<GenerationResponse>("/api/generate/from-topic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
  }

  async generateFromPDF(
    file: File,
    userId: string = "guest_user",
    numSlides: number = 15,
    themeOverride?: ThemeMood
  ): Promise<GenerationResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);
    formData.append("num_slides", numSlides.toString());
    if (themeOverride) {
      formData.append("theme_override", themeOverride);
    }

    const url = `${this.baseUrl}/api/generate/from-pdf`;
    const res = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Upload failed" }));
      throw new Error(err.detail || "PDF generation failed");
    }

    return res.json() as Promise<GenerationResponse>;
  }

  async getJobStatus(jobId: string): Promise<GenerationResponse> {
    return this.request<GenerationResponse>(`/api/generate/status/${jobId}`);
  }

  getDownloadUrl(jobId: string): string {
    return `${this.baseUrl}/api/generate/download/${jobId}`;
  }

  async checkHealth(): Promise<{ status: string; version: string; engine: string }> {
    return this.request<{ status: string; version: string; engine: string }>("/health");
  }
}

export const api = new NativeSlideAPI();
