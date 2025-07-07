import { createTheme } from "@mantine/core";

export const theme = createTheme({
    shadows: {
        md: '3px 8px 6px rgba(0,0,0,0.3)', // x-offset 3px, y-offset 8px
        // other sizes...
        xl: '0px 0px 8px rgba(0,0,0,0.1)', // x-offset 4px, y-offset 12px
      },
});
