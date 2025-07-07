import "@mantine/core/styles.css";
import { MantineProvider, Box } from "@mantine/core";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { useState } from "react";
import { theme } from "./theme";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/admin/Dashboard";
import { Sidebar } from "./components/sidebar/Sidebar";
import ResetPassword from "./pages/reset/ResetPassword";
import SetPassword from "./pages/set/SetPassword";

function AppContent() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const location = useLocation();
  
  const showSidebar = location.pathname !== "/" && location.pathname !== "/login" && location.pathname !== "/reset-password" && location.pathname !== "/set-password";

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
          <Route path="/" element={<LoginPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/set-password" element={<SetPassword />} />
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
