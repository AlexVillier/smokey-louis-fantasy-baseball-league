import { useState } from "react";
import DailyPlayerStats from "../daily-player-stats/daily-player-stats";
import "./daily-stats-table.css";

const DailyStatsTable = (props) => {
    const [selectedValue, setSelectedValue] = useState([]);

    const determineIndex = (updateSelected, playerName, arrIndex) => {
      let index = -1;
      updateSelected.forEach((row, i) => {
        if (row?.some(e => e?.playerName === playerName)) {
          index = i;
        }
      });
      const selectedValuesArr = [...selectedValue];
      const newValue = index === -1 ? "" : "" + (index + 1);
      selectedValuesArr.forEach((value, ind) => {
        if (value === newValue) {
          selectedValuesArr[ind] = "";  // Clear the previous selection if the same SP# is selected again
        }
      });
      selectedValuesArr[arrIndex] = newValue;
      setSelectedValue(selectedValuesArr);
    };

    const playerSelected = (stat, selected, index) => {
      props.onPlayerSelected(stat.playerId, stat.name, stat.totalPoints, stat.points, selected);
      determineIndex(props.updateSelected, stat.name, index);
    }

    return (
        <table className="points-table">
          <thead>
            <tr className="row-light">
              <th></th>
              <th>Player Name</th>
              {props.dates.map((date, index) => (
                <th key={index}>{date.toLocaleDateString("en-US", { month: "numeric", day: "numeric" })}</th>
              ))}
              <th>Total Points</th>
            </tr>
          </thead>
          <tbody>
            {props.data.map((stat, index) => (
                <DailyPlayerStats
                  key={index}
                  index={index}
                  playerName={stat.name}
                  playerId={stat.playerId}
                  points={stat.points}
                  totalPoints={stat.totalPoints}
                  useLink={props.useLink}
                  qualifiedPositions={stat.qualifiedPositions}
                  onPlayerSelected={(selected) => playerSelected(stat, selected, index)}
                  updateSelected={selectedValue[index]}
                />
            ))}
          </tbody>
        </table>
    );
};
export default DailyStatsTable;