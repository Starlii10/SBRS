"""
    The basic game behavior for SBRS, in the form of
    SBRSActions and SBRSAddons.

    This file should not be modified. Use an addon instead.
"""

import random
import sbrs
from action import SBRSAction
from player import SBRSPlayer
from sbrs import SBRSAddon

class Addon(SBRSAddon):
    """
        The base game behavior for SBRS in the form of an SBRSAddon.
    """

    def initgame(self, game: sbrs.SBRSGame):
        game.add_action(SBRSAction("attack", "Player attacks another player", self.attack))
        game.add_action(SBRSAction("passive", "Player does nothing", self.passive))
        game.add_action(SBRSAction("passive-death", "Player dies", self.passive_death))

    def start_turn(self, game):
        if (
            not game.config.classic_behavior
            and len(game.remaining_players) <= len(game.config.players) * 0.1
            and not game.sudden_death
        ):
            # SUDDEN DEATH: bump death chance to 100% at 10% players remaining
            game.sudden_death = True
            game.game_print(
                f"{game.message_color('attack-success')}SUDDEN DEATH - All attacks are guaranteed to succeed\n"
            )
            game.config.attack_chance = 1
            game.config.passive_death_chance = 1
            game.config.attack_success_chance = 1

    def attack(self, game: sbrs.SBRSGame, player: SBRSPlayer):
        """
            Player attacks another player.

            Args:
                game (sbrs.SBRSGame): The game being simulated.
                player (sbrs.SBRSPlayer): The player who took the action.
        """
        if random.random() < game.config.attack_chance:
            target = random.choice(list(game.remaining_players))
            if game.config.use_teams:
                while target.team == player.team:
                    target = random.choice(
                        list(game.remaining_players)
                    )
            else:
                while target == player:
                    target = random.choice(
                        list(game.remaining_players)
                    )
            if random.random() < game.config.attack_success_chance:
                game.game_print(
                    f"{game.message_color('attack-success')}{game.random_message("attack-success", player.type)
                    .replace('{player}', game.message_color('generic-player') + player.name + game.message_color('attack-success'))
                    .replace('{target}', game.message_color('target-player') + target.name + game.message_color('attack-success'))}"
                )
                target.kill()
                player.kills += 1
                game.remaining_players = [
                    p for p in game.remaining_players if p.alive
                ]
                if len(game.remaining_players) == 1:
                    game.game_over()
            elif not game.config.show_kills_only:
                game.game_print(
                    f"{game.message_color('attack-fail')}{game.random_message('attack-fail', player.type)
                    .replace('{player}', game.message_color('generic-player') + player.name + game.message_color('attack-fail'))
                    .replace('{target}', game.message_color('target-player') + target.name + game.message_color('attack-fail'))}"
                )
        elif (
            not game.config.classic_behavior
            and not game.config.show_kills_only
        ):
            game.game_print(
                f"{game.message_color('passive-attack')}{game.random_message('passive-attack', player.type)
                .replace('{player}', game.message_color('generic-player') + player.name + game.message_color('passive-attack'))}"
            )

    def passive(self, game: sbrs.SBRSGame, player: SBRSPlayer):
        """
            Player does nothing.

            Args:
                game (sbrs.SBRSGame): The game being simulated.
                player (sbrs.SBRSPlayer): The player who took the action.
        """
        num_players = random.randint(
            1,
            (4 if len(game.remaining_players) >= 4 else len(game.remaining_players)),
        )
        players_to_include = []
        while len(players_to_include) < num_players:
            player_to_include = random.choice(game.remaining_players)
            if player_to_include not in players_to_include:
                players_to_include.append(player_to_include)
        message = game.random_message("passive", player.type)
        highest_accessed_player_id = (
            10  # to allow while loop to actually work
        )
        while highest_accessed_player_id > len(players_to_include):
            message = game.random_message("passive", player.type)
            # find highest accessed player ID ({playerx})
            highest_accessed_player_id = 0
            for i in range(1, 5):
                if f"{{player{i}}}" in message:
                    highest_accessed_player_id = i
        message = message.replace(
            "{player1}",
            game.message_color("generic-player")
            + player.name
            + game.message_color("passive"),
        )
        try:
            message = message.replace(
                "{player2}",
                game.message_color("generic-player")
                + players_to_include[0].name
                + game.message_color("passive"),
            )
            message = message.replace(
                "{player3}",
                game.message_color("generic-player")
                + players_to_include[1].name
                + game.message_color("passive"),
            )
            message = message.replace(
                "{player4}",
                game.message_color("generic-player")
                + players_to_include[2].name
                + game.message_color("passive"),
            )
        except IndexError:
            pass  # too many players for this message, but it's alright
        game.game_print(f"{game.message_color('passive')}{message}")

    def passive_death(self, game: sbrs.SBRSGame, player: SBRSPlayer):
        """
            Player dies.

            Args:
                game (sbrs.SBRSGame): The game being simulated.
                player (sbrs.SBRSPlayer): The player who took the action.
        """
        if random.random() < game.config.passive_death_chance:
            game.game_print(
                f"{game.message_color('passive-death')}{game.random_message('passive-death', player.type).replace('{player}', game.message_color('generic-player') + player.name + game.message_color('passive-death'))}"
            )
            player.kill()
            game.remaining_players = [p for p in game.remaining_players if p.alive]
            if len(game.remaining_players) == 1:
                game.game_over()
