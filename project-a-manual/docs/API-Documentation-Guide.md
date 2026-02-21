# API Documentation Guide

This guide explains how the "project-a-manual" API documentation works and how to use it.

## Quick Reference

| Endpoint | Auth | Description |

| `GET /` | No | Root with links to docs |
| `GET /health` | No | Health check |
| `POST /notes` | Yes | Create a note |
| `GET /notes` | Yes | List notes (optional `tag`, `keyword` filters) |
| `GET /notes/{id}` | Yes | Get one note |
| `PUT /notes/{id}` | Yes | Update a note |
| `DELETE /notes/{id}` | Yes | Delete a note |

For full endpoint details, You can see Swagger UI: http://localhost:8000/docs
