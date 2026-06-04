import axios from "axios";

export class HttpService {

    static API_URL = import.meta.env.VITE_API_URL || "/api";

    static async getPlayer(playerId) {
        try {
            const res = (await axios.get(`${this.API_URL}/players/${playerId}`)).data;
            console.log("Player data:", res);
            return res;
        } catch (error) {
            console.error("Error fetching player data:", error);
            throw error;
        }
    }

    static async getDailyPlayerStats(startDate, endDate, playerId = null) {
        try {
            const res = (await axios.get(`${this.API_URL}/daily-player-stats/`, {
                params: {
                    start_date: startDate,
                    end_date: endDate,
                    player_id: playerId
                }
            })).data;
            console.log("Results:", res);
            return res;
        } catch (error) {
            console.error("Error fetching daily player stats:", error);
            throw error;
        }
    }

    static getWeeklyPlayerStats() {
        return axios.get(`${this.API_URL}/weekly-player-stats/`);
    }

    static getSeasonPlayerStats() {
        return axios.get(`${this.API_URL}/season-player-stats/`);
    }

    static async getSlfblTeams() {
        try {
            const res = (await axios.get(`${this.API_URL}/slfbl-teams/`)).data.results;
            console.log("SLFBL Teams:", res);
            return res;
        } catch (error) {
            console.error("Error fetching SLFBL teams:", error);
            throw error;
        }
    }

    static async getTeamDailyStats(startDate, endDate, teamId) {
        try {
            const res = (await axios.get(`${this.API_URL}/daily-player-stats/`, {
                params: {
                    start_date: startDate,
                    end_date: endDate,
                    slfbl_team_id: teamId
                }
            })).data;
            console.log("Team Daily Stats:", res);
            return res;
        } catch (error) {
            console.error("Error fetching team daily stats:", error);
            throw error;
        }
    }
}