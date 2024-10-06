This repo is now at https://github.com/joshbressers/meshbbs
I created a new repo to remove the fork


# meshbbs

This is a BBS project to run on a meshtastic node. The project was forked from https://github.com/TheCommsChannel/TC2-BBS-mesh and has been heavily modified. They deserve credit for the initial idea and code.

![image](examples/meshbbs-screenshot.jpeg)

This project is VERY VERY early, so be nice and patient. The code isn't amazing, the model to get and send message was designed to be easy for anyone to write plugins, not to be "correct". You'll understand when you look at the code :)

## Getting started

Make sure you have poetry installed
https://python-poetry.org/

You will need to copy the file `examples/example_config.ini` to config.ini. You should be able to figure this file out if you look in it. You can talk to a meshtastic node via serial or TCP/IP. There is also a debug interface that you can run to type commands to the BBS locally to test things out. I would like to see this also run on a raspberry pi with a LoRa hat someday.

You should be able to run `poetry install` to install all the dependencies, then run `poetry run meshbbs` and the BBS will start to run.

Just send the message "hello" to the BBS and it will get you going.

You may want to change your mesh node long name to "hello to start BBS" or something similar.

Here's what getting started should look like

```shell
➜  /tmp git clone https://github.com/joshbressers/meshbbs.git
Cloning into 'meshbbs'...
remote: Enumerating objects: 497, done.
remote: Counting objects: 100% (350/350), done.
remote: Compressing objects: 100% (183/183), done.
remote: Total 497 (delta 242), reused 250 (delta 166), pack-reused 147 (from 1)
Receiving objects: 100% (497/497), 233.16 KiB | 1.62 MiB/s, done.
Resolving deltas: 100% (284/284), done.
➜  /tmp cd meshbbs 
➜  meshbbs git:(main) poetry install
Creating virtualenv meshbbs in /tmp/meshbbs/.venv
Updating dependencies
Resolving dependencies... (1.2s)

Package operations: 22 installs, 0 updates, 0 removals

  • Installing certifi (2024.8.30)
  • Installing charset-normalizer (3.3.2)
  • Installing dbus-fast (2.24.2)
  • Installing idna (3.10)
  • Installing ptyprocess (0.7.0)
  • Installing urllib3 (2.2.3)
  • Installing bleak (0.21.1)
  • Installing dotmap (1.3.30)
  • Installing packaging (24.1)
  • Installing pexpect (4.9.0)
  • Installing print-color (0.4.6)
  • Installing protobuf (5.28.2)
  • Installing pyparsing (3.1.4)
  • Installing pypubsub (4.0.3)
  • Installing pyqrcode (1.2.1)
  • Installing pyserial (3.5)
  • Installing pyyaml (6.0.2)
  • Installing requests (2.32.3)
  • Installing tabulate (0.9.0)
  • Installing webencodings (0.5.1)
  • Installing meshtastic (2.5.1)
  • Installing peewee (3.17.6)

Writing lock file

Installing the current project: meshbbs (0.0.1)
➜  meshbbs git:(main) ✗ cp examples/example_config.ini config.ini
➜  meshbbs git:(main) ✗ poetry run meshbbs
Enter Text: 2024-10-04 19:55:02 - INFO - meshbbs is running on debug interface...
hello
2024-10-04 19:55:05 - INFO - Received message from user 'short_from' to short_to: hello
Enter Text: 
---START MESSAGE---
Welcome to Meshtastic BBS
[A] About
[H] Help
[E] Echo
[W] Wall
[B] Boards
----END MESSAGE----

2024-10-04 19:55:05 - INFO - REPLY SEND ID=456

---START MESSAGE---
Welcome to Meshtastic BBS
[A] About
[H] Help
[E] Echo
[W] Wall
[B] Boards
----END MESSAGE----

```

The first time you type hello it does print the menu twice. It's harder to fix than it looks :)
It only happens once

# Contributing

Patches are welcome! Issues are also just fine if you're not looking to send a PR.

The biggest part of the rewrite was to make adding functionality easy. You should look in the "stages" directory to see how modules can be added to the system. Even though it's event driven, the BBS is designed to run synchronous code (this is easier to write and read).

The `main()` function exists in the server.py file. You can start there if you want to see how the sausage is made. Otherwise I would suggesting looking at the `wall.py` and `main.py` in the stages directory.

## License

GNU General Public License v3.0
