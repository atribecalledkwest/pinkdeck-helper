# Pinkdeck Helper #
This script is a helper script I wrote for my Pinkdeck OBS controlling keyboard. It lets you change your game, stream title, and communities all in the press of a button!

## Setup ##
1. Create a file called `.pinkdeck.handles` in the root of your user directory (`C:\User\YourUser\.pinkdeck.handles` on windows, `~/.pinkdeck.handles` on OS X and Linux) based on the `example.pinkdeck.handles` file.
2. run `pip install -r requirements.txt`.
3. Run the `pinkdeck-helper.py` script.
4. Authorize the _Pinkdeck Helper_ application for your Twitch account (We only the `channel_read` and `channel_editor` permissions to set your stream data and get your channel's ID).
5. You should be done!

## I found an error! I want this feature! Help! ##
Submit an issue! I'm only really testing this on Windows because that's where I'm using it, but it should theoretically work on every platform. If it doesn't, tell me!!!
