import json
import requests
from pinkdeck.core import config

class TwitchApiError(Exception):
    pass

class TwitchOauthError(Exception):
    pass

class TwitchApi(object):
    def __init__(self, oauth):
        self.oauth = oauth
        self.sess = requests.Session()
        self.sess.headers.update({
            "Client-ID": config.CLIENT_ID,
            "Authorization": "OAuth {}".format(self.oauth),
            "User-Agent": config.USER_AGENT,
            "Accept": "application/vnd.twitchtv.v5+json",
            "Content-Type": "application/json"
        })

        # Validate our OAuth token
        if not self.validate():
            raise TwitchOauthError("Could not validate with Twitch API")

        # Initialize values
        self._id = None
        self._name = None
        self._is_partner = None
        self._broadcaster_type = None
        self._description = None
        self._mature = None

    @property
    def id(self):
        if self._id == None:
            self.get_channel_data()
        return self._id

    @property
    def is_partner(self):
        if self.is_partner == None:
            self.get_channel_data()
        return self._is_partner

    @property
    def name(self):
        if self._name == None:
            self.get_channel_data()
        return self._name

    @property
    def description(self):
        if self._description == None:
            self.get_channel_data()
        return self._description

    @property
    def mature(self):
        if self._mature == None:
            self.get_channel_data()
        return self._mature

    def get_channel_data(self):
        r = self.sess.get("https://api.twitch.tv/kraken/channel")
        data = r.json()

        self._id = int(data.get("_id"))
        self._name = data.get("name")
        self._is_partner = data.get("partner")
        self._broadcaster_type = data.get("broadcaster_type")
        self._mature = data.get("mature")

    def validate(self):
        r = self.sess.get("https://id.twitch.tv/oauth2/validate")
        if r.status_code == 200:
            return True
        else:
            return False

    def get_community_by_name(self, community):
        r = self.sess.get("https://api.twitch.tv/kraken/communities?name={}".format(community))
        data = r.json()
        if r.status_code is 200 and "_id" in data:
            return data.get("_id")
        else:
            return None

    def set_channel_communities(self, names):
        ids = []
        for name in names:
            r = self.get_community_by_name(name)
            if r:
                ids.append(r)
        data = json.dumps({
            "community_ids": ids
        })
        req = self.sess.put("https://api.twitch.tv/kraken/channels/{}/communities".format(self.id), data=data)
        if req.status_code != 204:
            raise TwitchApiError()

    def set_channel_data(self, game=None, title=None):
        if not game and not title:
            raise TwitchApiError("Either a game name or a status is required.")
        d = {
            "channel": {}
        }
        if game:
            d["channel"]["game"] = game
        if title:
            d["channel"]["status"] = title
        data = json.dumps(d)
        req = self.sess.put("https://api.twitch.tv/kraken/channels/{}".format(self.id), data=data)
        if req.status_code != 200:
            e = req.json().get("message")
            raise TwitchApiError(e)
        else:
            return True

    def set_channel_game(self, game):
        return self.set_channel_data(game=game)

    def set_channel_title(self, title):
        return self.set_channel_data(title=title)

    def start_channel_commercial(self, length=30):
        # Reject invalid commercial lengths
        if length not in [30, 60, 90, 120, 150, 180]:
            raise TwitchApiError("Invalid commercial length!")
        if not self.is_partner:
            raise TwitchApiError("Only Twitch partners can start commercials")
        data = json.dumps({
            "length": length
        })
        req = self.sess.post("https://api.twitch.tv/kraken/channels/{}/commercial".format(self.id), data=data)
        if req.status_code != 200:
            e = req.json().get("message")
            raise TwitchApiError(e)
        else:
            return True
