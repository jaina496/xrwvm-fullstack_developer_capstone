import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Dealers from "./components/Dealers/Dealers";
import Register from "./components/Register/Register";
import DealerDetails from "./components/DealerDetails/DealerDetails";
import PostReview from "./components/Dealers/PostReview";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealer/:id" element={<DealerDetails />} />
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;
