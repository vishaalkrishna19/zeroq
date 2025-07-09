import { useState, useEffect, useRef } from 'react';
import {
  Box,
  Group,
  Text,
  TextInput,
  Select,
  NumberInput,
  Textarea,
  Button,
  ActionIcon,
  Stack,
  ScrollArea,
  Title,
} from '@mantine/core';
import { IconTrash, IconPlus } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';
import { TopBar } from '../../components/topbar/Topbar';
import OnBoardingFormHeader from '../../components/onBoarding/onBoardingFormHeader/OnBoardingFormHeader';
import ApiService from '../../utils/api';
import styles from './OnBoardingFormPage.module.css';

const departmentOptions = [
  { value: 'engineering', label: 'Engineering' },
  { value: 'sales', label: 'Sales' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'hr', label: 'HR' },
];

const businessUnitOptions = [
  { value: 'india', label: 'India' },
  { value: 'uk', label: 'UK' },
  { value: 'usa', label: 'USA' },
  { value: 'canada', label: 'Canada' },
];

const stepTypeOptions = [
  { value: 'documentation', label: 'Documentation' },
  { value: 'orientation', label: 'Orientation' },
  { value: 'integration', label: 'Integration' },
];

const responsiblePartyOptions = [
  { value: 'manager', label: 'Manager' },
  { value: 'it_team', label: 'IT Team' },
  { value: 'hr_team', label: 'HR Team' },
];

const OnBoardingFormPage = () => {
  const navigate = useNavigate();
  const stepRefs = useRef({});
  const [formData, setFormData] = useState({
    journeyTitle: '',
    department: '',
    businessUnit: '',
    estimatedDuration: 0,
    journeyDescription: '',
  });

  const [steps, setSteps] = useState([
    {
      id: 1,
      stepTitle: '',
      stepDescription: '',
      stepType: '',
      responsibleParty: '',
      dueDays: 1,
    },
  ]);

  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await ApiService.getAccounts();
      setAccounts(response.results || response);
    } catch (error) {
      console.error('Failed to fetch accounts:', error);
      setAccounts([{ id: 'default', name: 'Default Account' }]);
    }
  };

  const handleAddStep = () => {
    const newStep = {
      id: Date.now(),
      stepTitle: '',
      stepDescription: '',
      stepType: '',
      responsibleParty: '',
      dueDays: 1,
    };
    setSteps(prevSteps => {
      const updatedSteps = [...prevSteps, newStep];
      
      // Scroll to the new step after it's rendered
      setTimeout(() => {
        const newStepElement = stepRefs.current[newStep.id];
        if (newStepElement) {
          newStepElement.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'nearest'
          });
          
          // Optional: Add a subtle highlight animation
          newStepElement.style.transform = 'scale(1.02)';
          newStepElement.style.transition = 'transform 0.3s ease';
          setTimeout(() => {
            newStepElement.style.transform = 'scale(1)';
          }, 300);
        }
      }, 100);
      
      return updatedSteps;
    });
  };

  const handleRemoveStep = (stepId) => {
    if (steps.length > 1) {
      setSteps(steps.filter(step => step.id !== stepId));
    }
  };

  const handleStepChange = (stepId, field, value) => {
    setSteps(steps.map(step => 
      step.id === stepId ? { ...step, [field]: value } : step
    ));
  };

  const mapStepTypeToBackend = (frontendType) => {
    const mapping = {
      'documentation': 'documentation',
      'orientation': 'orientation', 
      'integration': 'training'
    };
    return mapping[frontendType] || 'other';
  };

  const mapResponsiblePartyToRole = (party) => {
    const mapping = {
      'manager': 'Manager',
      'it_team': 'IT Administrator',
      'hr_team': 'HR Manager'
    };
    return mapping[party] || party;
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Validate required fields
      if (!formData.journeyTitle.trim()) {
        throw new Error('Journey title is required');
      }
      
      if (steps.some(step => !step.stepTitle.trim())) {
        throw new Error('All steps must have a title');
      }

      // Get account - use first account or create a default ID
      let accountId = 'default';
      if (accounts.length > 0) {
        accountId = accounts[0].id;
      }

      // Map form data to API format
      const apiData = {
        journey_type: 'onboarding',
        title: formData.journeyTitle,
        description: formData.journeyDescription,
        job_title: null,
        department: formData.department,
        business_unit: formData.businessUnit,
        estimated_duration_days: formData.estimatedDuration,
        account: accountId,
        is_active: true,
        is_default: false,
        steps_data: steps.filter(step => step.stepTitle.trim()).map((step, index) => ({
          title: step.stepTitle,
          description: step.stepDescription,
          step_type: mapStepTypeToBackend(step.stepType),
          responsible_role: mapResponsiblePartyToRole(step.responsibleParty),
          due_days_from_start: step.dueDays,
          order: index + 1,
          is_mandatory: true,
          is_blocking: false,
          requires_approval: false,
          auto_assign: true,
          estimated_duration_hours: 4,
          notes: ''
        }))
      };

      console.log('Submitting template data:', apiData);

      try {
        const newTemplate = await ApiService.createJourneyTemplate(apiData);
        console.log('Template created successfully:', newTemplate);
        
        // Show success toast
        toast.success('Onboarding journey created successfully!', {
          duration: 3000,
          position: 'top-center',
          style: {
            background: '#10b981',
            color: 'white',
            fontWeight: '500',
            padding: '16px 20px',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          },
        });

        // Navigate back to templates page after a short delay
        setTimeout(() => {
          navigate('/dashboard/employee-journeys');
        }, 1000);
        
      } catch (apiError) {
        console.error('API submission failed:', apiError);
        
        if (apiError.message.includes('403')) {
          setError('Permission denied. Please check your authentication.');
        } else if (apiError.message.includes('CSRF')) {
          setError('Security token error. Please refresh the page and try again.');
        } else if (apiError.message.includes('400')) {
          setError('Invalid data submitted. Please check your form fields.');
        } else {
          setError(`Failed to create template: ${apiError.message}`);
        }
        
        return;
      }

    } catch (error) {
      console.error('Failed to create template:', error);
      setError(error.message || 'Failed to create template. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/dashboard/employee-journeys');
  };

  return (
    <>
      <Toaster />
      <TopBar />
      <Box className={styles.formHeader}>
        <OnBoardingFormHeader />
      </Box>
      <Box className={styles.container}>
        {error && (
          <Box className={styles.errorMessage}>
            {error}
          </Box>
        )}

        {/* Main Content */}
        <Box className={styles.mainContent}>
          {/* Left Side - Journey Details */}
          <Box className={styles.leftSection}>
            <Box className={styles.sectionCard}>
              <Title order={3} className={styles.sectionTitle}>
                Journey Details
              </Title>
              <Text className={styles.sectionSubtitle}>
                Define the core details for this onboarding journey.
              </Text>

              <Stack gap="lg" mt="xl">
                {/* Journey Title only */}
                <TextInput
                  label="Journey Title"
                  placeholder="e.g., Software Engineer Onboarding"
                  value={formData.journeyTitle}
                  onChange={(event) => setFormData({ ...formData, journeyTitle: event.target.value })}
                  className={styles.input}
                  size="sm"
                />

                {/* Department, Business Unit, Duration */}
                <Group grow align="flex-start">
                  <Select
                    label="Department"
                    placeholder="Select department"
                    data={departmentOptions}
                    value={formData.department}
                    onChange={(value) => setFormData({ ...formData, department: value })}
                    className={styles.select}
                    size="sm"
                  />
                  <Select
                    label="Business Unit"
                    placeholder="Select business unit"
                    data={businessUnitOptions}
                    value={formData.businessUnit}
                    onChange={(value) => setFormData({ ...formData, businessUnit: value })}
                    className={styles.select}
                    size="sm"
                  />
                  <NumberInput
                    label="Estimated Duration (days)"
                    placeholder="e.g., 30"
                    value={formData.estimatedDuration}
                    onChange={(value) => setFormData({ ...formData, estimatedDuration: value })}
                    min={1}
                    max={365}
                    className={styles.numberInput}
                    size="sm"
                  />
                </Group>

                {/* Journey Description */}
                <Textarea
                  label="Journey Description"
                  placeholder="Brief description of the onboarding process..."
                  value={formData.journeyDescription}
                  onChange={(event) => setFormData({ ...formData, journeyDescription: event.target.value })}
                  rows={4}
                  className={styles.textarea}
                  size="sm"
                />
              </Stack>
            </Box>
          </Box>

          {/* Right Side - Onboarding Steps */}
          <Box className={styles.rightSection}>
            <Box className={styles.sectionCard}>
              <Group justify="space-between" align="center" mb="md">
                <Box>
                  <Title order={3} className={styles.sectionTitle}>
                    Onboarding Steps
                  </Title>
                  <Text className={styles.sectionSubtitle}>
                    Define the steps for this journey.
                  </Text>
                </Box>
                <Button
                  variant="outline"
                  leftSection={<IconPlus size={16} />}
                  onClick={handleAddStep}
                  className={styles.addStepButton}
                  size="sm"
                >
                  Add Step
                </Button>
              </Group>

              <ScrollArea className={styles.stepsScrollArea}>
                <Stack gap="lg">
                  {steps.map((step, index) => (
                    <Box 
                      key={step.id} 
                      className={styles.stepContainer}
                      ref={(el) => stepRefs.current[step.id] = el}
                    >
                      <Group justify="space-between" align="center" mb="md">
                        <Text className={styles.stepTitle}>Step {index + 1}</Text>
                        {steps.length > 1 && (
                          <ActionIcon
                            variant="subtle"
                            color="red"
                            size="sm"
                            onClick={() => handleRemoveStep(step.id)}
                          >
                            <IconTrash size={16} />
                          </ActionIcon>
                        )}
                      </Group>

                      <Stack gap="md">
                        <TextInput
                          label="Step Title"
                          placeholder="e.g., Complete HR Orientation"
                          value={step.stepTitle}
                          onChange={(event) => handleStepChange(step.id, 'stepTitle', event.target.value)}
                          size="sm"
                        />

                        <Textarea
                          label="Step Description (Optional)"
                          placeholder="Detailed instructions for this step..."
                          value={step.stepDescription}
                          onChange={(event) => handleStepChange(step.id, 'stepDescription', event.target.value)}
                          rows={2}
                          size="sm"
                        />

                        <Group grow>
                          <Select
                            label="Step Type"
                            placeholder="Select type"
                            data={stepTypeOptions}
                            value={step.stepType}
                            onChange={(value) => handleStepChange(step.id, 'stepType', value)}
                            size="sm"
                          />
                          <Select
                            label="Responsible Party"
                            placeholder="Select assignee"
                            data={responsiblePartyOptions}
                            value={step.responsibleParty}
                            onChange={(value) => handleStepChange(step.id, 'responsibleParty', value)}
                            size="sm"
                          />
                          <NumberInput
                            label="Due (days from start)"
                            placeholder="e.g., 1"
                            value={step.dueDays}
                            onChange={(value) => handleStepChange(step.id, 'dueDays', value)}
                            min={1}
                            max={365}
                            size="sm"
                          />
                        </Group>
                      </Stack>
                    </Box>
                  ))}
                </Stack>
              </ScrollArea>
            </Box>
          </Box>
        </Box>

        {/* Footer */}
        <Box className={styles.footer}>
          <Group justify="flex-end">
            <Button
              variant="outline"
              onClick={handleBack}
              className={styles.cancelButton}
              size="sm"
              disabled={loading}
            >
              Cancel
            </Button>
            <Button
              onClick={handleSubmit}
              className={styles.createButton}
              size="sm"
              loading={loading}
            >
              Create Onboarding Journey
            </Button>
          </Group>
        </Box>
      </Box>
    </>
  );
};

export default OnBoardingFormPage;
