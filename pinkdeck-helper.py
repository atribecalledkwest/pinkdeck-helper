# coding=utf8

import json
import logging
import os
import sys
import webbrowser
import requests, keyboard
from flask import Flask, request, Response, g

CLIENT_ID = "teyrrbalgekx3x0apkp8ncauiz2h80"
# requires channel_read and channel_editor
global OAUTH

# Turn off Flask logging 
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

def server_start():
	twitch_authorize_url = "https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id={}&redirect_uri=http://localhost:2111&scope=channel_read+channel_editor".format(CLIENT_ID)

	print "Starting server"

	app = Flask(__name__)

	def after_this_request(func):
	    if not hasattr(g, 'call_after_request'):
	        g.call_after_request = []
	    g.call_after_request.append(func)
	    return func

	@app.after_request
	def per_request_callbacks(response):
	    for func in getattr(g, 'call_after_request', ()):
	        response = func(response)
	    return response

	def shutdown_server():
		func = request.environ.get("werkzeug.server.shutdown")
		if func is None:
			return None
		func()

	@app.route("/")
	def flask_index():
		return """
		<script>
			var h = window.location.hash;
			if(h) {
				h = h.substring(1, h.length);
				window.location = "/authorize?" + h;
			} else {
				document.write("Something went wrong, sorry!");
			}
		</script>
		"""

	@app.route("/authorize")
	def flask_authorize():
		print "Got twitch auth key!"
		global OAUTH
		items = map(lambda x: x.split("="), request.query_string.split("&"))
		for key, value in items:
			if key == "access_token":
				OAUTH = value
				cachelocation = os.path.expanduser(os.path.join("~", ".pinkdeck.cache"))
				with open(cachelocation, "w") as cachefile:
					cachefile.write(OAUTH)
		@after_this_request
		def r(*args, **kwargs):
			shutdown_server()
			return Response("""<script>window.open('', '_self').close()</script>""")
		return """<script>window.open('', '_self').close()</script>"""

	webbrowser.open_new(twitch_authorize_url)

	app.run(port=2111)
	print "Server ending"

handlelocation = os.path.expanduser(os.path.join("~", ".pinkdeck.handles"))
if os.path.isfile(handlelocation):
	with open(handlelocation, "r") as handlefile:
		try:
			custom_handles = json.loads(handlefile.read())
		except:
			print "ERROR: Couldn't load handles in ~/.pinkdeck.handles, exiting"
			sys.exit(2)

cachelocation = os.path.expanduser(os.path.join("~", ".pinkdeck.cache"))
if os.path.isfile(cachelocation):
	with open(cachelocation, "r") as cachefile:
		OAUTH = cachefile.read().strip()
else:
	server_start()
print "Starting twitch stuff"

sess = requests.Session()
sess.headers.update({
	"Client-ID": CLIENT_ID,
	"Accept": "application/vnd.twitchtv.v5+json",
	"Authorization": "OAuth " + OAUTH,
	"Content-Type": "application/json"
})

def twitch_get_id():
	req = sess.get("https://api.twitch.tv/kraken/channel")
	data = req.json()
	# This is not the best place to start auth checking but it's the first place we can
	if req.status_code != 200:
		cachelocation = os.path.expanduser(os.path.join("~", ".pinkdeck.cache"))
		os.remove(cachelocation)
		print "ERROR: Cached OAuth value was incorrect or out of date, please restart program to reauth."
		sys.exit(1)
	return int(data["_id"])

def twitch_get_community_ids(communities):
	ids = []
	for community in communities:
		req = sess.get("https://api.twitch.tv/kraken/communities?name={n}".format(n=community))
		j = req.json()
		if req.status_code == 200 and "_id" in j:
			ids.append(j["_id"])
	return ids

def twitch_set_channel_communities(ids):
	global _id
	ids = json.dumps({
		"community_ids": ids
	})
	return sess.put("https://api.twitch.tv/kraken/channels/{id}/communities".format(id=_id), data=ids)

def twitch_set_channel_data(game, title):
	global _id
	data = {
		"channel": {
			"game": game
		}
	}
	if title:
		data["channel"]["status"] = title
	return sess.put("https://api.twitch.tv/kraken/channels/{id}".format(id=_id), data=json.dumps(data))

def twitch_handle(game, title=None, communities=["varietystreaming"]):
	print "Setting Twitch channel data"
	twitch_set_channel_data(game, title)

	print "Getting Twitch channel communities for {c}".format(c=", ".join(communities))
	ids = twitch_get_community_ids(communities)
	
	print "Got {i} ids, setting now".format(i=len(ids))
	fin = twitch_set_channel_communities(ids)

	print("Done")

print "Setting up custom handlers"
for keybind in custom_handles:
	print "Adding hotkey for {h}".format(h=keybind)
	keyboard.add_hotkey(keybind, lambda: twitch_handle(*custom_handles[keybind]))

print "Getting Twich user ID"
_id = twitch_get_id()

print "Starting Keyboard loop"
keyboard.wait()
