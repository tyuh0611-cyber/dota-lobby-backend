# AI notes — backend repository

These notes are for future ChatGPT/AI work on this repo.

## Rule: keep notes updated

Whenever you change architecture, deployment, setup, or important behavior, update this file or `docs/project_context.md`.

Whenever you add/remove/move files, update `PROJECT_FILES.txt`.

Do not leave important decisions only in chat history.

## Current split

This repo is backend-only. Streamer-side code belongs in:

```text
tyuh0611-cyber/dota-lobby-streamer-proxy
```

Old monorepo was:

```text
tyuh0611-cyber/dota-twitch-lobby-bot
```

## Backend responsibilities

- web dashboard / Control Center
- player database
- slots and comments
- ranked queue
- settings
- UI autosave
- calls to streamer proxy

## Not backend responsibilities

- Twitch OAuth token storage
- Twitch refresh token storage
- Steam credentials
- Dota Game Coordinator connection
- streamer host secrets

## UI decisions already made

- Main page is Control Center.
- Refresh button removed.
- Quick Invite has explanation for count field.
- Queue row actions are only Invite and Delete.
- Save button removed from queue rows.
- Inline edits autosave on Enter or blur.
- Player detail page rebuilt into profile-style layout.

## Security decisions already made

- CSRF token added to web forms.
- Real `.env` files must not be committed.
- Backend uses streamer proxy API key only.

## Deployment note

Backend `.env` should contain streamer proxy URL and API key. It should not contain streamer Twitch/Steam secrets.
