# playerctl-currently-playing

This script calls playerctl to get information about currently playing media and displays it.  It requires [uv](https://docs.astral.sh/uv/) and [playerctl](https://github.com/altdesktop/playerctl).  (playerctl is probably available in your package manager)

```
usage: playerctl-currently-playing [-h] [--album] [--remaining]

Display information about the currently playing media

options:
  -h, --help   show this help message and exit
  --album      Show current album name (if available)
  --remaining  Show time remaining for current track
```

Example:

```bash
playerctl-currently-playing --album --remaining
```

```
Cherub Rock | The Smashing Pumpkins - Siamese Dream | 1993 | 04:42
```
