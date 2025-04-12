"""
    Starlii's Battle Royale Simulator
    A Hunger Games Simulator-like game written in Python
    https://github.com/Starlii10/sbrs

    Copyright (c) 2024 Starlii10
    Insert license here
"""

class SBRSTeam:
    """
        Represents a team of players in SBRS.

        Attributes:
            name (str): The name of the team.
            players (list): A list of players in the team.
            addon_data (dict): A dictionary of data that addons can use.
    """
    
    # Boring python class stuff
    def __init__(self, name):
        self.name = name
        """The name of the team."""
        self.players = []
        """A list of players in the team."""
        self.addon_data = {}
        """A dictionary of data that addons can use."""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, SBRSTeam):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        if isinstance(other, SBRSTeam):
            return self.name < other.name
        return False

    def __gt__(self, other):
        if isinstance(other, SBRSTeam):
            return self.name > other.name
        return False

    def __le__(self, other):
        if isinstance(other, SBRSTeam):
            return self.name <= other.name
        return False

    def __ge__(self, other):
        if isinstance(other, SBRSTeam):
            return self.name >= other.name
        return False

    def __ne__(self, other):
        if isinstance(other, SBRSTeam):
            return self.name != other.name
        return False

    def __bool__(self):
        for player in self.players:
            if player.alive:
                return True
        return False

    def __len__(self):
        return len(self.players)

    def __getitem__(self, index):
        return self.players[index]

    def __setitem__(self, index, value):
        self.players[index] = value

    def __iter__(self):
        return iter(self.players)

    def add_player(self, player):
        """
            Adds a player to the team.

            Args:
                player (SBRSPlayer): The player to add.
        """
        self.players.append(player)
        player.team = self

    def remove_player(self, player):
        """
            Removes a player from the team.

            Args:
                player (SBRSPlayer): The player to remove.
            
            Notes:
                This sets the player's team to None. Some wacky things happen
                if a player with no team is placed in a team game.
        """
        self.players.remove(player)
        player.team = None
