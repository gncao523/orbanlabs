'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { fetchNote, updateNote, deleteNote } from '@/lib/api'

export default function NoteDetailPage() {
  const router = useRouter()
  const params = useParams()
  const id = Number(params.id)
  const [note, setNote] = useState<{ title: string; body: string; tags: string[] } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editing, setEditing] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError(null)
      const { data, error: err } = await fetchNote(id)
      setLoading(false)
      if (err) setError(err)
      else if (data) setNote({ title: data.title, body: data.body, tags: data.tags })
    }
    if (!isNaN(id)) load()
  }, [id])

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!note) return
    setError(null)
    setSubmitting(true)
    const { error: err } = await updateNote(id, {
      title: note.title,
      body: note.body,
      tags: note.tags,
    })
    setSubmitting(false)
    if (err) setError(err)
    else setEditing(false)
  }

  const handleDelete = async () => {
    if (!confirm('Delete this note?')) return
    setError(null)
    setSubmitting(true)
    const { error: err } = await deleteNote(id)
    setSubmitting(false)
    if (err) setError(err)
    else router.push('/')
  }

  if (loading) return <p>Loading...</p>
  if (error && !note) return <><div className="error-message">{error}</div><Link href="/">← Back</Link></>
  if (!note) return null

  const tagsInput = note.tags.join(', ')

  return (
    <main>
      <Link href="/" style={{ display: 'inline-block', marginBottom: '1rem' }}>← Back to notes</Link>

      {error && <div className="error-message">{error}</div>}

      {editing ? (
        <form onSubmit={handleUpdate} style={{ maxWidth: '600px' }}>
          <h1>Edit Note</h1>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="title">Title</label>
            <input
              id="title"
              value={note.title}
              onChange={(e) => setNote({ ...note, title: e.target.value })}
              required
              maxLength={200}
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="body">Body</label>
            <textarea
              id="body"
              rows={8}
              value={note.body}
              onChange={(e) => setNote({ ...note, body: e.target.value })}
              required
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="tags">Tags (comma-separated)</label>
            <input
              id="tags"
              value={tagsInput}
              onChange={(e) =>
                setNote({
                  ...note,
                  tags: e.target.value.split(',').map((t) => t.trim()).filter(Boolean),
                })
              }
            />
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button type="submit" className="primary" disabled={submitting}>
              {submitting ? 'Saving...' : 'Save'}
            </button>
            <button type="button" onClick={() => setEditing(false)}>Cancel</button>
          </div>
        </form>
      ) : (
        <>
          <h1>{note.title}</h1>
          <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', margin: '1rem 0' }}>
            {note.body}
          </pre>
          {note.tags.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              {note.tags.map((t) => (
                <span
                  key={t}
                  style={{
                    marginRight: '0.25rem',
                    padding: '0.2rem 0.5rem',
                    background: '#e0e0e0',
                    borderRadius: '4px',
                    fontSize: '0.8rem',
                  }}
                >
                  {t}
                </span>
              ))}
            </div>
          )}
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="primary" onClick={() => setEditing(true)} disabled={submitting}>
              Edit
            </button>
            <button className="danger" onClick={handleDelete} disabled={submitting}>
              Delete
            </button>
          </div>
        </>
      )}
    </main>
  )
}
