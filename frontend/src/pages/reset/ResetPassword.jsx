import React from "react";
import {
  Paper, PasswordInput, Button,
  Stack, Title, Text, Box, Image
} from "@mantine/core";
import { useForm } from "@mantine/form";

const bgGradient = "#fff";
const cardRadius = 15;

export default function ResetPassword() {
  const form = useForm({
    initialValues: { 
      currentPassword: "", 
      newPassword: "", 
      confirmPassword: "" 
    },
    validate: {
      currentPassword: (v) => (v.length >= 6 ? null : "Current password is required"),
      newPassword: (v) => (v.length >= 6 ? null : "Password must be ≥ 6 chars"),
      confirmPassword: (value, values) => 
        value !== values.newPassword ? "Passwords did not match" : null,
    },
  });

  const handleSubmit = (values) => {
    console.log("Resetting password:", values);
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
          
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack spacing="md">
              <PasswordInput
                label="Current Password"
                placeholder="Enter your current password"
                required
                {...form.getInputProps("currentPassword")}
                radius="md"
                size="md"
              />
              <PasswordInput
                label="New Password"
                placeholder="Enter your new password"
                required
                {...form.getInputProps("newPassword")}
                radius="md"
                size="md"
              />
              <PasswordInput
                label="Confirm New Password"
                placeholder="Confirm your new password"
                required
                {...form.getInputProps("confirmPassword")}
                radius="md"
                size="md"
              />
              <Button
                fullWidth
                radius="md"
                size="md"
                type="submit"
                style={{
                  background: "oklch(62.3% .214 259.815)",
                  color: "#fff",
                  fontWeight: 600,
                  marginTop: 8,
                  marginBottom: 8,
                }}
              >
                Update Password
              </Button>
            </Stack>
          </form>
        </Box>
      </Paper>
    </Box>
  );
}
