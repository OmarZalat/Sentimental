import React, { useContext, useEffect, useRef, useState } from "react";
import styles from "./notepage.module.css";
import { UserContext } from "../../userProvider";

export default function Notepage() {
  const { userData } = useContext(UserContext);
  const [journalEntry, setJournalEntry] = useState("");
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    // Fetch user data to get user_id based on email
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/users`);
        const data = await response.json();
        console.log(`userdata email is ${userData.email}`);
        console.log(`data is ${data}`);
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
        <button className={styles.save_button}>Save</button>
      </div>
    </>
  );
}
