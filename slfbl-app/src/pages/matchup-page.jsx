import React, { useState, useEffect } from 'react';import DailyStatsTable from "../components/daily-stats-table/daily-stats-table";

import NavHeader from "../components/nav-header/nav-header";
import { HttpService } from "../services/http-service";
import './matchup-page.css';

const MatchupPage = () => {
  const [slfblTeams, setSlfblTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [playersTeam1, setPlayersTeam1] = useState([]);
  const [playersTeam2, setPlayersTeam2] = useState([]);
  const [selectedTeam1, setSelectedTeam1] = useState("");
  const [selectedTeam2, setSelectedTeam2] = useState("");
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [selectedStartingPitchers, setSelectedStartingPitchers] = useState([
    [null, null],
    [null, null],
    [null, null],
    [null, null],
    [null, null]
  ]);

  const startDate = "2026-05-04"; // month is 0-based
  const endDate = "2026-05-10"; // month is 0-based
  const dates = [];
  for (let d = new Date(startDate + "T00:00:00"); d <= new Date(endDate + "T23:59:59"); d.setDate(d.getDate() + 1)) {
      dates.push(new Date(d));
  }

  useEffect(() => {
    const fetchSlfblTeams = async () => {
      try {
        const teams = await HttpService.getSlfblTeams();
        setSlfblTeams(teams);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching SLFBL teams:", error);
      }
    };

    fetchSlfblTeams();
  }, []);

  if (loading) return <p>Loading...</p>;

  const handleTeamChange = (event, teamIndex) => {
    const selectedTeam = event.target.value;
    HttpService.getTeamDailyStats(startDate, endDate, selectedTeam)
      .then((response) => {
        if (teamIndex === 0) {
          setPlayersTeam1(response);
        } else {
          setPlayersTeam2(response);
        }
      })
      .catch((error) => console.error('Error fetching team daily stats:', error));
  };

  const removeStartingPitcher = (startingPitchers, teamIndex, playerId) => {
    startingPitchers.forEach(row => {
      if (row[teamIndex]?.playerId === playerId) {
        row[teamIndex] = null;  // If this player already existed in the SP selection, remove it
      }
    });
  };

  const selectPlayer = (playerId, teamIndex, playerName, playerPoints, pointsByDay, selected) => {
    let selectedTeam = teamIndex === 0 ? selectedTeam1 : selectedTeam2;

    if (typeof selected === "string") {
      // Selected a starting pitcher dropdown
      const startingPitchers = [...selectedStartingPitchers];
      removeStartingPitcher(startingPitchers, teamIndex, playerId);
      if (selected) {
        // Add the starting pitcher to the list
        const spIndex = Number.parseInt(selected) - 1;
        startingPitchers[spIndex][teamIndex] = { playerId, playerName, playerPoints, pointsByDay, countAllStarts: true };

        // Re-evaluate all previously selected SPs for this team to see if we need to update their countAllStarts value based on the total number of starts for this team
        let cumulativeStarts = 0;
        for (let i = 0; i < startingPitchers.length; i++) {
          if (startingPitchers[i][teamIndex]) {
            const spPointsByDay = startingPitchers[i][teamIndex].pointsByDay;
            const spNumStarts = spPointsByDay.filter(day => day && day !== "X").length;
            cumulativeStarts += spNumStarts;
            startingPitchers[i][teamIndex].countAllStarts = cumulativeStarts <= 6;
          }
        }
      }
      setSelectedStartingPitchers(startingPitchers);
    } else if (selected) {
      // If player is being selected, add to selected team and to selected players list
      selectedTeam = [...selectedTeam, { playerId, playerName, playerPoints }];
      teamIndex === 0 ? setSelectedTeam1(selectedTeam) : setSelectedTeam2(selectedTeam);
      if (teamIndex === 0 && selectedTeam1.length >= selectedTeam2.length || teamIndex === 1 && selectedTeam2.length >= selectedTeam1.length) {
        // Only add row object if the selected player's team has more or equal players than the other team
        let currentSelectedPlayers = selectedPlayers;
        if (teamIndex === 0) {
          currentSelectedPlayers = [...currentSelectedPlayers, { team1: { playerId, playerName, playerPoints } }];
        } else {
          currentSelectedPlayers = [...currentSelectedPlayers, { team2: { playerId, playerName, playerPoints } }];
        }
        setSelectedPlayers(currentSelectedPlayers);
      } else {
        // If the selected player's team has fewer players than the other team, add to existing row object
        const lastSelectedPlayerTeamIndex = teamIndex === 0 ? selectedTeam1.length : selectedTeam2.length;
        const newPlayerObject = { playerId, playerName, playerPoints };
        let currentSelectedPlayers = selectedPlayers;
        teamIndex === 0 ?
          currentSelectedPlayers[lastSelectedPlayerTeamIndex].team1 = newPlayerObject
          : currentSelectedPlayers[lastSelectedPlayerTeamIndex].team2 = newPlayerObject;
        setSelectedPlayers(currentSelectedPlayers);
      }
    } else {
      // If player is being deselected, remove from selected team and from selected players list
      selectedTeam = selectedTeam.filter((player) => player.playerId !== playerId);
      teamIndex === 0 ? setSelectedTeam1(selectedTeam) : setSelectedTeam2(selectedTeam);
      const rows = selectedPlayers.filter((row) => row.team1?.playerId === playerId || row.team2?.playerId === playerId);
      if (rows.length > 0) {
        const row = rows[0];
        if (row.team1 && row.team2) {
          // If both teams have a player in the row, just remove the deselected player
          // Need to cascade all subsequent rows up by one to fill in the gap left by the removed player
          let currentSelectedPlayers = selectedPlayers;
          const removedPlayerIndex = currentSelectedPlayers.findIndex((r) => r === row);
          if (removedPlayerIndex < selectedTeam.length) {  // Not minus 1 because we already removed the player from the selected team array
            let i = removedPlayerIndex;
            for (i = removedPlayerIndex; i < selectedTeam.length; i++) {
              teamIndex === 0 ? currentSelectedPlayers[i].team1 = currentSelectedPlayers[i + 1].team1 : currentSelectedPlayers[i].team2 = currentSelectedPlayers[i + 1].team2;
            }
            teamIndex === 0 ? delete currentSelectedPlayers[i].team1 : delete currentSelectedPlayers[i].team2; // Delete the last player's team from the last row since it has been cascaded up
            if (!currentSelectedPlayers[i].team1 && !currentSelectedPlayers[i].team2) {
              currentSelectedPlayers.pop(); // If the last row is now empty, remove it from the selected players array
            }
            setSelectedPlayers(currentSelectedPlayers);
          } else {
            // If the removed player is in the last row, just remove the player from the row object
            teamIndex === 0 ? delete row.team1 : delete row.team2;
            setSelectedPlayers([...selectedPlayers]);
          }
        } else {
          // If only one team has a player in the row, remove the entire row
          setSelectedPlayers(selectedPlayers.filter((r) => r !== row));
        }
      }

    }
  };

  const calculateStartingPitcherPoints = (teamIndex) => {
    let numStarts = 0;
    const totalPoints = selectedStartingPitchers.reduce((acc, row, rowIndex) => {
      return acc + (row[teamIndex]?.pointsByDay.reduce((dayAcc, day) => {
        if (!day || day === "X") {
          return dayAcc;  // If the pitcher didn't start that day, don't add any points and don't count it as a start
        }
        numStarts++;
        if (numStarts > 6) {
          return dayAcc; // Only count points for the first 6 starts by the 5 starting pitchers
        }
        return dayAcc + (Number(day) || 0);
      }, 0) || 0)
    }, 0);

    return totalPoints;
  };

  return (
    <div>
      <NavHeader />
      <h1>Matchup</h1>
      <div>
        <div>
          <p>Team 1:</p>
          <select className="team-select" onChange={(e) => handleTeamChange(e, 0)}>
            {slfblTeams?.map((team, index) => (
              <option key={index} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
          <DailyStatsTable data={playersTeam1} dates={dates} useLink={true} onPlayerSelected={(playerId, playerName, playerPoints, pointsByDay, selected) => selectPlayer(playerId, 0, playerName, playerPoints, pointsByDay, selected)} updateSelected={selectedStartingPitchers} />
        </div>
        <div className="team-2-div">
          <p>Team 2:</p>
          <select className="team-select" onChange={(e) => handleTeamChange(e, 1)}>
            {slfblTeams?.map((team, index) => (
              <option key={index} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
          <DailyStatsTable data={playersTeam2} dates={dates} useLink={true} onPlayerSelected={(playerId, playerName, playerPoints, pointsByDay, selected) => selectPlayer(playerId, 1, playerName, playerPoints, pointsByDay, selected)} updateSelected={selectedStartingPitchers} />
        </div>
      </div>
      <h2>Results</h2>
      <div>
        {selectedPlayers.length > 0 || selectedStartingPitchers.some(row => row.some(e => e != null)) ?
        <table className="points-table results-table bottom-spacing">
            <thead className="light-text">
              <tr className="row-dark">
                <th colSpan="2">Team 1</th>
                <th colSpan="2">Team 2</th>
              </tr>
              <tr className="row-light">
                <th>Player Name</th>
                <th>Total Points</th>
                <th>Player Name</th>
                <th>Total Points</th>
              </tr>
            </thead>
            <tbody>
              {selectedPlayers.map((row, index) => (
                <tr key={index} className={index % 2 === 0 ? "row-dark" : "row-light"}>
                  <td><p>{row.team1?.playerName}</p></td>
                  <td><p>{row.team1?.playerPoints}</p></td>
                  <td><p>{row.team2?.playerName}</p></td>
                  <td><p>{row.team2?.playerPoints}</p></td>
                </tr>
              ))}
              <tr className={selectedPlayers.length % 2 === 0 ? "row-dark" : "row-light"}>
                <td colSpan="4"><strong>Starting Pitcher Points:</strong></td>
              </tr>
              {selectedStartingPitchers.map((row, index) => (
                <tr key={"sp" + index} className={(selectedPlayers.length + index + 1) % 2 === 0 ? "row-dark" : "row-light"}>
                  <td><p>{row[0]?.playerName}</p></td>
                  <td><p>{(row[0]?.countAllStarts === false ? "(" : "") + (row[0]?.playerPoints ? row[0]?.playerPoints : "") + (row[0]?.countAllStarts === false ? ")" : "")}</p></td>
                  <td><p>{row[1]?.playerName}</p></td>
                  <td><p>{(row[1]?.countAllStarts === false ? "(" : "") + (row[1]?.playerPoints ? row[1]?.playerPoints : "") + (row[1]?.countAllStarts === false ? ")" : "")}</p></td>
                </tr>
              ))}
            </tbody>
            <tfoot className="light-text">
              <tr className={(selectedPlayers.length + selectedStartingPitchers.length + 1) % 2 === 0 ? "row-dark" : "row-light"}>
                <td><strong>Total</strong></td>
                <td><strong>{selectedPlayers.reduce((acc, row) => acc + (row.team1?.playerPoints || 0), 0) + calculateStartingPitcherPoints(0)}</strong></td>
                <td><strong>Total</strong></td>
                <td><strong>{selectedPlayers.reduce((acc, row) => acc + (row.team2?.playerPoints || 0), 0) + calculateStartingPitcherPoints(1)}</strong></td>
              </tr>
            </tfoot>
          </table>
          : <p>No players selected.</p>}
        </div>
    </div>
    );
};

export default MatchupPage;