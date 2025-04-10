"""
The configuration file for sbrs.
"""

from dataclasses import dataclass
import logging

@dataclass
class SBRSConfig:
    """
    Dataclass for SBRS configuration.

    Attributes:
        config (dict): The config file.
        players (list): A list of SBRSPlayer objects.
        playertypes (list): A list of SBRSPlayer types.
        teams (list): A list of SBRSTeam objects.
        messages (dict): The messages file.
        sbrs_game_logger (logging.Logger | None): The logger for the game.
            None if there was an error initializing the logger, or if saving was disabled.
        message_colors (dict): The colors for the messages.
        classic_behavior (bool): If True, classic behavior is enabled.
        sudden_death (bool): If True, sudden death is enabled.
        passive_death_chance (int): The chance of a passive death per turn.
        attack_success_chance (int): The chance of a successful attack per turn.
        death_chances (dict): The chances of death per player type.
        show_kills_only (bool): If True, only show kills in the messages.
        turns (int): The number of turns in the game.
        use_teams (bool): If True, team mode is enabled.
        actions (list): A list of SBRSAction objects.
    """

    config: dict
    players: list
    playertypes: list
    teams: list
    messages: dict
    sbrs_game_logger: logging.Logger
    message_colors: dict
    classic_behavior: bool
    sudden_death: bool
    passive_death_chance: int
    attack_chance: int
    attack_success_chance: int
    death_chances: dict
    show_kills_only: bool
    turns: int
    use_teams: bool
    actions: list

    def __init__(
        self,
        config,
        players,
        playertypes,
        teams,
        messages,
        sbrs_game_logger,
        message_colors=None,
        classic_behavior=None,
        sudden_death=None,
        passive_death_chance=None,
        attack_chance=None,
        attack_success_chance=None,
        death_chances=None,
        show_kills_only=None,
        turns=None,
        use_teams=None,
        actions=None
    ):
        self.config = config
        self.players = players
        self.playertypes = playertypes
        self.teams = teams
        self.messages = messages
        self.sbrs_game_logger = sbrs_game_logger
        self.message_colors = message_colors
        self.classic_behavior = classic_behavior
        self.sudden_death = sudden_death
        self.passive_death_chance = passive_death_chance
        self.attack_chance = attack_chance
        self.attack_success_chance = attack_success_chance
        self.death_chances = death_chances
        self.show_kills_only = show_kills_only
        self.turns = turns
        self.use_teams = use_teams
        self.actions = actions

    def __str__(self):
        return "SBRSConfig"

    def __repr__(self):
        return "SBRSConfig"

    def __eq__(self, other):
        return self.config == other.config

    def __len__(self):
        return len(self.config)

    def __hash__(self):
        return hash(self.config)
