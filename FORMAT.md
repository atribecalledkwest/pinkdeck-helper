# Handlers

pinkdeck-handlers uses a JSON configuration file in order to figure out what to look for. The main body of it is a JSON `object`, with each key being the keybind to look for, and each value being an array of tasks to do for that keybind.

## Tasks

There are currently 5 tasks Pinkdeck handlers can invoke, although more will be added as time goes on.

`set_channel_title`: Sets the title/status for your Twitch stream
`set_channel_game`: Sets the game you are currently playing for your Twitch stream.
`set_channel_communities`: Changes the communities your Twitch channel is a part of. You can be a part of up to three different communities at a time.
`start_channel_commercial`: *Only works if you are a Twitch partner*. Starts a commercial on your Twitch stream.
`http_request`: Makes an HTTP/HTTPS request to any given URL.

## Task data
Some tasks optionally take/require extra data. You can supply this with the `"data"` key in your task's object.

While the tasks are currently limited, theoretically you can implement almost anything using `http_request`. If there is anything you think would be useful to support built-in, please let me know!
