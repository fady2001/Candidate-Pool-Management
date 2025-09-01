import { createTheme, alpha } from "@mui/material/styles";

const defaultTheme = createTheme();

const customShadows = [...defaultTheme.shadows];

export const brand = {
  50: "hsl(220, 100%, 97%)", // Very light navy
  100: "hsl(220, 80%, 94%)", // Light navy
  200: "hsl(220, 70%, 85%)", // Lighter navy
  300: "hsl(220, 60%, 70%)", // Medium light navy
  400: "hsl(220, 80%, 45%)", // EFG Medium navy
  500: "hsl(220, 90%, 35%)", // EFG Primary navy
  600: "hsl(220, 95%, 25%)", // EFG Dark navy
  700: "hsl(220, 100%, 18%)", // Very dark navy
  800: "hsl(220, 100%, 12%)", // Deep navy
  900: "hsl(220, 100%, 8%)", // Darkest navy
};

export const gold = {
  50: "hsl(45, 100%, 97%)", // Very light gold
  100: "hsl(45, 95%, 92%)", // Light gold
  200: "hsl(45, 90%, 80%)", // Lighter gold
  300: "hsl(45, 85%, 65%)", // Medium light gold
  400: "hsl(42, 88%, 55%)", // EFG Gold accent
  500: "hsl(42, 95%, 45%)", // Primary gold
  600: "hsl(42, 100%, 35%)", // Dark gold
  700: "hsl(42, 100%, 25%)", // Very dark gold
  800: "hsl(42, 100%, 18%)", // Deep gold
  900: "hsl(42, 100%, 12%)", // Darkest gold
};

export const gray = {
  50: "hsl(220, 15%, 97%)", // Very light gray with blue tint
  100: "hsl(220, 12%, 94%)", // Light gray
  200: "hsl(220, 10%, 88%)", // Lighter gray
  300: "hsl(220, 8%, 75%)", // Medium light gray
  400: "hsl(220, 6%, 60%)", // Medium gray
  500: "hsl(220, 8%, 45%)", // EFG Text gray
  600: "hsl(220, 10%, 35%)", // Dark gray
  700: "hsl(220, 15%, 25%)", // Very dark gray
  800: "hsl(220, 20%, 15%)", // Deep gray
  900: "hsl(220, 25%, 8%)", // Darkest gray
};

export const green = {
  50: "hsl(120, 80%, 98%)",
  100: "hsl(120, 75%, 94%)",
  200: "hsl(120, 75%, 87%)",
  300: "hsl(120, 61%, 77%)",
  400: "hsl(120, 44%, 53%)",
  500: "hsl(120, 59%, 30%)",
  600: "hsl(120, 70%, 25%)",
  700: "hsl(120, 75%, 16%)",
  800: "hsl(120, 84%, 10%)",
  900: "hsl(120, 87%, 6%)",
};

export const orange = {
  50: "hsl(42, 100%, 97%)", // Use gold tones instead of orange
  100: "hsl(42, 95%, 90%)",
  200: "hsl(42, 90%, 80%)",
  300: "hsl(42, 85%, 65%)",
  400: "hsl(42, 88%, 55%)", // EFG Gold
  500: "hsl(42, 95%, 45%)",
  600: "hsl(42, 100%, 35%)",
  700: "hsl(42, 100%, 25%)",
  800: "hsl(42, 100%, 18%)",
  900: "hsl(42, 100%, 12%)",
};

export const red = {
  50: "hsl(0, 100%, 97%)",
  100: "hsl(0, 92%, 90%)",
  200: "hsl(0, 94%, 80%)",
  300: "hsl(0, 90%, 65%)",
  400: "hsl(0, 90%, 40%)",
  500: "hsl(0, 90%, 30%)",
  600: "hsl(0, 91%, 25%)",
  700: "hsl(0, 94%, 18%)",
  800: "hsl(0, 95%, 12%)",
  900: "hsl(0, 93%, 6%)",
};

export const getDesignTokens = (mode) => {
  customShadows[1] =
    mode === "dark"
      ? "hsla(220, 30%, 5%, 0.7) 0px 4px 16px 0px, hsla(220, 25%, 10%, 0.8) 0px 8px 16px -5px"
      : "hsla(220, 30%, 5%, 0.07) 0px 4px 16px 0px, hsla(220, 25%, 10%, 0.07) 0px 8px 16px -5px";

  return {
    palette: {
      mode,
      primary: {
        light: brand[300],
        main: brand[500], // EFG Primary navy
        dark: brand[700],
        contrastText: "#ffffff",
        ...(mode === "dark" && {
          contrastText: brand[50],
          light: brand[400],
          main: brand[500],
          dark: brand[800],
        }),
      },
      secondary: {
        light: gold[300],
        main: gold[400], // EFG Gold accent
        dark: gold[600],
        contrastText: brand[800],
        ...(mode === "dark" && {
          contrastText: brand[100],
          light: gold[400],
          main: gold[500],
          dark: gold[700],
        }),
      },
      info: {
        light: brand[200],
        main: brand[400],
        dark: brand[600],
        contrastText: gray[50],
        ...(mode === "dark" && {
          contrastText: brand[300],
          light: brand[500],
          main: brand[600],
          dark: brand[800],
        }),
      },
      warning: {
        light: gold[300], // Use gold instead of orange
        main: gold[400],
        dark: gold[700],
        ...(mode === "dark" && {
          light: gold[400],
          main: gold[500],
          dark: gold[700],
        }),
      },
      error: {
        light: red[300],
        main: red[400],
        dark: red[800],
        ...(mode === "dark" && {
          light: red[400],
          main: red[500],
          dark: red[700],
        }),
      },
      success: {
        light: green[300],
        main: green[400],
        dark: green[800],
        ...(mode === "dark" && {
          light: green[400],
          main: green[500],
          dark: green[700],
        }),
      },
      grey: {
        ...gray,
      },
      divider: mode === "dark" ? alpha(gray[700], 0.6) : alpha(gray[300], 0.4),
      background: {
        default: "hsl(220, 15%, 99%)", // Very light blue-gray
        paper: "hsl(220, 15%, 97%)", // Light blue-gray
        ...(mode === "dark" && {
          default: gray[900],
          paper: "hsl(220, 20%, 8%)",
        }),
      },
      text: {
        primary: brand[800], // Dark navy for text
        secondary: gray[600],
        warning: gold[500], // Gold for warnings
        ...(mode === "dark" && {
          primary: "hsl(0, 0%, 100%)",
          secondary: gray[400],
        }),
      },
      action: {
        hover: alpha(brand[100], 0.3), // Light navy hover
        selected: `${alpha(brand[200], 0.4)}`,
        ...(mode === "dark" && {
          hover: alpha(gray[600], 0.2),
          selected: alpha(gray[600], 0.3),
        }),
      },
    },
    typography: {
      fontFamily: "Inter, sans-serif",
      h1: {
        fontSize: defaultTheme.typography.pxToRem(48),
        fontWeight: 600,
        lineHeight: 1.2,
        letterSpacing: -0.5,
      },
      h2: {
        fontSize: defaultTheme.typography.pxToRem(36),
        fontWeight: 600,
        lineHeight: 1.2,
      },
      h3: {
        fontSize: defaultTheme.typography.pxToRem(30),
        lineHeight: 1.2,
      },
      h4: {
        fontSize: defaultTheme.typography.pxToRem(24),
        fontWeight: 600,
        lineHeight: 1.5,
      },
      h5: {
        fontSize: defaultTheme.typography.pxToRem(20),
        fontWeight: 600,
      },
      h6: {
        fontSize: defaultTheme.typography.pxToRem(18),
        fontWeight: 600,
      },
      subtitle1: {
        fontSize: defaultTheme.typography.pxToRem(18),
      },
      subtitle2: {
        fontSize: defaultTheme.typography.pxToRem(14),
        fontWeight: 500,
      },
      body1: {
        fontSize: defaultTheme.typography.pxToRem(14),
      },
      body2: {
        fontSize: defaultTheme.typography.pxToRem(14),
        fontWeight: 400,
      },
      caption: {
        fontSize: defaultTheme.typography.pxToRem(12),
        fontWeight: 400,
      },
    },
    shape: {
      borderRadius: 8,
    },
    shadows: customShadows,
  };
};

export const colorSchemes = {
  light: {
    palette: {
      primary: {
        light: brand[300],
        main: brand[500],
        dark: brand[700],
        contrastText: "#ffffff",
      },
      secondary: {
        light: gold[300],
        main: gold[400],
        dark: gold[600],
        contrastText: brand[800],
      },
      info: {
        light: brand[200],
        main: brand[400],
        dark: brand[600],
        contrastText: gray[50],
      },
      warning: {
        light: gold[300],
        main: gold[400],
        dark: gold[700],
      },
      error: {
        light: red[300],
        main: red[400],
        dark: red[800],
      },
      success: {
        light: green[300],
        main: green[400],
        dark: green[800],
      },
      grey: {
        ...gray,
      },
      divider: alpha(gray[300], 0.4),
      background: {
        default: "hsl(220, 15%, 99%)",
        paper: "hsl(220, 15%, 97%)",
      },
      text: {
        primary: brand[800],
        secondary: gray[600],
        warning: gold[500],
      },
      action: {
        hover: alpha(brand[100], 0.3),
        selected: `${alpha(brand[200], 0.4)}`,
      },
      baseShadow:
        "hsla(220, 30%, 5%, 0.07) 0px 4px 16px 0px, hsla(220, 25%, 10%, 0.07) 0px 8px 16px -5px",
    },
  },
  dark: {
    palette: {
      primary: {
        contrastText: brand[50],
        light: brand[400],
        main: brand[500],
        dark: brand[800],
      },
      secondary: {
        contrastText: brand[100],
        light: gold[400],
        main: gold[500],
        dark: gold[700],
      },
      info: {
        contrastText: brand[300],
        light: brand[500],
        main: brand[600],
        dark: brand[800],
      },
      warning: {
        light: gold[400],
        main: gold[500],
        dark: gold[700],
      },
      error: {
        light: red[400],
        main: red[500],
        dark: red[700],
      },
      success: {
        light: green[400],
        main: green[500],
        dark: green[700],
      },
      grey: {
        ...gray,
      },
      divider: alpha(gray[700], 0.6),
      background: {
        default: gray[900],
        paper: "hsl(220, 20%, 8%)",
      },
      text: {
        primary: "hsl(0, 0%, 100%)",
        secondary: gray[400],
      },
      action: {
        hover: alpha(gray[600], 0.2),
        selected: alpha(gray[600], 0.3),
      },
      baseShadow:
        "hsla(220, 30%, 5%, 0.7) 0px 4px 16px 0px, hsla(220, 25%, 10%, 0.8) 0px 8px 16px -5px",
    },
  },
};

export const typography = {
  fontFamily: "Inter, sans-serif",
  h1: {
    fontSize: defaultTheme.typography.pxToRem(48),
    fontWeight: 600,
    lineHeight: 1.2,
    letterSpacing: -0.5,
  },
  h2: {
    fontSize: defaultTheme.typography.pxToRem(36),
    fontWeight: 600,
    lineHeight: 1.2,
  },
  h3: {
    fontSize: defaultTheme.typography.pxToRem(30),
    lineHeight: 1.2,
  },
  h4: {
    fontSize: defaultTheme.typography.pxToRem(24),
    fontWeight: 600,
    lineHeight: 1.5,
  },
  h5: {
    fontSize: defaultTheme.typography.pxToRem(20),
    fontWeight: 600,
  },
  h6: {
    fontSize: defaultTheme.typography.pxToRem(18),
    fontWeight: 600,
  },
  subtitle1: {
    fontSize: defaultTheme.typography.pxToRem(18),
  },
  subtitle2: {
    fontSize: defaultTheme.typography.pxToRem(14),
    fontWeight: 500,
  },
  body1: {
    fontSize: defaultTheme.typography.pxToRem(14),
  },
  body2: {
    fontSize: defaultTheme.typography.pxToRem(14),
    fontWeight: 400,
  },
  caption: {
    fontSize: defaultTheme.typography.pxToRem(12),
    fontWeight: 400,
  },
};

export const shape = {
  borderRadius: 8,
};

const defaultShadows = [
  "none",
  "var(--template-palette-baseShadow)",
  ...defaultTheme.shadows.slice(2),
];

export const shadows = defaultShadows;
