
import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Dealers from "./components/Dealers/Dealers";
import Register from "./components/Register/Register";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
