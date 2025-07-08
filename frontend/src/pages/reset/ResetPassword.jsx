import React, { useState, useEffect } from "react";
import {
  Paper, PasswordInput, Button,
  Stack, Title, Text, Box, Image, Alert, Loader
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useNavigate, useLocation } from "react-router-dom";
import { IconCheck, IconX, IconInfoCircle } from "@tabler/icons-react";

const bgGradient = "#fff";
const cardRadius = 15;

// Helper to get CSRF token from cookie
const getCSRFToken = () => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
};

// API service for password reset
const resetPassword = async (username, currentPassword, newPassword) => {
  const csrfToken = getCSRFToken();
  const response = await fetch('http://localhost:8000/api/users/reset_password/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
    body: JSON.stringify({
      username: username,
      current_password: currentPassword,
      new_password: newPassword,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Password reset failed');
  }

  return response.json();
};

export default function ResetPassword() {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [showMessage, setShowMessage] = useState(false);

  // Check if user was redirected here due to must_reset_password
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const message = params.get('message');
    const fromLogin = params.get('from') === 'login';
    
    if (message || fromLogin) {
      setShowMessage(true);
    }
  }, [location]);

  const form = useForm({
    initialValues: { 
      currentPassword: "", 
      newPassword: "", 
      confirmPassword: "" 
    },
    validate: {
      currentPassword: (v) => (v.length >= 1 ? null : "Current password is required"),
      newPassword: (v) => (v.length >= 6 ? null : "Password must be ≥ 6 chars"),
      confirmPassword: (value, values) => 
        value !== values.newPassword ? "Passwords did not match" : null,
    },
  });

  const handleSubmit = async (values) => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    // Get username from session storage or prompt user
    const storedUsername = sessionStorage.getItem('resetUsername');
    
    if (!storedUsername) {
      setError("Session expired. Please log in again to reset your password.");
      setLoading(false);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
      return;
    }

    try {
      console.log("Resetting password for:", storedUsername);
      const result = await resetPassword(storedUsername, values.currentPassword, values.newPassword);
      
      console.log("Password reset successful:", result);
      setSuccess(true);
      
      // Clean up session storage
      sessionStorage.removeItem('resetUsername');
      sessionStorage.removeItem('resetCurrentPassword');
      
      setTimeout(() => {
        navigate('/login');
      }, 2000);
      
    } catch (err) {
      console.error("Password reset error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      style={{
        minHeight: "100vh",
        width: "100vw",
        background: bgGradient,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Paper
        shadow="xl"
        radius={cardRadius}
        p={0}
        style={{
          display: "flex",
          width: 900,
          minHeight: 520,
          overflow: "hidden",
          background: "#fff",
        }}
      >
        {/* Left: Image */}
        <Box
          style={{
            flex: 1,
            background: "#f3f4f6",
            position: "relative",
            borderTopLeftRadius: cardRadius,
            borderBottomLeftRadius: cardRadius,
            overflow: "hidden",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            minHeight: 520,
          }}
        >
          <Image
            src="/login-bg.jpeg"
            alt="Security"
            fit="cover"
            height="100%"
            width="100%"
            style={{
              objectFit: "cover",
              width: "100%",
              height: "100%",
              borderTopLeftRadius: cardRadius,
              borderBottomLeftRadius: cardRadius,
            }}
          />
          {/* Centered Logo Overlay */}
          <div style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "150px",
            height: "150px",
            borderRadius: "16px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}>
            <img 
              src="https://zeroq.hfapp.net/logo.svg" 
              width="120px" 
              height="120px" 
              alt="ZeroQ Logo" 
            />
          </div>
        </Box>

        {/* Right: Form */}
        <Box
          style={{
            flex: 1,
            padding: "48px 40px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            borderTopRightRadius: cardRadius,
            borderBottomRightRadius: cardRadius,
            background: "rgba(255,255,255,0.95)",
          }}
        >
          <Stack spacing={8} mb={32}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '12px', 
              marginBottom: '32px' 
            }}>
              <div style={{ 
                width: '40px', 
                height: '40px', 
                background: '#999', 
                borderRadius: '8px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <img src="https://zeroq.hfapp.net/logo.svg" width="24px" height="24px" alt="ZeroQ Logo" />
              </div>
              <Title order={3} size="h1" style={{ fontWeight: 400, color: "#222" }}>
                ZeroQ
              </Title>
            </div>
          </Stack>
          
          <Title order={2} mb={8} style={{ fontWeight: 500, color: "#222" }}>
            Reset your password
          </Title>
          <Text size="sm" color="dimmed" mb={24}>
            Enter your current password and choose a new one
          </Text>

          {showMessage && (
            <Alert icon={<IconInfoCircle size="1rem" />} color="blue" mb="md">
              You must reset your password before logging in to continue using the system.
            </Alert>
          )}

          {error && (
            <Alert icon={<IconX size="1rem" />} color="red" mb="md">
              {error}
            </Alert>
          )}

          {success && (
            <Alert icon={<IconCheck size="1rem" />} color="green" mb="md">
              Password reset successfully! Redirecting to login...
            </Alert>
          )}
          
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack spacing="md">
              <PasswordInput
                label="Current Password"
                placeholder="Enter your current password"
                required
                {...form.getInputProps("currentPassword")}
                radius="md"
                size="md"
                disabled={loading || success}
              />
              <PasswordInput
                label="New Password"
                placeholder="Enter your new password"
                required
                {...form.getInputProps("newPassword")}
                radius="md"
                size="md"
                disabled={loading || success}
              />
              <PasswordInput
                label="Confirm New Password"
                placeholder="Confirm your new password"
                required
                {...form.getInputProps("confirmPassword")}
                radius="md"
                size="md"
                disabled={loading || success}
              />
              <Button
                fullWidth
                radius="md"
                size="md"
                type="submit"
                disabled={loading || success}
                style={{
                  background: success ? "#51cf66" : "oklch(62.3% .214 259.815)",
                  color: "#fff",
                  fontWeight: 600,
                  marginTop: 8,
                  marginBottom: 8,
                }}
              >
                {loading ? (
                  <>
                    <Loader size="sm" mr="sm" />
                    Updating Password...
                  </>
                ) : success ? (
                  "Password Updated Successfully!"
                ) : (
                  "Update Password"
                )}
              </Button>
            </Stack>
          </form>
        </Box>
      </Paper>
    </Box>
  );
}
