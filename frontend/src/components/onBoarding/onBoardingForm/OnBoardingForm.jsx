import { useState, useEffect } from 'react';
import {
  Modal,
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
  Divider,
} from '@mantine/core';
import { IconX, IconTrash, IconPlus } from '@tabler/icons-react';
import styles from './OnBoardingForm.module.css';
import ApiService from '../../../utils/api';

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

const OnBoardingForm = ({ opened, onClose, onTemplateCreated }) => {
  const [formData, setFormData] = useState({
    journeyTitle: '',
    jobTitle: '',
    department: '',
    businessUnit: '',
    estimatedDuration: 30,
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
    if (opened) {
      fetchAccounts();
    }
  }, [opened]);

  const fetchAccounts = async () => {
    try {
      const response = await ApiService.getAccounts();
      setAccounts(response.results || response);
    } catch (error) {
      console.error('Failed to fetch accounts:', error);
      // Use default account
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
    setSteps([...steps, newStep]);
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
        // Try to submit to API first
        const newTemplate = await ApiService.createJourneyTemplate(apiData);
        console.log('Template created successfully:', newTemplate);
        
        // Notify parent component with real API response
        if (onTemplateCreated) {
          onTemplateCreated(newTemplate);
        }

        // Reset form
        setFormData({
          journeyTitle: '',
          jobTitle: '',
          department: '',
          businessUnit: '',
          estimatedDuration: 30,
          journeyDescription: '',
        });
        
        setSteps([{
          id: 1,
          stepTitle: '',
          stepDescription: '',
          stepType: '',
          responsibleParty: '',
          dueDays: 1,
        }]);

        onClose();
        
      } catch (apiError) {
        console.error('API submission failed:', apiError);
        
        // Show specific error message
        if (apiError.message.includes('403')) {
          setError('Permission denied. Please check your authentication.');
        } else if (apiError.message.includes('CSRF')) {
          setError('Security token error. Please refresh the page and try again.');
        } else if (apiError.message.includes('400')) {
          setError('Invalid data submitted. Please check your form fields.');
        } else {
          setError(`Failed to create template: ${apiError.message}`);
        }
        
        // Don't create mock data if API fails - let user fix the issue
        return;
      }

    } catch (error) {
      console.error('Failed to create template:', error);
      setError(error.message || 'Failed to create template. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
        opened={opened}
        onClose={onClose}
        size="xl"
        centered
        overlayProps={{ opacity: 0.8 }}
        className={styles.modal}
        withCloseButton={false}
        padding="xl"
        styles={{
            content: { borderRadius: 10, maxHeight: '90vh', overflowY: 'auto' },
            body: { padding: 0 },
        }}
    >
        <Box className={styles.container}>
 
            <Group justify="space-between" align="center" mb="lg">
                <Box>
                    <Text className={styles.title}>Create New Onboarding Journey</Text>
                    <Text className={styles.subtitle}>
                        Define the core details and initial steps for this onboarding journey.
                    </Text>
                </Box>
                <ActionIcon
                    variant="subtle"
                    color="gray"
                    size="lg"
                    onClick={onClose}
                    className={styles.closeButton}
                >
                    <IconX size={18} />
                </ActionIcon>
            </Group>

            {error && (
              <Box mb="md" style={{ 
                color: 'red', 
                fontSize: '14px', 
                backgroundColor: '#fee2e2', 
                padding: '8px', 
                borderRadius: '4px' 
              }}>
                {error}
              </Box>
            )}

            {/* Form Content */}
            <Stack gap="lg">
                {/* Journey Title */}
                <Group grow align='flex-start'>
                    <TextInput
                        label="Journey Title"
                        placeholder="e.g., Software Engineer Onboarding"
                        value={formData.journeyTitle}
                        onChange={(event) => setFormData({ ...formData, journeyTitle: event.target.value })}
                        className={styles.input}
                        size="sm"
                    />
                    <TextInput
                        label="Job Title"
                        placeholder="e.g., Software Engineer"
                        value={formData.jobTitle}
                        onChange={(event) => setFormData({ ...formData, jobTitle: event.target.value })}
                        className={styles.input}
                        size="sm"
                    />
                </Group>

                {/* Department, Business Unit, Duration Row */}
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
                        placeholder="e.g., 30 for 1 month"
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
                    rows={3}
                    className={styles.textarea}
                    size="sm"
                />
                <Divider my="sm" />
                {/* Onboarding Steps */}
                <Box>
                    <Text className={styles.sectionTitle} mb="md">Onboarding Steps</Text>
                    
                    {steps.map((step, index) => (
                        <Box key={step.id} className={styles.stepContainer} mb="lg">
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
                                        label="Due (days from start date)"
                                        placeholder="e.g., 1 for first day"
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

                    <Button
                        variant="outline"
                        leftSection={<IconPlus size={16} />}
                        onClick={handleAddStep}
                        className={styles.addStepButton}
                        size="sm"
                    >
                        Add Another Step
                    </Button>
                </Box>
            </Stack>

            {/* Footer Buttons */}
            <Group justify="flex-end" mt="xl" pt="lg" className={styles.footer}>
                <Button
                    variant="outline"
                    onClick={onClose}
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
    </Modal>
  );
};

export default OnBoardingForm;