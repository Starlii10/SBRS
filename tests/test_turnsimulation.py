"""
Unit tests: Simulating turns

All tests will succeed if the turn is simulated without any exceptions.
"""

# Pylint says we're redefining them, but this is the correct way to use fixtures in pytest
# pylint: disable=redefined-outer-name

import pytest
from sbrs import SBRSGame, basic_init

@pytest.fixture
def basic_game() -> SBRSGame:
    """
        Returns an SBRSGame object that will be used for the tests.
    """
    game = SBRSGame(basic_init("tests/configs/config-test_normal.json", True))
    return game

def test_simulate_turn_generic(basic_game: SBRSGame):
    """
        Simulates a basic turn.
    """
    basic_game.simulate_turn()
    assert True

def test_simulate_turn_classic(basic_game: SBRSGame):
    """
        Simulates a turn with classic behavior.
    """
    basic_game.config.classic_behavior = True
    basic_game.simulate_turn()
    assert True

def test_simulate_turn_sudden_death(basic_game: SBRSGame):
    """
        Simulates a turn with sudden death.
    """
    basic_game.sudden_death = True
    basic_game.simulate_turn()
    assert True
