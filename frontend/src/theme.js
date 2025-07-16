import { createTheme } from "@mantine/core";

export const theme = createTheme({

  spacing: {
    xs: "4px",    
    sm: "8px",   
    md: "16px",   
    lg: "24px",  
    xl: "32px",  
    xxl: "40px",  
    xxxl: "48px", 
  },
  

  components: {
    Container: {
      defaultProps: {
        padding: "md",
      },
    },
    Stack: {
      defaultProps: {
        gap: "md",
      },
    },
    Group: {
      defaultProps: {
        gap: "md",
      },
    },
  },
  
  other: {
    spacing: {
      xs: "4px",
      sm: "8px", 
      md: "16px",
      lg: "24px",
      xl: "32px",
      xxl: "40px",
      xxxl: "48px",
    },
    
    component: {
      padding: {
        xs: "8px",
        sm: "16px",
        md: "24px",
        lg: "32px",
        xl: "48px",
      },
      margin: {
        xs: "4px",
        sm: "8px",
        md: "16px",
        lg: "24px",
        xl: "32px",
      },
      gap: {
        xs: "4px",
        sm: "8px",
        md: "16px",
        lg: "24px",
        xl: "32px",
      },
    },
  },
});


