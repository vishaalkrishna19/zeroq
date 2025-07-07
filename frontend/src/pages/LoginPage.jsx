import React from "react";
import {
  Paper, TextInput, PasswordInput, Button,
  Stack, Title, Anchor, Text, Group, Divider, Box, Image
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconBrandApple, IconBrandGoogle } from "@tabler/icons-react";

const bgGradient = "#fff";
const cardRadius = 15;

export default function LoginPage() {
  const form = useForm({
    initialValues: { email: "", password: "" },
    validate: {
      email: (v) => (/^\S+@\S+$/.test(v) ? null : "Invalid email"),
      password: (v) => (v.length >= 6 ? null : "Password must be ≥ 6 chars"),
    },
  });

  const handleSubmit = (values) => {
    console.log("Logging in:", values);

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
        // backgroundImage: 'url("/login-new.png")'
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
            Enter the credentials
          </Text>
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack spacing="md">
              <TextInput
                label="Email"
                placeholder="you@email.com"
                required
                {...form.getInputProps("email")}
                radius="md"
                size="md"
              />
              <PasswordInput
                label="Password"
                placeholder="Your password"
                required
                {...form.getInputProps("password")}
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
                Submit
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
