import React, { useState } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Alert,
  Stack,
  Stepper,
  Step,
  StepLabel,
  Grid,
  Divider,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  AccountBalance,
  TrendingUp,
  AttachMoney,
  Payment,
  CreditCard,
  Timeline,
  CheckCircle,
  Warning,
  Schedule,
  TrendingDown,
  SaveAlt,
  School,
  Home,
} from '@mui/icons-material';
import axios from 'axios';
import { motion } from 'framer-motion';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
    success: {
      main: '#4caf50',
    },
    warning: {
      main: '#ff9800',
    },
    error: {
      main: '#f44336',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          padding: '12px 24px',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
});

const CreditScoreIndicator = ({ score, improvements }) => {
  const getColor = (score) => {
    if (score >= 700) return theme.palette.success.main;
    if (score >= 500) return theme.palette.warning.main;
    return theme.palette.error.main;
  };

  return (
    <Box sx={{ textAlign: 'center', mt: 4 }}>
      <Box sx={{ position: 'relative', display: 'inline-flex', mb: 4 }}>
        <CircularProgress
          variant="determinate"
          value={(score - 300) / (850 - 300) * 100}
          size={200}
          thickness={4}
          sx={{ color: getColor(score) }}
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column'
          }}
        >
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: getColor(score) }}>
            {score}
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            Credit Score
          </Typography>
        </Box>
      </Box>

      {improvements && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Improvement Recommendations
            </Typography>
          </Grid>
          {improvements.map((improvement, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  {improvement.timeframe}
                </Typography>
                <Typography variant="h6" gutterBottom>
                  {improvement.action}
                </Typography>
                <Chip
                  label={`Impact: ${improvement.impact}`}
                  color="success"
                  size="small"
                  sx={{ mb: 2 }}
                />
                <List dense>
                  {improvement.steps.map((step, stepIndex) => (
                    <ListItem key={stepIndex}>
                      <ListItemIcon>
                        <CheckCircle color="primary" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={step} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

function App() {
  const [userData, setUserData] = useState({
    // Current Financial Status
    monthly_income: '',
    monthly_expenses: '',
    total_debt: '',
    savings: '',
    
    // Credit History
    on_time_payments: '',
    late_payments: '',
    missed_payments: '',
    
    // Credit Utilization
    credit_limit: '',
    current_balance: '',
    
    // Debt Types
    credit_card_debt: '',
    personal_loan: '',
    student_loan: '',
    mortgage: '',
  });

  const [score, setScore] = useState(null);
  const [improvements, setImprovements] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  const steps = ['Financial Status', 'Credit History', 'Credit Usage', 'Debt Details'];

  const handleInputChange = (field) => (event) => {
    const value = event.target.value;
    if (value === '' || (!isNaN(value) && value >= 0)) {
      setUserData({ ...userData, [field]: value });
    }
  };

  const predictCreditScore = async () => {
    // Validate required fields
    const requiredFields = ['monthly_income', 'monthly_expenses'];
    const missingFields = requiredFields.filter(field => !userData[field]);
    
    if (missingFields.length > 0) {
      setError('Please fill in all required fields: Monthly Income and Monthly Expenses');
      return;
    }

    setError(null);
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict', userData);
      setScore(response.data.credit_score);
      setImprovements(response.data.improvements);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Monthly Income ($)"
                value={userData.monthly_income}
                onChange={handleInputChange('monthly_income')}
                fullWidth
                required
                type="number"
                InputProps={{
                  startAdornment: <AttachMoney color="action" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Monthly Expenses ($)"
                value={userData.monthly_expenses}
                onChange={handleInputChange('monthly_expenses')}
                fullWidth
                required
                type="number"
                InputProps={{
                  startAdornment: <TrendingDown color="action" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Total Savings ($)"
                value={userData.savings}
                onChange={handleInputChange('savings')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <SaveAlt color="action" />,
                }}
              />
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <TextField
                label="On-time Payments"
                value={userData.on_time_payments}
                onChange={handleInputChange('on_time_payments')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <CheckCircle color="success" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                label="Late Payments"
                value={userData.late_payments}
                onChange={handleInputChange('late_payments')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <Warning color="warning" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                label="Missed Payments"
                value={userData.missed_payments}
                onChange={handleInputChange('missed_payments')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <Warning color="error" />,
                }}
              />
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Total Credit Limit ($)"
                value={userData.credit_limit}
                onChange={handleInputChange('credit_limit')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <CreditCard color="action" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Current Balance ($)"
                value={userData.current_balance}
                onChange={handleInputChange('current_balance')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <AccountBalance color="action" />,
                }}
              />
            </Grid>
          </Grid>
        );
      case 3:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Credit Card Debt ($)"
                value={userData.credit_card_debt}
                onChange={handleInputChange('credit_card_debt')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <CreditCard color="action" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Personal Loan ($)"
                value={userData.personal_loan}
                onChange={handleInputChange('personal_loan')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <Payment color="action" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Student Loan ($)"
                value={userData.student_loan}
                onChange={handleInputChange('student_loan')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <School color="action" />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Mortgage ($)"
                value={userData.mortgage}
                onChange={handleInputChange('mortgage')}
                fullWidth
                type="number"
                InputProps={{
                  startAdornment: <Home color="action" />,
                }}
              />
            </Grid>
          </Grid>
        );
      default:
        return null;
    }
  };

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
          py: 4,
        }}
      >
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card>
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom align="center" 
                  sx={{ color: theme.palette.primary.main, mb: 4 }}>
                  Credit Score Predictor & Improvement Planner
                </Typography>

                <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
                  {steps.map((label) => (
                    <Step key={label}>
                      <StepLabel>{label}</StepLabel>
                    </Step>
                  ))}
                </Stepper>

                <Stack spacing={3}>
                  {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                      {error}
                    </Alert>
                  )}

                  {renderStepContent(activeStep)}

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                    <Button
                      disabled={activeStep === 0}
                      onClick={handleBack}
                      variant="outlined"
                    >
                      Back
                    </Button>
                    {activeStep === steps.length - 1 ? (
                      <Button
                        variant="contained"
                        onClick={predictCreditScore}
                        disabled={loading}
                      >
                        {loading ? (
                          <CircularProgress size={24} color="inherit" />
                        ) : (
                          'Calculate Credit Score'
                        )}
                      </Button>
                    ) : (
                      <Button
                        variant="contained"
                        onClick={handleNext}
                      >
                        Next
                      </Button>
                    )}
                  </Box>
                </Stack>

                {score !== null && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                  >
                    <CreditScoreIndicator score={score} improvements={improvements} />
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;