import React from "react";
import styles from "./landing.module.css";
import GoogleAuthButton from "../../components/googleAuthButton/googleAuthButton";

export default function Landing() {
  return (
    <>
      <div className={styles.container}>
        <div className={styles.landing_pic_1}></div>
        <div className={styles.landing_pic_2}></div>
        <GoogleAuthButton />
      </div>
    </>
  );
}
