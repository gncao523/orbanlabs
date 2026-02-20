'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { createNote } from '@/lib/api'

export default function NewNotePage() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [tagsInput, setTagsInput] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const tags = tagsInput
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    const { data, error: err } = await createNote({ title, body, tags })
    setSubmitting(false)
    if (err) {
      setError(err)
      return
    }
    if (data) router.push(`/notes/${data.id}`)
  }

  return (
    <main>
      <h1>New Note</h1>
      <Link href="/" style={{ display: 'inline-block', marginBottom: '1rem' }}>← Back to notes</Link>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} style={{ maxWidth: '600px' }}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="title" style={{ display: 'block', marginBottom: '0.25rem' }}>Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="body" style={{ display: 'block', marginBottom: '0.25rem' }}>Body</label>
          <textarea
            id="body"
            rows={8}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="tags" style={{ display: 'block', marginBottom: '0.25rem' }}>Tags (comma-separated)</label>
          <input
            id="tags"
            type="text"
            value={tagsInput}
            onChange={(e) => setTagsInput(e.target.value)}
            placeholder="work, ideas, personal"
          />
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button type="submit" className="primary" disabled={submitting}>
            {submitting ? 'Creating...' : 'Create Note'}
          </button>
          <Link href="/">
            <button type="button">Cancel</button>
          </Link>
        </div>
      </form>
    </main>
  )
}
