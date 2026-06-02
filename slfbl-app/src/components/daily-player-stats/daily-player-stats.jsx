import { useState } from 'react';
import "./daily-player-stats.css";

const DailyPlayerStats = (props) => {
    const rowClass = props.index % 2 === 0 ? "row-dark" : "row-light";

    return (
        <tr key={props.index} className={rowClass}>
            <td>
                {
                    props.qualifiedPositions.includes("SP") ?
                    <select value={props.updateSelected} onChange={(event) => props.onPlayerSelected(event.target.value)}>
                        <option value="">Select SP#</option>
                        <option value="1">SP#1</option>
                        <option value="2">SP#2</option>
                        <option value="3">SP#3</option>
                        <option value="4">SP#4</option>
                        <option value="5">SP#5</option>
                    </select>
                    : <input type="checkbox" onChange={(event) => props.onPlayerSelected(event.target.checked)} />
                }
            </td>
            <td className="column">
                {props.useLink ?
                <a href={`/players/${props.playerId}`}>{props.playerName}</a>
                : <strong>{props.playerName}</strong>
                }
            </td>
            {props.points.map((point, index) => (
                <td key={index} className="column"><p>{point}</p></td>
            ))}
            <td className="column"><p>{props.totalPoints}</p></td>
        </tr>
    );
};
export default DailyPlayerStats;