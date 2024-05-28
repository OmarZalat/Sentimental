import React from "react";
import styles from "./journal.module.css";
import Notepage from "../../components/notepage/notepage";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

export default function Journal() {
  const navigate = useNavigate();

  const handleSignOut = () => {
    // Clear the token cookie
    Cookies.remove("token");

    // Redirect the user to the landing page
    navigate("/");
  };
  return (
    <>
      <div className={styles.container}>
        <div className={styles.notepage}>
          <Notepage />
        </div>
        <div className={styles.wrapper}>
          <div className={styles.navigation}>
            <button
              className={styles.dashboard_button}
              onClick={() => navigate("/dashboard")}
            >
              Dashboard
            </button>
            <button className={styles.signOut_button} onClick={handleSignOut}>
              Sign out
            </button>
          </div>
          <div className={styles.journal_pic}></div>
        </div>
      </div>
    </>
  );
}
