import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Write from "./pages/Write";
import View from "./pages/View";
import ViewResult from "./pages/ViewResult";
import EditNote from "./pages/EditNote"; // ✅ ADD

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/write" element={<Write />} />
        <Route path="/view" element={<View />} />
        <Route path="/view-result" element={<ViewResult />} />

        {/* ✅ EDIT ROUTE */}
        <Route path="/edit/:id" element={<EditNote />} />

      </Routes>
    </BrowserRouter>
  );
}
