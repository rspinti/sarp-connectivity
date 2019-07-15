const breakpoints = ['40em', '52em', '64em']

const colors = {
  white: '#FFF',
  black: '#000',
  link: '#1891ac',
  primary: {
    100: '#e0f2fb',
    200: '#cce5f2',
    // 0: '#e4f0f9',
    // 100: '#c6e1f3',
    // 200: '#a5cfed',
    // 300: '#7db9e5',
    // 400: '#4a9eda',
    // 500: '#0077cc',
    // 600: '#006bb7',
    // 700: '#005da0',
    // 800: '#004d84',
    // 900: '#00365d',
    500: '#1891ac',
    800: '#1f5f8b',
    900: '#253b6e',
  },
  secondary: {
    500: '#1891ac',
    600: '#147b92',
    // 0: '#e3f9f7',
    // 100: '#c4f3ef',
    // 200: '#a0ece5',
    // 300: '#77e3da',
    // 400: '#44d9cd',
    // 500: '#00ccbb',
    // 600: '#00b8a9',
    // 700: '#00a294',
    // 800: '#00867b',
    // 900: '#006159',
  },
  highlight: {
    // 0: '#faeaeb',
    // 100: '#f6d2d5',
    // 200: '#f0b7bc',
    // 300: '#ea969d',
    // 400: '#e16973',
    500: 'orange',
    // 600: '#b8000f',
    // 700: '#a2000d',
    // 800: '#86000b',
    // 900: '#610008',
  },
  grey: {
    0: '#f8f9f9',
    100: '#ebedee',
    200: '#dee1e3',
    300: '#cfd3d6',
    400: '#bec4c8',
    500: '#acb4b9',
    600: '#97a1a7',
    700: '#7f8a93',
    800: '#5f6e78',
    900: '#374047',
  },
}

const buttons = {
  default: {
    type: 'button',
    backgroundColor: colors.grey[900],
  },
  primary: {
    backgroundColor: colors.primary[500],
  },
  secondary: {
    backgroundColor: colors.secondary[500],
  },
  warning: {
    backgroundColor: '#ea1b00',
  },
  disabled: {
    backgroundColor: colors.grey[300],
  },
}

const theme = {
  breakpoints,
  colors,
  buttons,
}

export default theme
