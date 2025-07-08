import React, { useState } from "react";
import {
  Paper, TextInput, PasswordInput, Button,
  Stack, Title, Anchor, Text, Group, Divider, Box, Image,
  Alert, Loader
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconBrandApple, IconBrandGoogle, IconCheck, IconX } from "@tabler/icons-react";
import { useNavigate } from "react-router-dom";

const bgGradient = "#fff";
const cardRadius = 15;

// Helper to get CSRF token from cookie
const getCSRFToken = () => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
};

// API service for credential verification using Django's built-in login
const verifyCredentials = async (username, currentPassword) => {
  const csrfToken = getCSRFToken();
  const response = await fetch('http://localhost:8000/api/users/verify_credentials/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
    body: JSON.stringify({
      username: username,
      password: currentPassword,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || error.detail || 'Invalid username or password');
  }

  return response.json();
};

export default function EnterKey() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const form = useForm({
    initialValues: { 
      username: "",
      current_password: ""
    },
    validate: {
      username: (v) => (v.length >= 1 ? null : "Username is required"),
      current_password: (v) => (v.length >= 1 ? null : "Current password is required"),
    },
  });

  const handleSubmit = async (values) => {
    setLoading(true);
    setError(null);

    try {
      console.log("Verifying credentials:", values.username);
      const result = await verifyCredentials(values.username, values.current_password);
      
      console.log("Credentials verified successfully:", result);
      
      // Store username in sessionStorage for the next page
      sessionStorage.setItem('resetUsername', values.username);
      sessionStorage.setItem('resetCurrentPassword', values.current_password);
      
      // Redirect to set password page
      navigate('/set-password');
      
    } catch (err) {
      console.error("Credential verification error:", err);
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
        <Box
          style={{
            flex: 1,
            padding: "48px 40px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            borderTopLeftRadius: cardRadius,
            borderBottomLeftRadius: cardRadius,
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
            Verify Your Identity
          </Title>
          <Text size="sm" color="dimmed" mb={24}>
            Enter your username and current password to continue
          </Text>

          {error && (
            <Alert icon={<IconX size="1rem" />} color="red" mb="md">
              {error}
            </Alert>
          )}

          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack spacing="md">
              <TextInput
                label="Username"
                placeholder="Enter your username"
                required
                {...form.getInputProps("username")}
                radius="md"
                size="md"
                disabled={loading}
              />
              <PasswordInput
                label="Current Password"
                placeholder="Enter your current password"
                required
                {...form.getInputProps("current_password")}
                radius="md"
                size="md"
                disabled={loading}
              />
              <Button
                fullWidth
                radius="md"
                size="md"
                type="submit"
                disabled={loading}
                style={{
                  background: "oklch(62.3% .214 259.815)",
                  color: "#fff",
                  fontWeight: 600,
                  marginTop: 8,
                  marginBottom: 8,
                }}
              >
                {loading ? (
                  <>
                    <Loader size="sm" mr="sm" />
                    Verifying...
                  </>
                ) : (
                  "Continue"
                )}
              </Button>
            </Stack>
          </form>

          <Group position="center" mt="md" style={{ fontSize: 13 }}>
            <Anchor component="button" type="button" color="gray" onClick={() => navigate('/login')}>
              Back to Login
            </Anchor>
          </Group>
        </Box>

        {/* Right: Image */}
        <Box
          style={{
            flex: 1,
            background: "#f3f4f6",
            position: "relative",
            borderTopRightRadius: cardRadius,
            borderBottomRightRadius: cardRadius,
            overflow: "hidden",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            minHeight: 520,
          }}
        >
          <Image
            src="/login-bg.jpeg"
            alt="Meeting"
            fit="cover"
            height="100%"
            width="100%"
            style={{
              objectFit: "cover",
              width: "100%",
              height: "100%",
              borderTopRightRadius: cardRadius,
              borderBottomRightRadius: cardRadius,
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
      </Paper>
    </Box>
  );
}
