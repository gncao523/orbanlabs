"use client";

import { useState, useEffect, useCallback } from "react";
import { createShortUrl, listShortUrls, ShortUrl } from "@/lib/api";

export default function Home() {
  const [longUrl, setLongUrl] = useState("");
  const [urls, setUrls] = useState<ShortUrl[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const loadUrls = useCallback(async () => {
    setLoading(true);
    setError(null);
    const { data, error: err } = await listShortUrls();
    setLoading(false);
    if (err) setError(err);
    else if (data) setUrls(data);
  }, []);

  useEffect(() => {
    loadUrls();
  }, [loadUrls]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setSubmitting(true);

    const trimmed = longUrl.trim();
    if (!trimmed) {
      setError("Please enter a URL");
      setSubmitting(false);
      return;
    }
    if (!trimmed.startsWith("http://") && !trimmed.startsWith("https://")) {
      setError("URL must start with http:// or https://");
      setSubmitting(false);
      return;
    }

    const { data, error: err } = await createShortUrl(trimmed);
    setSubmitting(false);

    if (err) {
      setError(err);
      return;
    }
    if (data) {
      setSuccess(data.full_short_url);
      setLongUrl("");
      loadUrls();
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <main style={{ padding: "2rem 0" }}>
      <h1>URL Shortener</h1>
      <p style={{ marginBottom: "2rem", color: "#8b949e" }}>
        Paste a long URL and get a short link. Track how many times it&apos;s been clicked.
      </p>

      <form
        onSubmit={handleSubmit}
        style={{
          marginBottom: "2rem",
          display: "flex",
          gap: "0.75rem",
          flexWrap: "wrap",
          alignItems: "flex-start",
        }}
      >
        <div style={{ flex: "1 1 300px", minWidth: 0 }}>
          <input
            type="url"
            placeholder="https://example.com/very/long/url"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            disabled={submitting}
            style={{ width: "100%" }}
          />
        </div>
        <button
          type="submit"
          className="primary"
          disabled={submitting}
        >
          {submitting ? (
            <>
              <span className="loading-spinner" />
              Shortening...
            </>
          ) : (
            "Shorten"
          )}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}
      {success && (
        <div className="success-message">
          Created! Short URL:{" "}
          <a href={success} target="_blank" rel="noopener noreferrer">
            {success}
          </a>
          <button
            type="button"
            onClick={() => copyToClipboard(success)}
            style={{ marginLeft: "0.5rem", padding: "0.25rem 0.5rem" }}
          >
            Copy
          </button>
        </div>
      )}

      <h2 style={{ marginTop: "2.5rem", marginBottom: "1rem" }}>Your URLs</h2>

      {loading && (
        <p style={{ color: "#8b949e" }}>
          <span className="loading-spinner" />
          Loading...
        </p>
      )}
      {!loading && error && <div className="error-message">{error}</div>}
      {!loading && !error && urls.length === 0 && (
        <p style={{ color: "#8b949e" }}>No short URLs yet. Create one above.</p>
      )}
      {!loading && !error && urls.length > 0 && (
        <ul style={{ listStyle: "none" }}>
          {urls.map((u) => (
            <li
              key={u.short_code}
              style={{
                padding: "1rem 1.25rem",
                marginBottom: "0.5rem",
                background: "#161b22",
                border: "1px solid #30363d",
                borderRadius: "8px",
              }}
            >
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem", alignItems: "center" }}>
                <a
                  href={u.full_short_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ fontWeight: 600, fontSize: "1rem" }}
                >
                  {u.full_short_url}
                </a>
                <button
                  type="button"
                  onClick={() => copyToClipboard(u.full_short_url)}
                  style={{ padding: "0.25rem 0.5rem", fontSize: "0.85rem" }}
                >
                  Copy
                </button>
              </div>
              <p style={{ marginTop: "0.25rem", color: "#8b949e", fontSize: "0.9rem", wordBreak: "break-all" }}>
                → {u.long_url}
              </p>
              <p style={{ marginTop: "0.5rem", fontSize: "0.85rem", color: "#58a6ff" }}>
                {u.click_count} click{u.click_count !== 1 ? "s" : ""}
              </p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
