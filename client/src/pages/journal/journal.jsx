import React from "react";
import styles from "./journal.module.css";
import Notepage from "../../components/notepage/notepage";

export default function Journal() {
  return (
    <>
      <div className={styles.container}>
        <div className={styles.notepage}>
          <Notepage />
        </div>
        <div className={styles.wrapper}>
          <div className={styles.navigation}>
            <button className={styles.dashboard_button}>Dashboard</button>
            <button className={styles.signOut_button}>Sign out</button>
          </div>
          <div className={styles.journal_pic}></div>
        </div>
      </div>
    </>
  );
}
