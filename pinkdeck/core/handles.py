import json
import logging
import os
from pinkdeck.core import config

VALID_METHODS = [
    "set_channel_title",
    "set_channel_game",
    "set_channel_communities",
    "start_channel_commercial",
    "http_request"
]

log = logging.getLogger("pinkdeck.core.handles")
log.setLevel(config.LOG_LEVEL)

def get_handle_file():
    default_data = {}
    # Windows
    if os.name == "nt":
        p = os.path.join(os.getenv("APPDATA"), ".pinkdeck.handlers")
    # Everyone else
    else:
        p = os.path.join(os.path.expanduser("~"), ".pinkdeck.handlers")

    if not os.path.isfile(p):
        with open(p, "w", encoding="utf-8") as hf:
            hf.write(json.dumps(default_data))

    return open(p, "r", encoding="utf-8")

def parse_handles(fp):
    with fp:
        data = json.load(fp)
    ret = {}
    for key, value in data.items():
        parsed_items = []
        for item in value:
            if item.get("action") in VALID_METHODS:
                parsed_items.append(item)
            else:
                log.error("Item in {} has invalid action: {}".format(key, item.get("action")))
        ret[key] = parsed_items
    return ret
