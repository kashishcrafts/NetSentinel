import { Route, Routes, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Threats from "./pages/Threats";
import Alerts from "./pages/Alerts";
import Reports from "./pages/Reports";
import Analytics from "./pages/Analytics";
import Incidents from "./pages/Incidents";
import IOCCenter from "./pages/IOCCenter";
import MITRECenter from "./pages/MITRECenter";
import ThreatHunting from "./pages/ThreatHunting";
import UserManagement from "./pages/UserManagement";
import AuditLogs from "./pages/AuditLogs";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

function App() {
  const location = useLocation();
  const isLoginRoute = location.pathname === "/login";

  return (
    <div className="min-h-screen bg-cyber-900 text-slate-100">
      <div className="flex flex-col lg:flex-row">
        {!isLoginRoute && <Sidebar />}
        <div className="flex-1">
          {!isLoginRoute && <Navbar />}
          <main className="p-4 lg:p-6">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/threats" element={<ProtectedRoute><Threats /></ProtectedRoute>} />
              <Route path="/alerts" element={<ProtectedRoute><Alerts /></ProtectedRoute>} />
              <Route path="/incidents" element={<ProtectedRoute><Incidents /></ProtectedRoute>} />
              <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
              <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
              <Route path="/threat-intelligence" element={<ProtectedRoute><Threats /></ProtectedRoute>} />
              <Route path="/ioc-center" element={<ProtectedRoute><IOCCenter /></ProtectedRoute>} />
              <Route path="/threat-hunting" element={<ProtectedRoute><ThreatHunting /></ProtectedRoute>} />
              <Route path="/mitre" element={<ProtectedRoute><MITRECenter /></ProtectedRoute>} />
              <Route path="/audit-logs" element={<ProtectedRoute><AuditLogs /></ProtectedRoute>} />
              <Route path="/users" element={<ProtectedRoute><UserManagement /></ProtectedRoute>} />
              <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
