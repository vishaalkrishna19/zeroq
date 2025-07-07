import "@mantine/core/styles.css";
import { MantineProvider } from "@mantine/core";
import { theme } from "./theme";
import LoginPage from "./pages/LoginPage";

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <LoginPage />
    </MantineProvider>
  );
}
