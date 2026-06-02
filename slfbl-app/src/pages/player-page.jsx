import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import NavHeader from "../components/nav-header/nav-header";
import DailyStatsTable from '../components/daily-stats-table/daily-stats-table';
import { HttpService } from "../services/http-service";

const PlayerPage = (props) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [weekData, setWeekData] = useState([]);
    const [weekLoading, setWeekLoading] = useState(true);
    const startDate = "2026-05-04"; // month is 0-based
    const endDate = "2026-05-10"; // month is 0-based
    const dates = [];
    for (let d = new Date(startDate + "T00:00:00"); d <= new Date(endDate + "T23:59:59"); d.setDate(d.getDate() + 1)) {
        dates.push(new Date(d));
    }

    // Get the playerId from the URL parameters
    const { playerId } = useParams();

    useEffect(() => {
        // API call inside useEffect to run on mount
        HttpService.getPlayer(playerId)
            .then((response) => {
                console.log("Player data:", response);
                setData(response);
                setLoading(false);
            })
            .catch((error) => console.error('Error fetching data:', error));
        HttpService.getDailyPlayerStats(startDate, endDate, playerId)
            .then((response) => {
                setWeekData(response);
                setWeekLoading(false);
            })
            .catch((error) => console.error('Error fetching data:', error));
    }, []); // Empty dependency array ensures this runs only once

    if (loading || weekLoading) return <p>Loading...</p>;

    if (!data || data.length === 0) return <p>No data available.</p>;

    return (
        <div>
            <NavHeader />
            <h1>Player Details</h1>
            <h2>{data.name}</h2>
            <p>{data.mlbTeam} - {data.qualifiedPositions}</p>
            <h3>Current Week Scores</h3>
            <DailyStatsTable data={weekData} dates={dates} />
            <h3>Season to Date (Weekly)</h3>
        </div>
    );
};
export default PlayerPage;