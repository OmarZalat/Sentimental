import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../../userProvider";
import axios from "axios";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";
import { useNavigate } from "react-router-dom";
import styles from "./dashboard.module.css";

// Register the necessary components
ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {
  const { userData } = useContext(UserContext);
  const [userId, setUserId] = useState(null);
  const [userJournalEntryId, setUserJournalEntryId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserDataAndJournalEntry = async () => {
      try {
        // Fetch user data to get user_id based on email
        const userResponse = await fetch(`http://127.0.0.1:5000/api/users`);
        const users = await userResponse.json();
        console.log(`User data email is ${userData.email}`);

        const user = users.find((u) => u.email === userData.email);
        if (user) {
          setUserId(user.user_id);
          console.log(`User ID has been set successfully: ${user.user_id}`);

          // Fetching journal entries
          const journalResponse = await axios.get(
            "http://localhost:5000/api/journal"
          );
          const journalEntries = journalResponse.data;
          // Finding the user entry
          const userEntry = journalEntries.find(
            (entry) => entry.user_id === user.user_id
          );
          if (userEntry) {
            setUserJournalEntryId(userEntry.entry_id);
            console.log(`Journal entry ID has been set: ${userEntry.entry_id}`);
          } else {
            console.error("Journal entry not found for user ID:", user.user_id);
          }
        } else {
          console.error("User not found for email:", userData.email);
        }
      } catch (error) {
        console.error("Error fetching user data or journal entry:", error);
      }
    };

    if (userData && userData.email) {
      fetchUserDataAndJournalEntry();
    }
  }, [userData]);

  useEffect(() => {
    const fetchAnalysisData = async () => {
      try {
        if (userJournalEntryId) {
          const response = await axios.get(
            `http://localhost:5000/api/analysis/${userJournalEntryId}`
          );
          setAnalysisData(response.data);
          console.log("Fetched analysis data:", response.data);
        }
      } catch (error) {
        console.error("Error fetching analysis data:", error);
      }
    };

    if (userJournalEntryId) {
      fetchAnalysisData();
    }
  }, [userJournalEntryId]);

  const getSentimentScores = () => {
    if (analysisData && analysisData[0] && analysisData[0].sentiment_score) {
      try {
        return JSON.parse(analysisData[0].sentiment_score);
      } catch (e) {
        console.error("Error parsing sentiment scores:", e);
        return { neg: 0, neu: 0, pos: 0 };
      }
    }
    return { neg: 0, neu: 0, pos: 0 };
  };

  const sentimentScores = getSentimentScores();

  const data = {
    labels: ["Negative", "Neutral", "Positive"],
    datasets: [
      {
        data: [sentimentScores.neg, sentimentScores.neu, sentimentScores.pos],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
        hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
  };

  const displayTopicKeywords = () => {
    if (analysisData && analysisData[0] && analysisData[0].topic_keywords) {
      const keywords = analysisData[0].topic_keywords
        .replace("[", "")
        .replace("]", "")
        .replace(/"/g, "")
        .split(",")
        .map((keyword) => keyword.trim());

      return (
        <div className={styles.repeatedWords}>
          <h2>Most repeated words in your journal:</h2>
          <ul className={styles.keywordsList}>
            {keywords.map((keyword, index) => (
              <li key={index}>{keyword}</li>
            ))}
          </ul>
        </div>
      );
    }
    return null;
  };

  return (
    <>
      {analysisData && (
        <div className={styles.analytics}>
          <div className={styles.navigation}>
            <button
              className={styles.backButton}
              onClick={() => navigate("../journal")}
            >
              back
            </button>
          </div>
          <div className={styles.mood}>
            <h2>Your overall mood of today's journal is:</h2>
            <div
              className={styles.pieChartWrapper}
              style={{ position: "relative", width: "50%", height: "50%" }}
            >
              <Pie data={data} options={options} />
            </div>
          </div>

          {displayTopicKeywords()}
        </div>
      )}
    </>
  );
}
