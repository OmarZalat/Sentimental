import React, { useEffect } from "react";
import { Route, Routes } from "react-router-dom";
import { Helmet, HelmetProvider } from "react-helmet-async";
import "./App.css";
import Landing from "./pages/landing/landing";
import Journal from "./pages/journal/journal";
import UserProvider from "./userProvider";

function App() {
  useEffect(() => {
    document.title = "Sentimental";
  }, []);

  return (
    <HelmetProvider>
      <UserProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/journal" element={<Journal />} />
        </Routes>
      </UserProvider>
    </HelmetProvider>
  );
}

export default App;
