import React, { createContext, useState } from "react";

export const UserContext = createContext(); // Changed export to named export

export default function UserProvider({ children }) {
  const [userData, setUserData] = useState(null);

  const updateUser = (data) => {
    setUserData(data);
  };

  return (
    <UserContext.Provider value={{ userData, updateUser }}>
      {children}
    </UserContext.Provider>
  );
}
