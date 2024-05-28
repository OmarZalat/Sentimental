import React, { useEffect } from "react";
import { Route, Routes } from "react-router-dom";
import { Helmet, HelmetProvider } from "react-helmet-async";
import "./App.css";
import Landing from "./pages/landing/landing";
import Journal from "./pages/journal/journal";
import UserProvider from "./userProvider";
import Dashboard from "./pages/dashboard/dashboard";

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
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </UserProvider>
    </HelmetProvider>
  );
}

export default App;
