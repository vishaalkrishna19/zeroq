import "@mantine/core/styles.css";
import { MantineProvider, Box } from "@mantine/core";
import { BrowserRouter as Router, Routes, Route, useLocation, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { theme } from "./theme";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/admin/Dashboard";
import { Sidebar } from "./components/sidebar/Sidebar";
import ResetPassword from "./pages/reset/ResetPassword";
import SetPassword from "./pages/set/SetPassword";
import EnterKey from "./pages/set/EnterKey";
import UserPanel from "./pages/user/UserPanel";

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  
  useEffect(() => {
    // Check authentication status (replace with your auth logic)
    const token = localStorage.getItem('authToken');
    setIsAuthenticated(!!token);
  }, []);
  
  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Or your loading component
  }
  
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function PublicRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    setIsAuthenticated(!!token);
  }, []);
  
  if (isAuthenticated === null) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? <Navigate to="/dashboard" replace /> : children;
}

function AppContent() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(true);
  const location = useLocation();
  
  const showSidebar = location.pathname !== "/" && location.pathname !== "/login" && location.pathname !== "/reset-password" && location.pathname !== "/set-password" && location.pathname !== "/enter-key";

  return (
    <Box style={{ display: 'flex', height: '100vh' }}>
      {showSidebar && (
        <Sidebar 
          collapsed={sidebarCollapsed} 
          onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} 
        />
      )}
      
      <Box style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<PublicRoute><LoginPage /></PublicRoute>} />
          <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/set-password" element={<SetPassword />} />
          <Route path="/enter-key" element={<EnterKey />} />
          <Route path="/user-panel" element={<ProtectedRoute><UserPanel /></ProtectedRoute>} />
        </Routes>
      </Box>
    </Box>
  );
}

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <Router>
        <AppContent />
      </Router>
    </MantineProvider>
  );
}
