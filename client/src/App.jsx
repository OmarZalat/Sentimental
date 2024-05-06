import { Route, Routes } from "react-router-dom";
import "./App.css";
import Landing from "./pages/landing/landing";
import Journal from "./pages/journal/journal";
import UserProvider from "./userProvider";

function App() {
  return (
    <>
      <UserProvider>
        <Routes>
          <Route path="/" element={<Landing />}></Route>
          <Route path="/journal" element={<Journal />}></Route>
        </Routes>
      </UserProvider>
    </>
  );
}

export default App;
