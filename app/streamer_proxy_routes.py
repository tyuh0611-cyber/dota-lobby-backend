from fastapi import Depends, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse

from .csrf import csrf_guard
from .twitch_proxy_client import streamer_proxy
from .web import app, require_auth, with_notice


@app.get('/twitch/status')
async def twitch_status_api(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect

    result: dict = {'ok': True}
    try:
        result['health'] = await streamer_proxy.health()
    except Exception as exc:
        result['health_error'] = str(exc)

    try:
        result['me'] = await streamer_proxy.get_twitch_me()
    except Exception as exc:
        result['me_error'] = str(exc)

    try:
        chatters = await streamer_proxy.get_chatters()
        result['chatters_count'] = len(chatters)
    except Exception as exc:
        result['chatters_error'] = str(exc)

    return JSONResponse(result)


@app.post('/twitch/setup', dependencies=[Depends(csrf_guard)])
async def twitch_setup_from_backend(return_to: str = Form('/')):
    try:
        result = await streamer_proxy.setup_twitch()
    except Exception as exc:
        return RedirectResponse(with_notice(return_to, f'Twitch setup failed: {exc}', 'error'), status_code=303)

    display_name = result.get('display_name') or result.get('login') or result.get('broadcaster_id') or 'Twitch user'
    return RedirectResponse(with_notice(return_to, f'Twitch setup saved for {display_name}'), status_code=303)


@app.get('/dota/status-json')
async def dota_status_api(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect

    result: dict = {'ok': True}
    try:
        result['health'] = await streamer_proxy.health()
    except Exception as exc:
        result['health_error'] = str(exc)

    try:
        result['dota'] = await streamer_proxy.get_dota_status()
    except Exception as exc:
        result['dota_error'] = str(exc)

    try:
        result['lobby'] = await streamer_proxy.get_lobby()
    except Exception as exc:
        result['lobby_error'] = str(exc)

    return JSONResponse(result)
