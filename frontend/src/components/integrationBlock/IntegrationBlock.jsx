import { useState } from 'react';
import {
  Modal,
  Box,
  TextInput,
  Text,
  Group,
  UnstyledButton,
  Stack,
  Select,
  Checkbox,
  Button,
  ScrollArea,
  Divider,
} from '@mantine/core';
import {
  IconSearch,
  IconChevronRight,
  IconX,
} from '@tabler/icons-react';
import styles from './IntegrationBlock.module.css';

const integratedApps = [
  {
    name: 'HappyFox Helpdesk',
    logo: (
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 500 500">
        <rect stroke="#E4E4E4" x="0.5" y="0.5" width="499" height="499" rx="12" fill="white"/>
        <g transform="translate(50, 52)" fill="#FF5A00" fillRule="evenodd">
          <path d="M357.331039,4.79237461 C375.428093,-7.57385856 400,5.43461279 400,27.3300025 L400,229.255143 C400,237.608437 396.143423,245.479003 389.6161,250.668329 L211.562911,391.084472 C201.337996,399.170167 186.830444,398.902568 176.926649,390.391862 L134.528435,353.987872 L9.52915651,246.654341 C3.47983955,241.517485 0,233.966988 0,225.991482 L0,168.175354 C14.8821907,183.004025 34.5827419,190.658937 54.443328,190.658937 C68.6832806,190.658937 83.0297481,186.751463 95.7171004,178.667868 L193.41496,116.676667 Z M0,29.3070886 C0,7.03706001 25.3211847,-5.86437165 43.3620959,7.30518396 L165.524298,96.3302045 L78.5330315,151.52281 C71.3062778,156.126567 62.9550827,158.535485 54.443328,158.535485 L52.5811521,158.426871 C40.536038,158.426871 31.2099421,153.824689 22.6981874,145.366454 L0,122.775831 Z" fillRule="nonzero"/>
        </g>
      </svg>
    ),
    configured: true,
    color: '#FF6B35'
  },
  {
    name: 'Bamboo HR',
    logo: (
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22">
        <circle cx="11" cy="11" r="11" fill="#73C41D"/>
      </svg>
    ),
    configured: false,
    color: '#4CAF50'
  },
  {
    name: 'Pipedrive',
    logo: (
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 500 500">
        <rect stroke="#E4E4E4" x="0.5" y="0.5" width="499" height="499"/>
        <g transform="translate(50, 50)">
          <rect fill="#017737" x="0" y="0" width="400" height="400" rx="200"/>
          <path d="M309.732283,166.692913 C309.732283,220.80315 274.818898,257.811024 224.897638,257.811024 C201.165354,257.811024 181.606299,248.031496 174.283465,235.811024 L174.629921,248.377953 L174.629921,325.874016 L123.669291,325.874016 L123.669291,125.496063 C123.669291,122.708661 122.976378,122 119.826772,122 L102.362205,122 L102.362205,79.4173228 L144.96063,79.4173228 C164.503937,79.4173228 169.401575,96.1732283 170.787402,103.511811 C178.472441,90.5984252 198.708661,75.5905461 227.338583,75.5905461 C276.566929,75.5748031 309.732283,112.220472 309.732283,166.692913 Z M257.716535,167.03937 C257.716535,138.062992 238.866142,118.173228 215.11811,118.173228 C195.574803,118.173228 173.574803,131.086614 173.574803,167.401575 C173.574803,191.133858 186.834646,215.92126 214.425197,215.92126 C234.677165,215.905512 257.716535,201.244094 257.716535,167.03937 Z" fill="#FFFFFF"/>
        </g>
      </svg>
    ),
    configured: false,
    color: '#017737'
  },
  {
    name: 'Wrike',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <circle cx="11" cy="11" r="11" fill="#34C759"/>
        <polyline points="6,12 10,16 16,8" fill="none" stroke="#fff" strokeWidth="2"/>
      </svg>
    ),
    configured: false,
    color: '#34C759'
  }
];

const otherApps = [
  {
    name: 'Zendesk',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#03363D"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">Z</text>
      </svg>
    ),
    color: '#03363D'
  },
  {
    name: 'Microsoft Teams',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#5B2C87"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">T</text>
      </svg>
    ),
    color: '#5B2C87'
  },
  {
    name: 'Gemini',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#4285F4"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">G</text>
      </svg>
    ),
    color: '#4285F4'
  },
  {
    name: 'Microsoft Entra ID',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#0078D4"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">E</text>
      </svg>
    ),
    color: '#0078D4'
  },
  {
    name: 'Google Sheets',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#34A853"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">S</text>
      </svg>
    ),
    color: '#34A853'
  },
  {
    name: 'Gusto',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#FF6B35"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">G</text>
      </svg>
    ),
    color: '#FF6B35'
  },
  {
    name: 'JIRA',
    logo: (
      <svg width="22" height="22" viewBox="0 0 22 22">
        <rect width="22" height="22" rx="6" fill="#0052CC"/>
        <text x="11" y="15" textAnchor="middle" fontSize="12" fill="#fff">J</text>
      </svg>
    ),
    color: '#0052CC'
  }
];

export function IntegrationBlock({ opened, onClose }) {
  const [searchValue, setSearchValue] = useState('');
  const [selectedApp, setSelectedApp] = useState(integratedApps[0]);
  const [showConfigForm, setShowConfigForm] = useState(true);

  const [category, setCategory] = useState('');
  const [ticketTitle, setTicketTitle] = useState('New Employee Onboarding');
  const [ticketDescription, setTicketDescription] = useState('Dynamic / pre-defined with placeholders');
  const [updateComments, setUpdateComments] = useState(true);
  const [closeOnCompletion, setCloseOnCompletion] = useState(true);

  const handleAppClick = (app) => {
    setSelectedApp(app);
    setShowConfigForm(true);
  };

  const handleBackToList = () => {
    setShowConfigForm(false);
    setSelectedApp(null);
  };

  const handleSave = () => {
 
    onClose();
  };

  const handleCancel = () => {
    setShowConfigForm(false);
    setSelectedApp(null);
  };

  const filteredIntegratedApps = integratedApps.filter(app =>
    app.name.toLowerCase().includes(searchValue.toLowerCase())
  );

  const filteredOtherApps = otherApps.filter(app =>
    app.name.toLowerCase().includes(searchValue.toLowerCase())
  );

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      size="xl"
      radius={16}
      withCloseButton
      centered
      classNames={{
        header: styles.modalHeader,
        title: styles.modalTitle,
        content: styles.modalContent,
      }}
      overlayProps={{
        opacity: 0.15,
        blur: 1,
      }}
    >
      <Box className={styles.integrationModalBody}>
        <Box className={styles.integrationSidebar}>
          <Box className={styles.searchContainer}>
            <IconSearch size={18} className={styles.searchIcon} />
            <TextInput
              placeholder="Search apps or actions"
              value={searchValue}
              onChange={(e) => setSearchValue(e.currentTarget.value)}
              className={styles.searchInput}
              variant="unstyled"
            />
          </Box>
          <Box className={styles.sidebarSection}>
            <Text className={styles.sidebarSectionTitle}>Integrated Apps</Text>
            <Stack gap={2}>
              {filteredIntegratedApps.map((app) => (
                <UnstyledButton
                  key={app.name}
                  className={`${styles.sidebarAppItem} ${selectedApp && selectedApp.name === app.name ? styles.sidebarAppItemActive : ''}`}
                  onClick={() => handleAppClick(app)}
                >
                  <Group gap="sm" align="center">
                    <Box className={styles.sidebarAppLogo}>{app.logo}</Box>
                    <Box>
                      <Text className={styles.sidebarAppName}>{app.name}</Text>
                      {app.configured && (
                        <Text className={styles.sidebarConfiguredText}>Configured for Employee Journeys</Text>
                      )}
                    </Box>
                  </Group>
                  <IconChevronRight size={16} className={styles.sidebarChevronIcon} />
                </UnstyledButton>
              ))}
            </Stack>
          </Box>
          <Divider my="sm" />
          <Box className={styles.sidebarSection}>
            <Text className={styles.sidebarSectionTitle}>Other Apps</Text>
            <Stack gap={2}>
              {filteredOtherApps.map((app) => (
                <UnstyledButton
                  key={app.name}
                  className={styles.sidebarAppItem}
                  onClick={() => handleAppClick(app)}
                >
                  <Group gap="sm" align="center">
                    <Box className={styles.sidebarAppLogo}>{app.logo}</Box>
                    <Text className={styles.sidebarAppName}>{app.name}</Text>
                  </Group>
                </UnstyledButton>
              ))}
            </Stack>
          </Box>
        </Box>
        <Box className={styles.integrationFormArea}>
          {showConfigForm && selectedApp && (
            <Box className={styles.configForm}>
              <Group gap="sm" mb="xl" className={styles.configHeader} align="center" justify="space-between">
                <Group gap="sm" align="center">
                  <Box className={styles.appLogo} style={{ backgroundColor: selectedApp.color }}>
                    {selectedApp.logo}
                  </Box>
                  <Box>
                    <Text className={styles.configTitle}>{selectedApp.name}</Text>
                    <Text className={styles.configSubtitle}>Configured for Employee Journeys</Text>
                  </Box>
                </Group>
                <UnstyledButton onClick={onClose} className={styles.closeButton}>
                  <IconX size={20} />
                </UnstyledButton>
              </Group>
              <Stack gap="lg">
                <Select
                  label="Category"
                  placeholder="Please select"
                  data={[
                    { value: 'hr', label: 'HR' },
                    { value: 'it', label: 'IT' },
                    { value: 'general', label: 'General' }
                  ]}
                  value={category}
                  onChange={setCategory}
                  required
                  className={styles.formField}
                />
                <Select
                  label="Ticket title"
                  value={ticketTitle}
                  onChange={setTicketTitle}
                  data={[
                    { value: 'New Employee Onboarding', label: 'New Employee Onboarding' },
                    { value: 'Employee Exit', label: 'Employee Exit' }
                  ]}
                  required
                  className={styles.formField}
                />
                <Select
                  label="Ticket description"
                  value={ticketDescription}
                  onChange={setTicketDescription}
                  data={[
                    { value: 'Dynamic / pre-defined with placeholders', label: 'Dynamic / pre-defined with placeholders' },
                    { value: 'Custom', label: 'Custom' }
                  ]}
                  className={styles.formField}
                />
                <Checkbox
                  label="Update all communication as comments"
                  checked={updateComments}
                  onChange={(event) => setUpdateComments(event.currentTarget.checked)}
                  className={styles.checkbox}
                />
                <Checkbox
                  label="Close ticket on onboarding completion"
                  checked={closeOnCompletion}
                  onChange={(event) => setCloseOnCompletion(event.currentTarget.checked)}
                  className={styles.checkbox}
                />
              </Stack>
              <Group justify="flex-end" mt="xl" gap="sm">
                <Button
                  variant="outline"
                  onClick={handleCancel}
                  className={styles.cancelButton}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleSave}
                  className={styles.saveButton}
                >
                  Save
                </Button>
              </Group>
            </Box>
          )}
        </Box>
      </Box>
    </Modal>
  );
}
