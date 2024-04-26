import React from "react";
import { useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import styles from "./googleAuthButton.module.css";
import { useNavigate } from "react-router-dom";

export default function GoogleAuthButton() {
  const navigate = useNavigate();

  const login = useGoogleLogin({
    onSuccess: async (response) => {
      try {
        const res = await axios.get(
          "https://www.googleapis.com/oauth2/v1/userinfo",
          {
            headers: {
              Authorization: `Bearer ${response.access_token}`,
            },
          }
        );
        console.log(res);

        navigate("/journal");
      } catch (err) {
        console.log(err);
      }
    },
  });
  return (
    <>
      <button className={styles.authButton} onClick={() => login()}>
        Sign in
      </button>
      ;
    </>
  );
}
