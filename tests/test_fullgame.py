"""
Unit tests: Running a full game

All tests will succeed if the game is run without any exceptions.
"""

import pytest # pylint: disable=unused-import
from sbrs import SBRSGame, basic_init

def test_run_game_normal():
    """A normal game with ten players."""
    game = SBRSGame(basic_init("tests/configs/config-test_normal.json", True))
    game.run_game()
    assert True

def test_run_game_stresstest():
    """
        A game with a lot of players and a lot of turns.
        Helps to test edge cases. May take a few seconds to run.
    """
    game = SBRSGame(basic_init("tests/configs/config-test_stresstest.json", True))
    game.run_game()
    assert True

def test_run_game_teams():
    """
        A game with teams.
    """

    game = SBRSGame(basic_init("tests/configs/config-test_teams.json", True))
    game.run_game()
    assert True
