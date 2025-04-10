"""
Load functions for SBRS.
"""

# pylint: disable=broad-exception-caught, broad-exception-raised

import json
import logging
import os
import sys
import time
import traceback

from colorama import Fore, Style

from version import __version__
from player import SBRSPlayer
from team import SBRSTeam

def load_config(configpath: str) -> tuple:
    """
    Loads the config file.

    Args:
        configpath (str): The path to the config file.

    Returns:
        tuple: A tuple containing:
            config (dict): The loaded config file.
            players (list): A list of players.
            playertypes (list): A list of player types.
            teams (list | None): A list of teams. None if teams mode is disabled.
    """
    try:
        with open(configpath, encoding="utf-8") as f:
            config = json.load(f)
            # Check if teams mode is enabled
            if "use-teams" not in config:
                print(
                    f"{Fore.YELLOW}Teams mode not specified in config file. Defaulting to FFA."
                )
                use_teams = False
            else:
                use_teams = config["use-teams"]
            # TODO: Implement teams fix
            # For now disable teams mode
            if use_teams:
                raise NotImplementedError(
                    "Teams mode is not working yet. Please disable teams mode in the config file."
                )
            # Load players, playertypes, and teams
            if "files" in config:
                try:
                    # players
                    if "players" in config["files"]:
                        if os.path.exists(config["files"]["players"]):
                            with open(
                                config["files"]["players"], encoding="utf-8"
                            ) as f:
                                cfg_players = f.readlines()
                                cfg_players = [
                                    player.strip()
                                    for player in cfg_players
                                    if player.strip() != ""
                                ]
                        else:
                            raise FileNotFoundError(
                                f"Players file ({config['files']['players']}) does not exist."
                            )
                    # playertypes
                    if "playertypes" in config["files"]:
                        if os.path.exists(config["files"]["playertypes"]):
                            with open(
                                config["files"]["playertypes"], encoding="utf-8"
                            ) as f:
                                cfg_playertypes = f.readlines()
                                cfg_playertypes = [
                                    playertype.strip()
                                    for playertype in cfg_playertypes
                                    if playertype.strip() != ""
                                ]
                                # replace empty playertypes with default
                                cfg_playertypes = [
                                    "Default" if playertype == "" else playertype
                                    for playertype in cfg_playertypes
                                ]
                        else:
                            print(
                                f"{Fore.YELLOW}Playertypes file ({config['files']['playertypes']}) does not exist. Defaulting to Default for all players."
                            )
                            cfg_playertypes = ["Default"] * len(cfg_players)
                    else:
                        print(
                            f"{Fore.YELLOW}Playertypes not specified in config file. Defaulting to Default for all players."
                        )
                        cfg_playertypes = ["Default"] * len(cfg_players)

                    # teams
                    if "teams" in config["files"] and use_teams:
                        if os.path.exists(config["files"]["teams"]):
                            with open(config["files"]["teams"], encoding="utf-8") as f:
                                cfg_teams = f.readlines()
                                cfg_teams = [
                                    team.strip()
                                    for team in cfg_teams
                                    if team.strip() != ""
                                ]
                        else:
                            raise FileNotFoundError(
                                f"Teams file ({config['files']['teams']}) does not exist."
                            )
                    else:
                        cfg_teams = None
                except Exception as e:
                    raise Exception(
                        f"Unable to parse files: {e.__class__.__name__}: {e}"
                    ) from e
            else:
                try:
                    cfg_players = config["players"]
                    try:
                        cfg_playertypes = config["playertypes"]
                    except KeyError:
                        print(
                            f"{Fore.YELLOW}Playertypes not specified in config file. Defaulting to Default."
                        )
                        cfg_playertypes = ["Default"] * len(cfg_players)
                    if use_teams:
                        cfg_teams = config["teams"]
                except Exception as e:
                    raise Exception(
                        f"Unable to get players, playertypes, and teams from config: {e.__class__.__name__}: {e}"
                    ) from e
            # Load message colors
            if "message-colors" in config:
                message_colors = config["message-colors"]
                # See if any colors are missing
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
                ]:
                    if color not in message_colors:
                        message_colors[color] = "white"
                # Check if any colors are invalid
                for color in message_colors:
                    if message_colors[color] not in [
                        "black",
                        "red",
                        "green",
                        "yellow",
                        "blue",
                        "magenta",
                        "cyan",
                        "white",
                    ]:
                        raise ValueError(
                            f'Invalid color "{message_colors[color]}" for message color "{color}". \
                            Supported colors: black, red, green, yellow, blue, magenta, cyan, white'
                        )
            else:
                message_colors = {}
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
                ]:
                    message_colors[color] = "white"
            messages = {}
            # Load extra message files
            if "extra-message-files" in config:
                for messagefile in config["extra-message-files"]:
                    messages = {**messages, **load_messages(messagefile)}
            # Load default messages
            if (
                "load-default-messages" in config
                and not config["load-default-messages"] is False
            ):
                load_messages("messages.json")
            elif not "load-default-messages" in config:
                messages = {**messages, **load_messages("messages.json")}
            # Additional settings go here...
            print(
                f'{Fore.GREEN}Loaded config file "{configpath}" successfully.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(
            f"{Fore.RED}Unable to load configuration.\n{"".join(traceback.format_exception(type(e), e, e.__traceback__))}"
        )
        # sys.exit kills pytest for some unexplainable reason so wrap in main check
        if __name__ == "__main__":
            sys.exit(1)
        else:
            raise

    return (config, cfg_players, cfg_playertypes, cfg_teams, messages)


# Load messages
def load_messages(messagefile=None) -> dict:
    """Loads messages from a JSON file."""
    messages = {}
    try:
        if messagefile:
            if os.path.exists(messagefile):
                with open(messagefile, encoding="utf-8") as f:
                    messages.update(json.load(f))
            else:
                print(
                    f"{Fore.YELLOW}Provided messages file ({messagefile}) does not exist. Skipping."
                )
        print(f'{Fore.GREEN}Message file "{messagefile}" loaded successfully.')
    except Exception as e:
        print(
            f"{Fore.RED}Unable to load messages.\n"
            + "".join(traceback.format_exception(type(e), e, e.__traceback__))
        )
        # sys.exit kills pytest for some unexplainable reason so wrap in main check
        if __name__ == "__main__":
            sys.exit(1)
        else:
            raise

    return messages


def load_players(playernames, playertypes, teams: list, use_teams=False):
    """
    Builds the player list with SBRSPlayer objects from the previously loaded player files.
    Also builds the teams if specified.

    Args:
        teams (list): List of teams to build.
        cfg_playernames (list): List of player names to build.
        cfg_playertypes (list): List of player types to build.

    Returns:
        tuple: A tuple containing:
            - players (list): A list of SBRSPlayer objects.
            - remaining_players (list): A list of SBRSPlayer objects that were not loaded.
            - teams (list): A list of SBRSTeam objects.
    """
    players = []
    try:
        for player in playernames:
            if use_teams:
                if teams[playernames.index(player)] not in teams:
                    teams.append(SBRSTeam(teams[playernames.index(player)]))
            if player not in players:
                try:
                    target_type = playertypes[playernames.index(player)]
                except IndexError:
                    target_type = "Default"
                players.append(
                    SBRSPlayer(
                        player,
                        team=(teams[playernames.index(player)] if use_teams else None),
                        playertype=target_type,
                    )
                )
        print(f"{Fore.GREEN}Players loaded successfully.")
    except Exception as e:
        print(
            f"{Fore.RED}Unable to load players.\n"
            + "".join(traceback.format_exception(type(e), e, e.__traceback__))
        )
        # sys.exit kills pytest for some unexplainable reason so wrap in main check
        if __name__ == "__main__":
            sys.exit(1)
    return players, teams


def initialize_logger(nosave=False, configpath=None):
    """Initialize logger that allows saving of games."""
    try:
        if nosave:
            raise Exception("Saving was disabled via command line argument.")
        if not os.path.exists("logs"):
            os.mkdir("logs")
        sbrs_game_logger = logging.getLogger("")
        sbrs_game_logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f"logs/sbrs-{int(time.time())}.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        sbrs_game_logger.addHandler(handler)
        print(f"{Fore.GREEN}Logger initialized successfully.{Style.RESET_ALL}")
        sbrs_game_logger.info("SBRS version: %s", __version__)
        sbrs_game_logger.info("Config file: %s", configpath)
    except Exception as e:
        print(
            f"{Fore.YELLOW}Unable to initialize logger.\n{"".join(traceback.format_exception(type(e), e, e.__traceback__))}"
        )
        print(f"{Fore.YELLOW}Game will not be saved.")
        sbrs_game_logger = None
    return sbrs_game_logger


def verification_checks(players, messages):
    """Checks to ensure the configuration is valid."""
    # ---- Player verification checks
    # Check to ensure more than one player
    if len(players) < 2:
        raise ValueError(
            "Only one player was specified. Please specify at least two players."
        )
    # Check to ensure player names are unique
    if len(players) != len(set(players)):
        raise ValueError(
            "Player names are not unique (more than one player has the same name). \
            Please make sure player names are unique."
        )

    # ---- Message verification checks
    # Check to make sure messages isn't empty
    if len(messages) == 0:
        raise ValueError(
            'No messages were specified. Did you forget to specify "extra-message-files"?'
        )
    # Check to ensure all message types have at least one message
    for message_type in [
        "passive",
        "passive-death",
        "attack-success",
        "attack-fail",
        "passive-attack",
        "winner",
        "most-kills",
    ]:
        if message_type not in messages:
            raise ValueError(
                f'Message type "{message_type}" not found in messages file.'
            )
        else:
            if len(messages[message_type]["Default"]) == 0:
                raise ValueError(
                    f'Message type "{message_type}" in messages file does not have any messages for the Default type. Please add at least one message.'
                )


def load_everything(configpath=None, nosave=False) -> tuple:
    """
    Quickly loads everything needed to run the game, and runs verification checks.

    Args:
        configpath (str): The path to the config file.
        nosave (bool): If True, the game will not be saved.

    Returns:
        tuple: A tuple containing:
            - config (dict): The config file.
            - players (list): A list of SBRSPlayer objects.
            - playertypes (list): A list of SBRSPlayer types.
            - teams (list): A list of SBRSTeam objects.
            - messages (dict): The messages file.
            - sbrs_game_logger (logging.Logger | None): The logger for the game.
                None if there was an error initializing the logger, or if saving was disabled.
    """
    config, players, playertypes, teams, messages = load_config(configpath)
    players, teams = load_players(players, playertypes, teams, config["use-teams"])
    sbrs_game_logger = initialize_logger(nosave, configpath)
    # Message loading is handled in load_config
    # messages = load_messages(config["messages"])
    verification_checks(players, messages)

    return config, players, playertypes, teams, messages, sbrs_game_logger
