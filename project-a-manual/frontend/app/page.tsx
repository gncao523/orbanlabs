'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { fetchNotes, Note } from '@/lib/api'

export default function Home() {
  const [notes, setNotes] = useState<Note[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tagFilter, setTagFilter] = useState('')
  const [keywordFilter, setKeywordFilter] = useState('')

  const loadNotes = async () => {
    setLoading(true)
    setError(null)
    const { data, error: err } = await fetchNotes(
      tagFilter || undefined,
      keywordFilter || undefined
    )
    setLoading(false)
    if (err) setError(err)
    else if (data) setNotes(data)
  }

  useEffect(() => {
    loadNotes()
  }, [])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    loadNotes()
  }

  return (
    <main>
      <h1>Notes</h1>
      <p style={{ marginBottom: '1rem' }}>Create and manage your notes.</p>

      <form onSubmit={handleSearch} style={{ marginBottom: '1.5rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <input
          type="text"
          placeholder="Search by keyword (title/body)"
          value={keywordFilter}
          onChange={(e) => setKeywordFilter(e.target.value)}
          style={{ width: '200px' }}
        />
        <input
          type="text"
          placeholder="Filter by tag"
          value={tagFilter}
          onChange={(e) => setTagFilter(e.target.value)}
          style={{ width: '150px' }}
        />
        <button type="submit">Search</button>
        <Link href="/notes/new">
          <button type="button" className="primary">New Note</button>
        </Link>
      </form>

      {error && <div className="error-message">{error}</div>}
      {loading && <p>Loading...</p>}
      {!loading && !error && notes.length === 0 && (
        <p>No notes found. Create your first note!</p>
      )}
      {!loading && !error && notes.length > 0 && (
        <ul style={{ listStyle: 'none' }}>
          {notes.map((n) => (
            <li
              key={n.id}
              style={{
                padding: '1rem',
                marginBottom: '0.5rem',
                background: '#fff',
                borderRadius: '8px',
                border: '1px solid #ddd',
              }}
            >
              <Link href={`/notes/${n.id}`} style={{ fontWeight: 600 }}>
                {n.title}
              </Link>
              <p style={{ marginTop: '0.25rem', color: '#666', fontSize: '0.9rem' }}>
                {n.body.slice(0, 120)}
                {n.body.length > 120 ? '...' : ''}
              </p>
              {n.tags.length > 0 && (
                <div style={{ marginTop: '0.5rem' }}>
                  {n.tags.map((t) => (
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
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
