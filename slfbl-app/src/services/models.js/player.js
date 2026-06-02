class Player {

    playerId = 0;
    name = "";
    qualifiedPositions = [];
    mlbTeam = "";
    slfblTeam = "";

    constructor(playerId, name, qualifiedPositions, mlbTeam, slfblTeam) {
        this.playerId = playerId;
        this.name = name;
        this.qualifiedPositions = qualifiedPositions;
        this.mlbTeam = mlbTeam;
        this.slfblTeam = slfblTeam;
    }
}