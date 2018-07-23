import logging
import keyboard
from pinkdeck.core import config
from pinkdeck.core import handles, http, server, twitch

LOGO = """
       _      _      _        _
  _ __(_)_ _ | |____| |___ __| |__
 | '_ \\ | ' \\| / / _` / -_) _| / /
 | .__/_|_||_|_\\_\\__,_\\___\\__|_\\_\\
 |_|
"""

def main():
    log = logging.getLogger("pinkdeck.scripts.cli")
    log.setLevel(config.LOG_LEVEL)

    print(LOGO)

    # Read all our handlers and parse out bad values
    hf = handles.get_handle_file()
    handlers = handles.parse_handles(hf)

    # Get our Twitch OAuth value
    server.create_server()

    # Make our Twitch API instance
    t = twitch.TwitchApi(server.oauth)
    t.get_channel_data()

    # Map action names to functions
    FUNC_MAP = {
       "set_channel_title": t.set_channel_title,
       "set_channel_game": t.set_channel_game,
       "set_channel_communities": t.set_channel_communities,
       "start_channel_commercial": t.start_channel_commercial,
       "http_request": http.send_http_request
    }

    handler_funcs = {}

    for keybind in handlers:
        log.info("Adding keybind for {}".format(keybind))
        def custom_handler(k):
            h = handlers[k]
            for task in h:
                name = task.get("action")
                data = task.get("data")
                log.info("Doing task", name)
                try:
                    if data:
                        FUNC_MAP[name](data)
                    else:
                        FUNC_MAP[name]()
                except Exception as e:
                    log.error(e)
        handler_funcs[keybind] = custom_handler
        keyboard.add_hotkey(keybind, lambda k=keybind: custom_handler(k))

    log.info("Starting keyboard loop")

    try:
        keyboard.wait()
    except:
        log.info("Exiting...")
