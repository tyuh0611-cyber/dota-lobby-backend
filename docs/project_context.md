# Project context — backend

## Main strategy

Build a web Control Center for managing Dota 2 custom-lobby access through a Twitch-aware priority queue.

Backend is the operator/admin side. It should be comfortable to use during a stream and should not expose streamer secrets.

## Architecture

```text
Backend server:
- PostgreSQL
- FastAPI web dashboard
- settings and player database
- queue ranking logic
- calls streamer_proxy over HTTP with X-Api-Key

Streamer server:
- streamer_proxy
- Twitch OAuth and chatters
- Steam/Dota secrets
- future real Dota Game Coordinator adapter
```

## Security boundary

Backend must not store:

- Twitch access token
- Twitch refresh token
- Steam username/password
- Steam shared secret
- Dota credentials

Backend only stores:

- PostgreSQL app data
- streamer proxy URL
- streamer proxy API key

## Web dashboard direction

The main page `/` should be a Control Center.

Important blocks:

- Settings
- Twitch status
- Lobby status
- Add player / slots
- Priority queue table

Queue row actions should stay minimal:

- Invite
- Delete from DB

Inline edits should autosave on Enter or blur.

## Queue strategy

Queue is ranked using bot settings:

- `oldest_played`
- `most_slots`
- `recent_slot`
- `recent_played`
- `most_active`

Special Twitch names like `EZ25` can be prioritized if eligible.

`require_twitch_online=true` means the player must be present in Twitch chatters.

## Current important tasks

1. Keep backend and streamer proxy as separate repositories.
2. Make streamer setup simple: streamer gives required values during setup, not by editing many files manually.
3. Finish Twitch OAuth flow on streamer proxy.
4. Add better installer/setup scripts.
5. Later replace mock Dota adapter with real Steam/Dota GC adapter.
