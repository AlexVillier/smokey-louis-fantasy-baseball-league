from django.core.management.base import BaseCommand
from slfbl_app.static_functions import normalizeName
from slfbl_app.models import SlfblTeam, Player
from docx2python import docx2python
import re

class Command(BaseCommand):
    help = "Fetch and persist SLFBL team rosters"

    def handle(self, *args, **options):
        slfblTeamNames = SlfblTeam.objects.values_list('name_normalized', flat=True)
        print(f"Updating SLFBL team rosters...")

        with docx2python('./slfbl_app/rosters.docx') as docx_content:
            # Get all text from the body
            rostersText = docx_content.text

        currentTeam = None
        currentTeamPlayers = []
        inDVSection = False
        inInjuredReserveSection = False
        for line in rostersText.splitlines():
            line = line.strip()
            if line != '':
                if re.match(r'^[0-9]+\)', line):
                    # If the line starts with a number followed by a parenthesis, it's a player name. Remove the number and parenthesis.
                    line = re.sub(r'^[0-9]+\)\s*', '', line)
                    # Player names in the document also include their positions and MLB team separated by hyphens, so we need to remove that as well to get just the player name.
                    line = line.split('-')[0].strip()
                    name = normalizeName(line)
                    player = Player.objects.filter(name_normalized=name).first()

                    if player is None:
                        if not inDVSection and not inInjuredReserveSection:
                            print(f"Player {name} not found in database, skipping...")  # Only print a message if the player is on MLB roster and active
                        continue    # If the player isn't found in the database, skip this player
                    if player not in currentTeamPlayers:
                        player.slfblTeam = currentTeam
                        player.save()
                        print(f"Added {player.name} to {currentTeam}")
                    else:
                        currentTeamPlayers.remove(player)   # If the player is already in the current team, remove them from the list of players to be removed from the team
                elif normalizeName(line) in slfblTeamNames:
                    inDVSection = False
                    inInjuredReserveSection = False
                    currentTeam = SlfblTeam.objects.filter(name_normalized=normalizeName(line)).first()
                    currentTeamPlayers = list(Player.objects.filter(slfblTeam=currentTeam))
                    print(f"\n##### Processing team {currentTeam} #####")
                elif line.lower() == 'dv squad':
                    inDVSection = True
                    inInjuredReserveSection = False
                elif line.lower() == 'injured reserve':
                    inDVSection = False
                    inInjuredReserveSection = True
                else:
                    inDVSection = False
                    inInjuredReserveSection = False
        for player in currentTeamPlayers:
            player.slfblTeam = None
            player.save()
        print("\nDone updating SLFBL team rosters.")