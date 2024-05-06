import React, { useContext, useRef, useState } from "react";
import styles from "./notepage.module.css";
import { UserContext } from "../../userProvider";

export default function Notepage() {
  const { userData } = useContext(UserContext);
  const [journalEntry, setJournalEntry] = useState("");

  const handleChange = (e) => {
    setJournalEntry(e.target.value);
  };

  console.log(userData);
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
