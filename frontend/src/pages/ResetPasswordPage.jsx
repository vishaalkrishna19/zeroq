import React, { useState } from "react";
import {
  Paper, PasswordInput, Button,
  Stack, Title, Text, Box, Image, Alert, TextInput
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconCheck, IconX } from "@tabler/icons-react";

const bgGradient = "#fff";
const cardRadius = 15;

export default function ResetPasswordPage() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const form = useForm({
    initialValues: { 
      username: "",
      current_password: "",
      new_password: "",
      confirm_password: ""
    },
    validate: {
      username: (v) => (v.length > 0 ? null : "Username is required"),
      current_password: (v) => (v.length > 0 ? null : "Current password is required"),
      new_password: (v) => (v.length >= 8 ? null : "Password must be at least 8 characters"),
      confirm_password: (value, values) => 
        value !== values.new_password ? "Passwords do not match" : null,
    },
  });

  const handleSubmit = async (values) => {
    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      // First, login to get the token
      const loginResponse = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: values.username,
          password: values.current_password
        })
      });

      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        throw new Error(loginData.message || 'Login failed');
      }

      // If login successful, proceed with password change
      const token = loginData.token;
      const userId = loginData.user.id;

      const resetResponse = await fetch(`http://127.0.0.1:8000/api/users/${userId}/change_password/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
          current_password: values.current_password,
          new_password: values.new_password
        })
      });

      const resetData = await resetResponse.json();

      if (!resetResponse.ok) {
        throw new Error(resetData.error || 'Password reset failed');
      }

      setSuccess(true);
      form.reset();
    } catch (err) {
      setError(err.message || 'An error occurred');
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
            Reset Your Password
          </Title>
          <Text size="sm" color="dimmed" mb={24}>
            Enter your current password and new password
          </Text>

          {success && (
            <Alert icon={<IconCheck size="1rem" />} title="Success!" color="green" mb="md">
              Your password has been reset successfully! You can now use your new password to login.
            </Alert>
          )}

          {error && (
            <Alert icon={<IconX size="1rem" />} title="Error" color="red" mb="md">
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
              />
              <PasswordInput
                label="Current Password"
                placeholder="Enter your current password"
                required
                {...form.getInputProps("current_password")}
                radius="md"
                size="md"
              />
              <PasswordInput
                label="New Password"
                placeholder="Enter your new password"
                required
                {...form.getInputProps("new_password")}
                radius="md"
                size="md"
              />
              <PasswordInput
                label="Confirm New Password"
                placeholder="Confirm your new password"
                required
                {...form.getInputProps("confirm_password")}
                radius="md"
                size="md"
              />
              <Button
                fullWidth
                radius="md"
                size="md"
                type="submit"
                loading={loading}
                style={{
                  background: "oklch(62.3% .214 259.815)",
                  color: "#fff",
                  fontWeight: 600,
                  marginTop: 8,
                  marginBottom: 8,
                }}
              >
                Reset Password
              </Button>
            </Stack>
          </form>
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
