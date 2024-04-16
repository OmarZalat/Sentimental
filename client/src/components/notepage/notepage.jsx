import React, { useRef } from "react";
import styles from "./notepage.module.css";

export default function Notepage() {
  const inputs = Array.from({ length: 11 }, () => useRef(null));

  const handleInputChange = (index, event) => {
    const input = event.target;
    const { value, selectionStart, selectionEnd } = input;

    if (value.length >= 100 && inputs[index + 1]) {
      inputs[index + 1].current.focus();

      if (selectionStart === selectionEnd) {
        const nextInput = inputs[index + 1].current;
        nextInput.selectionStart = nextInput.selectionEnd = 0;
      }
    }
  };

  return (
    <div className={styles.ruled_lines_container}>
      {inputs.map((ref, index) => (
        <input
          key={index}
          ref={ref}
          className={styles.ruled_line_input}
          type="text"
          maxLength={100}
          onChange={(event) => handleInputChange(index, event)}
        />
      ))}
      <button className={styles.save_button}>Save</button>
    </div>
  );
}
