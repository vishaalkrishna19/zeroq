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
import { useNavigate, useParams } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';
import { TopBar } from '../../../components/topbar/Topbar';
import UpdateFormHeader from '../../../components/offBoarding/updateFormHeader/UpdateFormHeader';
import ApiService from '../../../utils/api';
import styles from '../OffBoardingFormPage.module.css';

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
  { value: 'handover', label: 'Handover' },
  { value: 'access_revocation', label: 'Access Revocation' },
];

const responsiblePartyOptionsDefault = [
  { value: 'manager', label: 'Manager' },
  { value: 'it_team', label: 'IT Team' },
  { value: 'hr_team', label: 'HR Team' },
];

const UpdateOffBoardingFormPage = () => {
  const navigate = useNavigate();
  const { templateId } = useParams();
  const stepRefs = useRef({});
  const [formData, setFormData] = useState({
    journeyTitle: '',
    department: '',
    businessUnit: '',
    estimatedDuration: 15,
    journeyDescription: '',
  });

  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const [error, setError] = useState('');
  const [account, setAccount] = useState(null);
  const [userOptions, setUserOptions] = useState([]);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const accountData = await ApiService.getAccounts();
        setAccount(accountData);
        await fetchUsers();
        if (templateId) {
          await fetchTemplateData();
        }
      } catch (error) {
        setError('Failed to load account data');
      }
    };
    fetchInitialData();
  }, [templateId]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const fetchTemplateData = async () => {
    try {
      setFetchLoading(true);
      
      console.log('Fetching offboarding template with ID:', templateId);
      
      const template = await ApiService.getJourneyTemplate(templateId);
      console.log('Fetched offboarding template:', template);
      
      if (!template || !template.id) {
        throw new Error('Invalid template data received');
      }
      
      setFormData({
        journeyTitle: template.title || '',
        department: template.department || '',
        businessUnit: template.business_unit || '',
        estimatedDuration: template.estimated_duration_days || 15,
        journeyDescription: template.description || '',
      });

      if (template.steps && Array.isArray(template.steps) && template.steps.length > 0) {
        const mappedSteps = template.steps.map((step, index) => ({
          id: step.id || Date.now() + index,
          stepTitle: step.title || '',
          stepDescription: step.description || '',
          stepType: mapBackendToStepType(step.step_type),
          responsibleParty: mapRoleToResponsibleParty(step.responsible_role),
          dueDays: step.due_days_from_start || 1,
        }));
        setSteps(mappedSteps);
      } else {
        setSteps([{
          id: 1,
          stepTitle: '',
          stepDescription: '',
          stepType: '',
          responsibleParty: '',
          dueDays: 1,
        }]);
      }
      
    } catch (error) {
      console.error('Failed to fetch template data:', error);
      setError(`Failed to load template data: ${error.message}`);
    } finally {
      setFetchLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/users/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });
      if (res.ok) {
        const data = await res.json();
        const users = Array.isArray(data) ? data : data.results || [];
        setUserOptions(
          users.map(user => ({
            value: user.username,
            label: user.username,
          }))
        );
      }
    } catch (err) {
      // fallback: do nothing, keep default options
    }
  };

  const mapBackendToStepType = (backendType) => {
    const mapping = {
      'documentation': 'documentation',
      'handover': 'handover',
      'access_revocation': 'access_revocation',
      'other': 'documentation'
    };
    return mapping[backendType] || 'documentation';
  };

  const mapRoleToResponsibleParty = (role) => {
    if (userOptions.some(u => u.value === role)) {
      return role;
    }
    const mapping = {
      'Manager': 'manager',
      'IT Administrator': 'it_team',
      'HR Manager': 'hr_team'
    };
    return mapping[role] || role;
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
      
      setTimeout(() => {
        const newStepElement = stepRefs.current[newStep.id];
        if (newStepElement) {
          newStepElement.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'nearest'
          });
          
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
      'handover': 'handover',
      'access_revocation': 'access_revocation'
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
      if (!formData.journeyTitle.trim()) {
        throw new Error('Journey title is required');
      }
      
      if (steps.some(step => !step.stepTitle.trim())) {
        throw new Error('All steps must have a title');
      }

      if (!account) {
        throw new Error('Account data not loaded');
      }

      let accountId = 'default';
      if (account.length > 0) {
        accountId = account[0].id;
      }

      const apiData = {
        title: formData.journeyTitle,
        description: formData.journeyDescription,
        department: formData.department,
        business_unit: formData.businessUnit,
        estimated_duration_days: formData.estimatedDuration,
        journey_type: 'offboarding',
        account: accountId,
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

      console.log('Updating offboarding template data:', apiData);

      const updatedTemplate = await ApiService.updateJourneyTemplate(templateId, apiData);
      console.log('Offboarding template updated successfully:', updatedTemplate);
    
      toast.success('Offboarding journey updated successfully!', {
        duration: 3000,
        position: 'top-center',
        style: {
          background: 'white',
          color: '#111',
          fontWeight: '400',
          padding: '16px 25px',
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          width: '420px', 
          maxWidth: '90vw',
        },
      });

      setTimeout(() => {
        navigate('/dashboard/employee-journeys');
      }, 1000);
        
    } catch (error) {
      console.error('Failed to update template:', error);
      if (error.message.includes('403')) {
        setError('Permission denied. Please check your authentication.');
      } else if (error.message.includes('400')) {
        setError('Invalid data submitted. Please check your form fields.');
      } else {
        setError(error.message || 'Failed to update template. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/dashboard/employee-journeys');
  };

  if (fetchLoading) {
    return (
      <>
        <TopBar />
        <Box className={styles.container}>
          <Text>Loading template data...</Text>
        </Box>
      </>
    );
  }

  return (
    <>
      <Toaster />
      <TopBar />
      <Box className={styles.formHeader}>
        <UpdateFormHeader />
      </Box>
      <Box className={styles.container}>
        {error && (
          <Box className={styles.errorMessage}>
            {error}
          </Box>
        )}

        <Box className={styles.mainContent}>
          <Box className={styles.leftSection}>
            <Box className={styles.sectionCard}>
              <Title order={3} className={styles.sectionTitle}>
                Journey Details
              </Title>
              <Text className={styles.sectionSubtitle}>
                Update the core details for this offboarding journey.
              </Text>

              <Stack gap="lg" mt="xl">
                <TextInput
                  label="Journey Title"
                  placeholder="e.g., Software Engineer Offboarding"
                  value={formData.journeyTitle}
                  onChange={(event) => setFormData({ ...formData, journeyTitle: event.target.value })}
                  className={styles.input}
                  size="sm"
                />

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
                    placeholder="e.g., 15"
                    value={formData.estimatedDuration}
                    onChange={(value) => setFormData({ ...formData, estimatedDuration: value })}
                    min={1}
                    max={180}
                    className={styles.numberInput}
                    size="sm"
                  />
                </Group>

                <Textarea
                  label="Journey Description"
                  placeholder="Brief description of the offboarding process..."
                  value={formData.journeyDescription}
                  onChange={(event) => setFormData({ ...formData, journeyDescription: event.target.value })}
                  rows={4}
                  className={styles.textarea}
                  size="sm"
                />
              </Stack>
            </Box>
          </Box>

          <Box className={styles.rightSection}>
            <Box className={styles.sectionCard}>
              <Group justify="space-between" align="center" mb="md">
                <Box>
                  <Title order={3} className={styles.sectionTitle}>
                    Offboarding Steps
                  </Title>
                  <Text className={styles.sectionSubtitle}>
                    Update the steps for this journey.
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
                          placeholder="e.g., Return Company Equipment"
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
                            data={[...responsiblePartyOptionsDefault, ...userOptions]}
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
                            max={180}
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
              Update Journey
            </Button>
          </Group>
        </Box>
      </Box>
    </>
  );
};

export default UpdateOffBoardingFormPage;
