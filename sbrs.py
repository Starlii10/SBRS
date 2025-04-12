"""
Starlii's Battle Royale Simulator
A Hunger Games Simulator-like game written in Python
based on the original Scratch version
https://github.com/Starlii10/sbrs

Copyright (c) 2025 Starlii10
Insert license here
"""

# I'm not dealing with all of this. SO
# pylint: disable=redefined-outer-name, global-statement

import argparse
import importlib
import os
import random
import sys
import traceback

import colorama
from colorama import Back, Fore, Style

from version import __version__
from load_functions import load_everything
from sbrs_config import SBRSConfig

# Python version check
if sys.version_info[0] < 3:
    raise Exception(  # pylint: disable=broad-exception-raised
        "Python 3 or above is required to run SBRS."
    )

colorama.init(autoreset=True)

DEFAULT_COLORS = {
    f"{color}: white"
    for color in [
        "passive",
        "passive-death",
        "attack-success",
        "attack-fail",
        "passive-attack",
        "generic-player",
        "target-player",
        "new-turn",
        "end-turn",
        "winner",
        "most-kills",
    ]
}


# Basic functions
def basic_init(configpath, nosave):
    """
    Fully loads a configuration file. Should be passed to `SBRSGame` to initialize the game.

    Args:
        configpath (str): The path to the config file.
        nosave (bool): If True, the game will not be saved.

    Returns:
        SBRSConfig: The game configuration.
    """
    config, players, playertypes, teams, messages, sbrs_game_logger = load_everything(
        configpath, nosave
    )

    # Config variables
    message_colors = (
        config["message-colors"] if "message-colors" in config else DEFAULT_COLORS
    )
    classic_behavior = (
        config["classic-behavior"] if "classic-behavior" in config else False
    )
    sudden_death = config["sudden-death"] if "sudden-death" in config else False
    attack_chance = config["attack-chance"]
    passive_death_chance = config["death-chances"]["passive"]
    attack_success_chance = config["death-chances"]["attack"]
    show_kills_only = (
        config["show-kills-only"] if "show-kills-only" in config else False
    )

    return SBRSConfig(
        config=config,
        players=players,
        playertypes=playertypes,
        teams=teams,
        messages=messages,
        sbrs_game_logger=sbrs_game_logger,
        message_colors=message_colors,
        classic_behavior=classic_behavior,
        sudden_death=sudden_death,
        passive_death_chance=passive_death_chance,
        attack_chance=attack_chance,
        attack_success_chance=attack_success_chance,
        death_chances=config["death-chances"],
        show_kills_only=show_kills_only,
        turns=0,
        use_teams=config["use-teams"],
    )


# SBRSGame
class SBRSGame:
    """
    A class representing a game of Starlii's Battle Royale Simulator.

    Attributes:
        addons (list): A list of loaded addons.
        actions (list): A list of actions that can be chosen from.
        config (SBRSConfig): The game configuration.
        remaining_players (list): A list of remaining players in the game.
        turn (int): The current turn number.
        sudden_death (bool): If True, sudden death is enabled.
        something_happened (bool): If True, a game print happened this turn.
    """

    def __init__(self, config):
        """
            NOTE: This function is also responsible for loading addons.
        """
        self.addons: list = []
        """A list of loaded addons."""
        self.actions: list = []
        """A list of actions that can be chosen from."""
        self.config: SBRSConfig = config
        """The game configuration."""
        self.remaining_players: list = config.players
        """A list of remaining players in the game."""
        self.sudden_death: bool = False
        """Whether sudden death is enabled."""
        self.something_happened: bool = False
        """Whether a game print happened this turn."""
        self.turn: int = 0
        """The current turn number."""

        # Load basic_game_behavior
        try:
            self.addons.append(importlib.import_module("basic_game_behavior").Addon())
            self.addons[-1].initgame(self)
        except Exception as e:  # pylint: disable=broad-except
            raise Exception(  # pylint: disable=broad-exception-raised
                f"{Fore.RED}Couldn't load SBRS base game behavior."
            ) from e
        # Load addons
        for _, _, files in os.walk("addons"):
            for filename in files:
                if filename.endswith(".py"):
                    print(f"{Fore.YELLOW}Loading addon: {Fore.CYAN}{filename}")
                    try:
                        addon = importlib.import_module(f"addons.{filename[:-3]}")
                        if not hasattr(addon, "Addon"):
                            raise ValueError(
                                "Addon does not have an Addon class. Was it renamed?"
                            )
                        self.addons.append(addon.Addon())
                        try:
                            self.addons[-1].initgame(self)
                        except Exception as e:  # pylint: disable=broad-except
                            if not hasattr(addon, "initgame"):
                                pass # Ah, okay then
                            print(
                                f"{Fore.RED}Unable to initialize addon {filename}.\n"
                                + "".join(
                                    traceback.format_exception(type(e), e, e.__traceback__)
                                )
                            )
                            self.addons.remove(addon)
                    except Exception as e:  # pylint: disable=broad-except
                        print(
                            f"{Fore.RED}Unable to load addon {filename}.\n"
                            + "".join(
                                traceback.format_exception(type(e), e, e.__traceback__)
                            )
                        )

    def add_action(self, action):
        """
        Adds an SBRSAction to the game.

        Args:
            action (SBRSAction): The action to add.

        Raises:
            ValueError: If the action is None, has no function, or already exists.
        """
        if action is None or action.function is None:
            raise ValueError("SBRSAction must have a function.")
        if action.name in [a.name for a in self.actions]:
            raise ValueError(f"SBRSAction with name {action.name} already exists.")
        self.actions.append(action)

    def remove_action(self, action):
        """
        Removes an SBRSAction from the game.

        Args:
            action (SBRSAction or str): The action to remove.

        Raises:
            ValueError: If the action is not in the game.
        """
        if isinstance(action, str):
            action = next((a for a in self.actions if a.name == action), None)
        if action is None:
            raise ValueError(f"SBRSAction with name {action.name} does not exist.")
        self.actions.remove(action)

    def game_print(self, msg: str):
        """
        Prints a message to the console and the game logger.
        """
        print(msg)
        if self.config.sbrs_game_logger:
            # check for color codes and erase them
            msg = msg.replace(Fore.RED, "")
            msg = msg.replace(Fore.GREEN, "")
            msg = msg.replace(Fore.BLUE, "")
            msg = msg.replace(Fore.WHITE, "")
            msg = msg.replace(Fore.YELLOW, "")
            msg = msg.replace(Back.RED, "")
            msg = msg.replace(Back.GREEN, "")
            msg = msg.replace(Back.BLUE, "")
            msg = msg.replace(Back.WHITE, "")
            msg = msg.replace(Style.RESET_ALL, "")
            msg = msg.replace("\x1b[36m", "")
            self.config.sbrs_game_logger.info(msg)
        self.something_happened = True

    def message_color(self, color: str):
        """
        Gets the color code for a message color using the loaded config.
        """
        color = self.config.message_colors[color]
        color_code = getattr(Fore, color.upper())
        return color_code

    def random_message(self, message_type: str, player_type: str):
        """
        Returns a random message from the loaded messagesfor the
        specified message type and player type.

        Args:
            message_type (str): The type of message to get.
            player_type (str): The type of player to get the message for.

        Returns:
            str: The random message.
        """
        if player_type == "Default":
            return random.choice(self.config.messages[message_type]["Default"])
        try:
            return random.choice(
                self.config.messages[message_type][player_type]
                + self.config.messages[message_type]["Default"]
            )
        except KeyError:
            # Player type isn't in messages
            return random.choice(self.config.messages[message_type]["Default"])

    def game_over(self):
        """
        Prints the game over messages (`winner` and `most-kills`).
        Also runs game_over on addons.
        """
        for addon in self.addons:
            if hasattr(addon, "game_over"):
                addon.game_over(self)
        self.game_print(
            self.random_message("winner", self.remaining_players[0].type)
            .replace(
                "{player}",
                f"{self.message_color('generic-player')}{self.remaining_players[0].name}{self.message_color('winner')}",
            )
            .replace(
                "{amount}",
                f"{self.message_color('generic-player')}{str(self.remaining_players[0].kills)}{self.message_color('winner')}",
            )
        )
        most_kills = 0
        most_kills_players = []
        for player in self.config.players:
            if player.kills > most_kills:
                most_kills = player.kills
                most_kills_players = [player]
            elif player.kills == most_kills:
                most_kills_players.append(player)
        players_str = ""
        if len(most_kills_players) == 1:
            players_str = f"{self.message_color('generic-player')}{most_kills_players[0].name}{self.message_color('most-kills')}"
        elif len(most_kills_players) == 2:
            players_str = f"{self.message_color('generic-player')}{most_kills_players[0].name} {self.message_color('most-kills')}and {self.message_color('generic-player')}{most_kills_players[1].name}{self.message_color('most-kills')}"
        else:
            for player in most_kills_players[:-1]:
                players_str += f"{self.message_color('generic-player')}{player.name}{self.message_color('most-kills')}, "
            players_str += f"{self.message_color('most-kills')}and {self.message_color('generic-player')}{most_kills_players[-1].name}{self.message_color('most-kills')}"
        self.game_print(
            f"{self.message_color('most-kills')}{self.random_message('most-kills', random.choice(most_kills_players).type)
            .replace('{player}', players_str)
            .replace(
                '{amount}',
                f"{self.message_color('generic-player')}{str(most_kills)}{self.message_color('most-kills')}"
            )}"
        )

    def simulate_turn(self):
        """
        Simulates a single turn in the game.
        """
        self.something_happened = False
        try:
            self.game_print(
                f"{self.message_color('new-turn')}Turn {self.turn} - {len(self.remaining_players)} players remaining\n"
            )
            for addon in self.addons:
                if hasattr(addon, "begin_turn"):
                    addon.begin_turn(self)
            for player in self.config.players:
                if len(self.remaining_players) == 1:
                    break
                if player.alive:
                    # Random action
                    action = random.choice(self.actions)
                    action.function(self, player)
                    # Remove dead players and check for game over
                    self.remaining_players = [
                        p for p in self.remaining_players if p.alive
                    ]
                    if len(self.remaining_players) == 1:
                        self.game_over()
            if not self.something_happened:
                if self.config.show_kills_only:
                    self.game_print(
                        f"{self.message_color('passive')}No one died on this turn.\n"
                    )
                else:
                    self.game_print(
                        f"{self.message_color('passive')}Nothing happened this turn.\n"
                    )
            self.game_print(
                f"------ {self.message_color('end-turn')}TURN ENDED {Fore.WHITE}------\n"
            )
        except KeyboardInterrupt:
            self.game_print(f"\n{self.message_color('end-turn')}Game stopped by user.")
            print("Exiting...\n")
            sys.exit(0)

    # Main loop
    def run_game(self):
        """
        The main game loop.
        Runs `simulate_turn()` until there is only one player left, then exits.
        """

        if len(self.remaining_players) == 1:
            print("Game already finished.")

        while len(self.remaining_players) > 1:
            self.turn += 1
            self.simulate_turn()
            if __name__ == "__main__":
                try:
                    if not args.auto:
                        input(
                            "Press enter to simulate next turn"
                            if len(self.remaining_players) > 1
                            else "Press enter to exit"
                        )
                except KeyboardInterrupt:
                    self.game_print(
                        f"\n{self.message_color('end-turn')}Game stopped by user."
                    )
                    print("Exiting...\n")
                    sys.exit(0)
                except EOFError:
                    pass
            if not len(self.remaining_players) > 1:
                break
            print("------\n")


# Addons
class SBRSAddon:
    """
    Base class for addons
    """

    # pylint: disable=unnecessary-pass

    def __init__(self):
        """
        Early initialization. Called immediately after the addon is loaded,
        before an `SBRSGame` is initialized.

        Can be used to print information about the addon (version, author, etc.)

        Note that not all addons are expected to be loaded at this point.
        Accessing additional addons should be done in `initgame()`.
        """
        pass

    def initgame(self, game: SBRSGame):
        """
        Called when an `SBRSGame` is initialized.
        Can be used to add things to the game, or change configuration.

        Note that all addons are loaded at this point. This means that
        if you need to access additional addons, you should do it here.

        Args:
            game (sbrs.SBRSGame): The game being initialized
        """
        pass

    def start_turn(self, game: SBRSGame):
        """
        Called before a turn is simulated.
        Note that you should not add actions here. Use `add_action()` in
        `initgame()` instead.

        Args:
            game (sbrs.SBRSGame): The game being simulated
        """
        pass

    def end_turn(self, game: SBRSGame):
        """
        Called when a turn ends.

        Args:
            game (sbrs.SBRSGame): The game being simulated
        """
        pass

    def end_game(self, game: SBRSGame):
        """
        Called when the game ends.

        Args:
            game (sbrs.SBRSGame): The game being simulated
        """
        pass


# Main
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to the config file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "-a", "--auto", action="store_true", help="Automatically simulate a game"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Disable saving the game to a log file"
    )
    args = parser.parse_args()

    # Startup prints
    print(
        f"""{Fore.BLUE}Starlii's Battle Royale Simulator {__version__}
A Hunger Games Simulator-like game written in Python
based on the original Scratch version
https://github.com/Starlii10/sbrs

Copyright (c) 2025 Starlii10
Insert license here\n"""
    )

    # Load config and game
    # Should there be an interactive prompt?
    game_config = basic_init(args.config, args.no_save)
    game = SBRSGame(game_config)
    if not args.auto:
        input("Initialization finished. Press enter to begin, or ctrl-c to exit.")
    print("------\n")
    game.run_game()
