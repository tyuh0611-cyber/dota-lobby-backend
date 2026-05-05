# Current status — backend

Last updated: 2026-05-05

## Repository split status

The original monorepo has been split into separate repositories:

```text
Old monorepo:
tyuh0611-cyber/dota-twitch-lobby-bot

Backend repo:
tyuh0611-cyber/dota-lobby-backend

Streamer proxy repo:
tyuh0611-cyber/dota-lobby-streamer-proxy
```

Backend code should live only in this repository.

Streamer-side code, Twitch OAuth, Twitch tokens, Steam/Dota credentials, and Dota GC integration belong in:

```text
tyuh0611-cyber/dota-lobby-streamer-proxy
```

## What backend is for

Backend is the operator/admin side of the project.

It owns:

- FastAPI web Control Center
- player database
- slot accounting
- comments
- queue ranking logic
- web UI/static/templates
- settings stored in DB
- calls to streamer proxy through HTTP API

It must not own:

- Twitch access token
- Twitch refresh token
- Twitch Client Secret for streamer runtime, except if only used for docs/examples
- Steam password
- Steam shared secret
- real Dota Game Coordinator session

## Current backend UI state

The Control Center UI has been heavily cleaned up.

Important decisions:

- Main page `/` is the operational Control Center.
- Removed Refresh button from header.
- Quick Invite count has explanatory text.
- Add player / slots uses simple inputs, no +/- steppers.
- Priority queue row actions are minimal:
  - Invite
  - Delete from DB
- Save button was removed from queue rows.
- Inline edit autosaves on Enter or blur/click outside.
- Player detail page was rebuilt into a profile-style layout.
- CSRF protection was added for dangerous POST actions.

## Current backend migration status

Systemd was moved from the old path:

```text
/opt/dota-twitch-lobby-bot/bot_backend
```

to the new path:

```text
/opt/dota-lobby-backend
```

Always verify that `/opt/dota-lobby-backend/app/web_main.py` exists before trusting systemd `active` output.

## Backend Twitch integration status

Backend Control Center now talks to streamer proxy for Twitch status and setup.

Implemented backend routes:

```text
/twitch/connect
/twitch/status
/twitch/setup
```

Implemented streamer proxy client helpers:

```text
health()
get_twitch_auth_url()
get_twitch_me()
setup_twitch()
get_chatters()
get_lobby()
invite()
```

Dashboard Twitch panel now includes:

- `Connect / reconnect Twitch`
- `Setup IDs`
- `Status JSON`

Verified current state:

```text
Backend Control Center -> Twitch panel -> Status JSON is OK.
```

A direct unauthenticated curl to `/twitch/status` returns `303 -> /login`, which is expected because this route is protected by web login.

## Backend systemd target configuration

The desired service paths are:

```ini
WorkingDirectory=/opt/dota-lobby-backend
EnvironmentFile=/opt/dota-lobby-backend/.env
ExecStart=/opt/dota-lobby-backend/.venv/bin/uvicorn app.web_main:app --host ${WEB_HOST} --port ${WEB_PORT}
```

## Backend `.env` rule

Real `.env` stays local on the server and must not be committed.

Backend `.env` should contain backend runtime settings, database settings, and streamer proxy URL/API key.

It should not contain real Twitch access/refresh tokens or Steam credentials.

Required streamer proxy settings:

```env
STREAMER_PROXY_URL=http://<streamer-proxy-host>:8081
STREAMER_PROXY_API_KEY=<same PROXY_API_KEY from streamer proxy .env>
```

## First backend checks after any migration or deploy

Run on backend server:

```bash
cd /opt/dota-lobby-backend
find . -maxdepth 3 -type f | sort | head -80
```

Must include at minimum:

```text
./app/web_main.py
./app/web.py
./app/config.py
./app/streamer_proxy_routes.py
```

Then check Git:

```bash
git status
git log --oneline -5
```

Then check service:

```bash
systemctl cat dota-lobby-web
systemctl restart dota-lobby-web
sleep 2
systemctl status dota-lobby-web --no-pager
journalctl -u dota-lobby-web -n 80 --no-pager
```

Important: `systemctl status` immediately after restart can show active for a few milliseconds even if uvicorn crashes right after. Always check logs after a short sleep.

## First thing to check for Twitch issues from backend

1. On streamer server, check streamer proxy directly:

```bash
KEY=$(grep '^PROXY_API_KEY=' /opt/dota-lobby-streamer-proxy/.env | cut -d= -f2-)
curl -i -H "X-Api-Key: $KEY" http://127.0.0.1:8081/twitch/me
curl -i -X POST -H "X-Api-Key: $KEY" http://127.0.0.1:8081/twitch/setup
curl -i -H "X-Api-Key: $KEY" http://127.0.0.1:8081/chatters
```

2. Only after streamer proxy works, check backend `.env`:

```bash
grep -E 'STREAMER_PROXY_URL|STREAMER_PROXY_API_KEY' /opt/dota-lobby-backend/.env
```

3. Then restart backend:

```bash
systemctl restart dota-lobby-web
journalctl -u dota-lobby-web -n 80 --no-pager
```

4. Check in browser after login:

```text
Control Center -> Twitch panel -> Status JSON
Control Center -> Twitch panel -> Setup IDs
```

## Rules for future AI work

Always update these files when changing the project:

```text
docs/CURRENT_STATUS.md
docs/AI_NOTES.md
docs/project_context.md
PROJECT_FILES.txt
```

Do not rely only on chat history.

Before changing code, check:

1. Which repo is responsible: backend or streamer proxy?
2. Current `git status`.
3. Relevant service logs.
4. Whether `.env` values are local-only and not committed.
5. Whether `PROJECT_FILES.txt` must be regenerated.

When adding/removing/moving files, regenerate:

```bash
find . -type f \
  -not -path './.git/*' \
  -not -path './.venv/*' \
  -not -path './venv/*' \
  -not -path './__pycache__/*' \
  -not -name '.env' \
  -not -name '*.pyc' \
  | sort > PROJECT_FILES.txt
```
