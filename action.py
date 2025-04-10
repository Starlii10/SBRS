"""
    SBRSAction object.
"""

class SBRSAction:
    """
        Represents a possible action for a player to take per turn.

        Attributes:
            name (str): The name of the action.
            description (str): The description of the action.
            function (function): The function to call when the action is taken.
    """

    def __init__(self, name, description, function):
        """
            Initializes the SBRSAction object.

            Args:
                name (str): The name of the action.
                description (str): The description of the action.
                function (function): The function to call when the action is taken.
                                     Should take an SBRSGame and an SBRSPlayer as arguments.
        """
        self.name = name
        self.description = description
        if function is None:
            raise ValueError("SBRSAction must have a function.")
        self.function = function

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
