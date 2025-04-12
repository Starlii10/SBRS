# Starlii's Battle Royale Simulator

The Python remake of the Hunger Games Simulator-like engine made by a silly goober. Also incredibly customizable.
This has absolutely nothing to do with battle royale video games. No idea where you got that idea from.

> [!WARNING]
> This is a very early version of SBRS.

## Getting Started

You'll need to specify a configuration file to begin (see documentation for info). Start SBRS by typing `python sbrs.py <config file>` in a terminal. There are also other arguments possible; use `-h` for a list of them all.

By default, SBRS will use the messages contained in `messages.json`. This can be overridden or extended with configuration settings; see the documentation for configuration options.

> [!NOTE]
> SBRS is very picky about the configuration and message files. It may help to look over the existing files as a reference.

## Addons

SBRS supports addons! Drop them into the `addons` folder next to sbrs.py and they'll apply to your games.

To make an addon, check out the `SBRSAddon` class and `basic_game_behavior.py`. They give a good idea of what an addon does.
