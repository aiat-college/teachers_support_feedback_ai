import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Write from "./pages/Write";
import View from "./pages/View";
import ViewResult from "./pages/ViewResult";
import AdminLogin from "./pages/AdminLogin";
import CreateUser from "./pages/CreateUser";
import EditNote  from "./pages/EditNote";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/auth/login" element={<AdminLogin />} />
        <Route path="/users/create" element={<CreateUser />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/write" element={<Write />} />
        <Route path="/view" element={<View />} />
        <Route path="/view-result" element={<ViewResult />} />
        <Route path="/edit/:id" element={<EditNote />} />
      </Routes>
    </BrowserRouter>
  );
}
