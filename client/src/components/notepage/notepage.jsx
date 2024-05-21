import React, { useContext, useEffect, useRef, useState } from "react";
import styles from "./notepage.module.css";
import { UserContext } from "../../userProvider";
import axios from "axios";

export default function Notepage() {
  const { userData } = useContext(UserContext);
  const [journalEntry, setJournalEntry] = useState("");
  const [userId, setUserId] = useState(null);
  const [userEntries, setUserEntries] = useState([]);
  const [entryId, setEntryId] = useState(null);

  useEffect(() => {
    console.log("entryId:", entryId);
  }, [entryId]);

  useEffect(() => {
    // Fetch user data to get user_id based on email
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/users`);
        const data = await response.json();
        console.log(`userdata email is ${userData.email}`);
        console.log(`data is:`);
        console.log(userData);
        const user = data.find((user) => user.email === userData.email);
        if (user) {
          setUserId(user.user_id);
          console.log(`user id has been set successfuly`);
        } else {
          console.error("User not found for email:", userData.email);
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    if (userData && userData.email) {
      fetchUserData();
    }
  }, [userData]);

  // Fetch journal entries and filter by user id
  const fetchJournalEntries = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/journal");
      const data = response.data;
      const userEntries = data.filter((entry) => entry.user_id === userId);
      console.log(userEntries);
      setUserEntries(userEntries); // Assuming you have a state variable for user entries

      // If the user has entries, set the journalEntry state to the entry_text of the first entry
      if (userEntries.length > 0) {
        setJournalEntry(userEntries[0].entry_text);
        setEntryId(userEntries[0].entry_id); // Convert entry_id to string
      }
    } catch (error) {
      console.error("Error fetching journal entries:", error);
    }
  };

  useEffect(() => {
    // Only fetch if userId is not null
    if (userId) {
      fetchJournalEntries();
    }
  }, [userId]); // Depend on userId so it runs whenever userId changes

  const saveJournalEntry = async () => {
    try {
      if (entryId) {
        console.log("Entry already exists. Skipping save operation.");
        console.log(entryId);
        return;
      }

      const response = await fetch("http://localhost:5000/api/journal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          entry_text: journalEntry,
          entry_timestamp: new Date().toISOString(),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Journal entry saved successfully.");
        console.log(entryId);
        if (data.alert_message) {
          alert(data.alert_message); // Display the alert message
        }
      } else {
        console.error("Failed to save journal entry.");
      }
    } catch (error) {
      console.error("Error saving journal entry:", error);
    }
  };

  const handleChange = (e) => {
    setJournalEntry(e.target.value);
  };

  console.log(userId);
  return (
    <>
      <div className={styles.journal}>
        <h1>Journal Entry</h1>
        <textarea
          className={`${styles.journal_entry} ${styles.notes}`}
          value={journalEntry}
          onChange={handleChange}
          maxLength={1120}
        />
        <button className={styles.save_button} onClick={saveJournalEntry}>
          Save
        </button>
      </div>
    </>
  );
}
