import React, { useContext } from "react";
import { useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import styles from "./googleAuthButton.module.css";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import { UserContext } from "../../userProvider";
export default function GoogleAuthButton() {
  const navigate = useNavigate();
  const { updateUser } = useContext(UserContext);

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

        // Send the user's data to the Flask backend
        const backendResponse = await axios.post(
          "http://localhost:5000/api/user",
          res.data
        );
        console.log(backendResponse);

        Cookies.set("token", response.access_token, {
          expires: 7,
          secure: true,
          sameSite: "Strict",
        });

        console.log("Token:", Cookies.get("token"));

        updateUser(res.data);

        navigate("/journal");
      } catch (err) {
        console.error(err);
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
