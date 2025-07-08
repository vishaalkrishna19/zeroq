import React, { useState } from "react";
import {
  Paper, TextInput, PasswordInput, Button,
  Stack, Title, Anchor, Text, Group, Divider, Box, Image,
  Alert, Loader
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconBrandApple, IconBrandGoogle, IconX } from "@tabler/icons-react";
import { useNavigate } from "react-router-dom";

const bgGradient = "#fff";
const cardRadius = 15;

const getCSRFToken = async () => {
  // Try to get from cookie first
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) return match[1];

  // If not found, fetch from API and try again
  await fetch('http://localhost:8000/api/auth/csrf/', {
    method: 'GET',
    credentials: 'include',
  });
  const newMatch = document.cookie.match(/csrftoken=([^;]+)/);
  return newMatch ? newMatch[1] : '';
};

const loginUser = async (username, password) => {
  try {
    const csrfToken = await getCSRFToken();
    console.log("CSRF Token:", csrfToken);
    const response = await fetch('http://localhost:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      credentials: 'include',
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      
      // Check if this is a must_reset_password error (403 status)
      if (response.status === 403 && error.must_reset_password) {
        const resetError = new Error(error.error || 'You must change your password before logging in.');
        resetError.mustResetPassword = true;
        resetError.redirectUrl = error.redirect_url;
        throw resetError;
      }
      
      // Regular login error
      throw new Error(error.non_field_errors?.[0] || error.detail || error.error || 'Login failed');
    }

    return response.json();
  } catch (error) {
    console.error('Login request failed:', error);
    throw error;
  }
};

export default function LoginPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const form = useForm({
    initialValues: { username: "", password: "" },
    validate: {
      username: (v) => (v.length >= 1 ? null : "Username is required"),
      password: (v) => (v.length >= 1 ? null : "Password is required"),
    },
  });

  const handleSubmit = async (values) => {
    setLoading(true);
    setError(null);

    try {
      console.log("Logging in:", values);
      const result = await loginUser(values.username, values.password);
      
      console.log("Login successful:", result);
      
      if (result.key || result.token) {
        localStorage.setItem('authToken', result.key || result.token);
      }
      
      localStorage.setItem('username', values.username);
      
      navigate('/dashboard');
      
    } catch (err) {
      console.error("Login error:", err);
      
      // Check if this is a must_reset_password error
      if (err.mustResetPassword) {
        // Store username and password for the reset flow
        sessionStorage.setItem('resetUsername', values.username);
        sessionStorage.setItem('resetCurrentPassword', values.password);
        navigate('/enter-key');
        return;
      }
      
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
            Sign in to your account
          </Title>
          <Text size="sm" color="dimmed" mb={24}>
            Enter your credentials
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
                label="Password"
                placeholder="Your password"
                required
                {...form.getInputProps("password")}
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
                    Signing In...
                  </>
                ) : (
                  "Sign In"
                )}
              </Button>
            </Stack>
          </form>

          <Group position="center" mt="md" style={{ fontSize: 13 }}>
            <Anchor component="button" type="button" color="gray">
              Terms & Conditions
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
