import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../../userProvider";
import axios from "axios";

export default function Dashboard() {
  const { userData } = useContext(UserContext);
  const [userId, setUserId] = useState(null);
  const [userJournalEntryId, setUserJournalEntryId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);

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

  return (
    <>
      <div>Hello World</div>
      {analysisData && (
        <div>
          <h2>Analysis Data</h2>
          <pre>{JSON.stringify(analysisData, null, 2)}</pre>
        </div>
      )}
    </>
  );
}
