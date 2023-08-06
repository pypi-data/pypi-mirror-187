# openstreetmap-tags-to-rivescript
**Convert of openstreetmap/id-tagging-schema to RiveScript, the Artificial Intelligence Scripting Language (alternative to AIML)**

## Quickstart
> Explains how to generate the RiveScripts

### Install

No pip release yet, install from GitHub

```bash
pip install https://github.com/fititnt/openstreetmap-tags-to-rivescript/archive/main.zip
```

### Fetch cache

```bash
# Prepare the cache directory
git clone https://github.com/openstreetmap/id-tagging-schema.git ./id-tagging-schema
```

### Generate RiveScript

```bash
osmtags2rive --language=pt > example/brain/osm-tagging_pt.rive
osmtags2rive --language=pt --reverse-index > example/brain/osm-tagging-reverse_pt.rive
```

<!--
To regenerate again example

osmtags2rive --language=pt > example/brain/osm-tagging_pt.rive
osmtags2rive --language=pt --reverse-index > example/brain/osm-tagging-reverse_pt.rive
-->

## Extras

### Quick example on how to use the generated RiveScripts

Check [Rivescript website page for interpreters](https://www.rivescript.com/interpreters) for other programming languages.
They all have a similar interface:
allow you to deposit all files in a directory which is loaded by your interpreter.

#### Python example
Using Rive Python interpreter from https://github.com/aichaos/rivescript-python

```bash
# install the script
pip install rivescript

python shell.py
```

```python
# file shell.py

from rivescript import RiveScript

# bot = RiveScript(utf8=True)
bot = RiveScript()
bot.load_directory("./example/brain")
bot.sort_replies()

while True:
    msg = input('You> ')
    if msg == '/quit':
        quit()

    reply = bot.reply("localuser", msg)
    print ('Bot>', reply)
```


# Disclaimers
<!--
TODO see https://wiki.osmfoundation.org/wiki/Trademark_Policy
-->

OpenStreetMap™ is a trademark of the OpenStreetMap Foundation, and is used with their permission.
This project is not endorsed by or affiliated with the OpenStreetMap Foundation. (via [OSMF Trademark_Policy](https://wiki.osmfoundation.org/wiki/Trademark_Policy))

# License


[![Public Domain](https://i.creativecommons.org/p/zero/1.0/88x31.png)](LICENSE)

Public domain