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
      
      navigate('/user-panel');
      
    } catch (err) {
      console.error("Login error:", err);
      
      // Check if this is a must_reset_password error
      if (err.mustResetPassword) {
        // Store username and password for the reset flow
        sessionStorage.setItem('resetUsername', values.username);
        sessionStorage.setItem('resetCurrentPassword', values.password);
        navigate('/set-password');
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
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 563 563" fill="none">
                  <rect width="563" height="563" rx="144" fill="white" fillOpacity="0.1"/>
                  <rect x="2" y="2" width="559" height="559" rx="142" stroke="white" strokeOpacity="0.1" strokeWidth="4"/>
                  <path d="M295.849 99.0146C395.827 100.281 476.483 181.721 476.483 282V294L476.469 296.365C476.015 332.209 465.254 365.567 447.016 393.616L499.739 441.364C513.657 453.969 514.723 475.471 502.118 489.39C489.513 503.308 468.012 504.373 454.094 491.768L307.159 358.701C293.241 346.096 292.177 324.595 304.781 310.677C317.386 296.759 338.887 295.693 352.806 308.298L395.558 347.016C403.815 331.151 408.483 313.121 408.483 294V282C408.483 218.487 356.996 167 293.483 167H269.483C252.313 167 236.022 170.765 221.389 177.512L168.611 129.29C196.919 110.554 230.739 99.4753 267.118 99.0146L269.483 98.9999H293.483L295.849 99.0146ZM170.615 223.23C160.37 240.429 154.483 260.527 154.483 282V294C154.483 355.207 202.3 405.244 262.616 408.796L332.659 472.794C320.779 475.385 308.468 476.825 295.849 476.985L293.483 477H269.483L267.118 476.985C167.927 475.729 87.7544 395.556 86.4979 296.365L86.4833 294V282C86.4833 242.825 98.7921 206.526 119.754 176.758L170.615 223.23ZM62.5565 74.3661C75.4049 61.0779 96.4626 60.5195 109.994 72.955L110.633 73.5565L130.132 92.4101L130.755 93.0282C143.639 106.133 143.79 127.198 130.941 140.486C118.093 153.775 97.0352 154.334 83.5038 141.898L82.8651 141.296L63.3671 122.443L62.744 121.825C49.8594 108.72 49.7082 87.6548 62.5565 74.3661Z" fill="white"/>
                </svg>
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
            <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 563 563" fill="none">
              <rect width="563" height="563" rx="144" fill="white" fillOpacity="0.1"/>
              <rect x="2" y="2" width="559" height="559" rx="142" stroke="white" strokeOpacity="0.1" strokeWidth="4"/>
              <path d="M295.849 99.0146C395.827 100.281 476.483 181.721 476.483 282V294L476.469 296.365C476.015 332.209 465.254 365.567 447.016 393.616L499.739 441.364C513.657 453.969 514.723 475.471 502.118 489.39C489.513 503.308 468.012 504.373 454.094 491.768L307.159 358.701C293.241 346.096 292.177 324.595 304.781 310.677C317.386 296.759 338.887 295.693 352.806 308.298L395.558 347.016C403.815 331.151 408.483 313.121 408.483 294V282C408.483 218.487 356.996 167 293.483 167H269.483C252.313 167 236.022 170.765 221.389 177.512L168.611 129.29C196.919 110.554 230.739 99.4753 267.118 99.0146L269.483 98.9999H293.483L295.849 99.0146ZM170.615 223.23C160.37 240.429 154.483 260.527 154.483 282V294C154.483 355.207 202.3 405.244 262.616 408.796L332.659 472.794C320.779 475.385 308.468 476.825 295.849 476.985L293.483 477H269.483L267.118 476.985C167.927 475.729 87.7544 395.556 86.4979 296.365L86.4833 294V282C86.4833 242.825 98.7921 206.526 119.754 176.758L170.615 223.23ZM62.5565 74.3661C75.4049 61.0779 96.4626 60.5195 109.994 72.955L110.633 73.5565L130.132 92.4101L130.755 93.0282C143.639 106.133 143.79 127.198 130.941 140.486C118.093 153.775 97.0352 154.334 83.5038 141.898L82.8651 141.296L63.3671 122.443L62.744 121.825C49.8594 108.72 49.7082 87.6548 62.5565 74.3661Z" fill="white"/>
            </svg>
          </div>
        </Box>
      </Paper>
    </Box>
  );
}
