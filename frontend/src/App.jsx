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
import EmployeeJourneys from "./pages/employeeJourneys/EmployeeJourneys";
import OnBoardingFormPage from "./pages/onBoardingFormPage/OnBoardingFormPage";
import UpdateFormPage from "./pages/onBoardingFormPage/updateFormPage/UpdateFormPage";
import OffBoardingFormPage from "./pages/offBoardingFormPage/OffBoardingFormPage";
import UpdateOffBoardingFormPage from "./pages/offBoardingFormPage/updateFormPage/UpdateOffBoardingFormPage";

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    setIsAuthenticated(!!token);
  }, []);
  
  if (isAuthenticated === null) {
    return <div>Loading...</div>; 
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
  
  return isAuthenticated ? <Navigate to="/user-panel" replace /> : children;
}

function AppContent() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(true);
  const location = useLocation();
  
  const showSidebar = location.pathname !== "/" && location.pathname !== "/login" && location.pathname !== "/reset-password" && location.pathname !== "/set-password" && location.pathname !== "/user-panel";

  return (
    <Box style={{ display: 'flex', height: '100vh' }}>
      {showSidebar && (
        <Sidebar 
          collapsed={sidebarCollapsed} 
          onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} 
        />
      )}
      
      <Box style={{ 
        flex: 1, 
        overflowY: 'auto',
        overflowX: 'hidden',
        height: '100vh',
        width: showSidebar ? (sidebarCollapsed ? 'calc(100vw - 55px)' : 'calc(100vw - 260px)') : '100vw',
        transition: 'width 0.3s ease'
      }}>
        <Routes>
          <Route path="/" element={<PublicRoute><LoginPage /></PublicRoute>} />
          <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/set-password" element={<SetPassword />} />
          <Route path="/enter-key" element={<EnterKey />} />
          <Route path="/user-panel" element={<ProtectedRoute><UserPanel /></ProtectedRoute>} />
          <Route path="/dashboard/employee-journeys" element={<EmployeeJourneys sidebarCollapsed={sidebarCollapsed} />} />
          <Route path="/onboarding-form" element={<ProtectedRoute><OnBoardingFormPage /></ProtectedRoute>} />
          <Route path="/onboarding-form/update/:templateId" element={<ProtectedRoute><UpdateFormPage /></ProtectedRoute>} />
          <Route path="/offboarding-form" element={<ProtectedRoute><OffBoardingFormPage /></ProtectedRoute>} />
          <Route path="/offboarding-form/update/:templateId" element={<ProtectedRoute><UpdateOffBoardingFormPage /></ProtectedRoute>} />
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
