"""
Starlii's Battle Royale Simulator
A Hunger Games Simulator-like game written in Python
based on the original Scratch version
https://github.com/Starlii10/sbrs

Copyright (c) 2024 Starlii10
Insert license here
"""

from team import SBRSTeam

class SBRSPlayer:
    """
    Represents a player in SBRS.
    
    Attributes:
        name (str): The name of the player.
        team (SBRSTeam): The team the player is on. If None, the player is not on a team (default for FFA).
        type (str): The player's type. Determines what type of messages to use. (default is "Default").
        alive (bool): Whether or not the player is alive. If dead, the player's turn is skipped..
        kills (int): The number of kills the player has.
        addon_data (dict): A dictionary of data that addons can use.
    """

    # Boring python class stuff
    def __init__(self, name: str, team: SBRSTeam = None, playertype: str = "Default"):
        self.name = name
        """The name of the player."""
        self.team = team
        """The team the player is on. If None, the player is not on a team (default for FFA)."""
        self.type = playertype
        """The player's type. Determines what type of messages to use. (default is "Default")."""
        self.alive = True
        """Whether or not the player is alive. If dead, the player's turn is skipped.."""
        self.kills = 0
        """The number of kills the player has."""
        self.addon_data = {}
        """A dictionary of data that addons can use."""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, SBRSPlayer):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        if isinstance(other, SBRSPlayer):
            return self.name < other.name
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, SBRSPlayer):
            return self.name > other.name
        else:
            return False

    def __le__(self, other):
        if isinstance(other, SBRSPlayer):
            return self.name <= other.name
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, SBRSPlayer):
            return self.name >= other.name
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, SBRSPlayer):
            return self.name != other.name
        else:
            return False

    def __bool__(self):
        return self.alive

    def __len__(self):
        return self.kills

    def kill(self):
        """Kills the player."""
        self.alive = False
