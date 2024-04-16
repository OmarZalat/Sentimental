import { Route, Routes } from "react-router-dom";
import "./App.css";
import Landing from "./pages/landing/landing";
import Journal from "./pages/journal/journal";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Landing />}></Route>
        <Route path="/journal" element={<Journal />}></Route>
      </Routes>
    </>
  );
}

export default App;
