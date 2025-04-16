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
        game.add_action(
            SBRSAction("attack", "Player attacks another player", self.attack)
        )
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
                    target = random.choice(list(game.remaining_players))
            else:
                while target == player:
                    target = random.choice(list(game.remaining_players))
            if random.random() < game.config.attack_success_chance:
                game.game_print(
                    f"{game.message_color('attack-success')}{game.random_message("attack-success", player.type)
                    .replace('{player}', game.message_color('generic-player') + player.name + game.message_color('attack-success'))
                    .replace('{target}', game.message_color('target-player') + target.name + game.message_color('attack-success'))}"
                )
                target.kill()
                player.kills += 1
            elif not game.config.show_kills_only:
                game.game_print(
                    f"{game.message_color('attack-fail')}{game.random_message('attack-fail', player.type)
                    .replace('{player}', game.message_color('generic-player') + player.name + game.message_color('attack-fail'))
                    .replace('{target}', game.message_color('target-player') + target.name + game.message_color('attack-fail'))}"
                )
        elif not game.config.classic_behavior and not game.config.show_kills_only:
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
        highest_accessed_player_id = 10  # to allow while loop to actually work
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
                f"{game.message_color('passive-death')}{game.random_message('passive-death', player.type)
                .replace('{player}', game.message_color('generic-player') + player.name + game.message_color('passive-death'))}"
            )
            player.kill()

    def game_over(self, game: sbrs.SBRSGame):
        """
        Runs the game over logic on all addons.

        Args:
            game (sbrs.SBRSGame): The game being simulated.
        """
        if not game.config.use_teams:
            game.game_print(
                game.random_message("winner", game.remaining_players[0].type)
                .replace(
                    "{player}",
                    f"{game.message_color('generic-player')}{game.remaining_players[0].name}{game.message_color('winner')}",
                )
                .replace(
                    "{amount}",
                    f"{game.message_color('generic-player')}{str(game.remaining_players[0].kills)}{game.message_color('winner')}",
                )
            )
        else:
            for team in set(p.team for p in game.remaining_players):
                team_players = [p for p in game.remaining_players if p.team == team]
                game.game_print(
                    game.random_message("winner", team_players[0].type)
                    .replace(
                        "{player}",
                        f"{game.message_color('generic-player')}{team} ({', '.join(p.name for p in team_players)}){game.message_color('winner')}",
                    )
                    .replace(
                        "{amount}",
                        f"{game.message_color('generic-player')}{str(sum(p.kills for p in team_players))}{game.message_color('winner')}",
                    )
                )
        most_kills = 0
        most_kills_players = []
        for player in game.config.players:
            if player.kills > most_kills:
                most_kills = player.kills
                most_kills_players = [player]
            elif player.kills == most_kills:
                most_kills_players.append(player)
        players_str = ""
        if len(most_kills_players) == 1:
            players_str = f"{game.message_color('generic-player')}{most_kills_players[0].name}{game.message_color('most-kills')}"
        elif len(most_kills_players) == 2:
            players_str = f"{game.message_color('generic-player')}{most_kills_players[0].name} {game.message_color('most-kills')}and {game.message_color('generic-player')}{most_kills_players[1].name}{game.message_color('most-kills')}"
        else:
            for player in most_kills_players[:-1]:
                players_str += f"{game.message_color('generic-player')}{player.name}{game.message_color('most-kills')}, "
            players_str += f"{game.message_color('most-kills')}and {game.message_color('generic-player')}{most_kills_players[-1].name}{game.message_color('most-kills')}"
        game.game_print(
            f"{game.message_color('most-kills')}{game.random_message('most-kills', random.choice(most_kills_players).type)
            .replace('{player}', players_str)
            .replace(
                '{amount}',
                f"{game.message_color('generic-player')}{str(most_kills)}{game.message_color('most-kills')}"
            )}"
        )
