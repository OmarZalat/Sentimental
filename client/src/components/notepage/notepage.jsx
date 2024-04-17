import React, { useRef, useState } from "react";
import styles from "./notepage.module.css";

export default function Notepage() {
  const [journalEntry, setJournalEntry] = useState("");

  const handleChange = (e) => {
    setJournalEntry(e.target.value);
  };

  return (
    <>
      <div className={styles.journal}>
        <h1>Journal Entry</h1>
        <textarea
          className={`${styles.journal_entry} ${styles.notes}`}
          value={journalEntry}
          onChange={handleChange}
        />
        <button className={styles.save_button}>Save</button>
      </div>
    </>
  );
}
