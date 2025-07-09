import { useState } from 'react';
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

const OnBoardingForm = ({ opened, onClose }) => {
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

  const handleSubmit = () => {
    // Handle form submission
    console.log('Form Data:', formData);
    console.log('Steps:', steps);
    onClose();
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
                >
                    Cancel
                </Button>
                <Button
                    onClick={handleSubmit}
                    className={styles.createButton}
                    size="sm"
                >
                    Create Onboarding Journey
                </Button>
            </Group>
        </Box>
    </Modal>
);
};

export default OnBoardingForm;
