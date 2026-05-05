# Dota Lobby Backend

Backend/control-center part of the Dota Twitch Lobby project.

## Purpose

This service runs the web Control Center and owns the application database.

It manages:

- web dashboard / Control Center
- players and slots
- ranked priority queue
- inline player editing
- settings in PostgreSQL
- calls to streamer proxy through a limited HTTP API

## Runtime role

```text
operator/browser -> backend web dashboard -> streamer proxy -> Twitch / Steam / Dota
```

The backend must not store Twitch tokens, Steam credentials, Dota secrets, or streamer private credentials.

The only shared secret between backend and streamer proxy is the API key:

```env
STREAMER_PROXY_API_KEY=...
```

It must match streamer proxy:

```env
PROXY_API_KEY=...
```

## Current direction

Main interface is the web Control Center, not Telegram.

The Control Center contains:

- Settings
- Twitch status
- Lobby status
- Add player / slots
- Priority queue table
- Invite/Delete actions
- autosave inline edits

## Important security rules

Never commit real `.env` files.
Never commit Twitch access/refresh tokens.
Never commit Steam credentials.
Never commit database passwords.

Use `.env.example` only.

## Notes for ChatGPT / future AI work

Keep project notes updated in:

```text
docs/AI_NOTES.md
docs/project_context.md
PROJECT_FILES.txt
```

Whenever structure changes, update `PROJECT_FILES.txt`.
Whenever strategy/architecture changes, update `docs/project_context.md`.
Whenever implementation decisions are made, update `docs/AI_NOTES.md`.
