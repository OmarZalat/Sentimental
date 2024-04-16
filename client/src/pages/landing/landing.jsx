import React from "react";
import styles from "./landing.module.css";

export default function Landing() {
  return (
    <>
      <div className={styles.container}>
        <div className={styles.landing_pic_1}></div>
        <div className={styles.landing_pic_2}></div>
        <button className={styles.signIn_button}>Sign in</button>
      </div>
    </>
  );
}
