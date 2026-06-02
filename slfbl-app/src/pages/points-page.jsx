import React, { useState, useEffect } from 'react';
import NavHeader from "../components/nav-header/nav-header";
import { HttpService } from "../services/http-service";
import DailyPlayerStats from "../components/daily-player-stats/daily-player-stats";
import DailyStatsTable from '../components/daily-stats-table/daily-stats-table';
import "./points-page.css";

const PointsPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const startDate = "2026-05-04"; // month is 0-based
  const endDate = "2026-05-10"; // month is 0-based
  const dates = [];
  for (let d = new Date(startDate + "T00:00:00"); d <= new Date(endDate + "T23:59:59"); d.setDate(d.getDate() + 1)) {
    dates.push(new Date(d));
  }

  useEffect(() => {
    // API call inside useEffect to run on mount
    HttpService.getDailyPlayerStats(startDate, endDate)
      .then((response) => {
        setData(response);
        setLoading(false);
      })
      .catch((error) => console.error('Error fetching data:', error));
  }, []); // Empty dependency array ensures this runs only once

  if (loading) return <p>Loading...</p>;

  if (!data || data.length === 0) return <p>No data available.</p>;

  return (
    <div>
      <NavHeader />
      <h1>Weekly Points Page</h1>
      <div>
        <DailyStatsTable data={data} dates={dates} useLink={true} />
      </div>
    </div>
  );
};
export default PointsPage;