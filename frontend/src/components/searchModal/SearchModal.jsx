/* filepath: /Users/happyfox/Documents/GitHub/zeroq/frontend/src/components/searchModal/SearchModal.jsx */
import { useState } from 'react';
import {
  Modal,
  Box,
  TextInput,
  Text,
  Group,
  UnstyledButton,
  Stack,
  Divider,
} from '@mantine/core';
import {
  IconSearch,
  IconRoad,
  IconUserCheck,
  IconHeart,
  IconUsers,
  IconQuestionMark,
  IconKey,
  IconDeviceDesktop,
  IconArrowUp,
  IconArrowDown,
  IconCornerDownLeft,
  IconHome,
} from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import styles from './SearchModal.module.css';

export function SearchModal({ opened, onClose }) {
  const [searchValue, setSearchValue] = useState('');
  const navigate = useNavigate();

  const homeItem = { label: 'Home', icon: IconHome };
  const hrItems = [
    { label: 'Employee Journeys', icon: IconRoad },
    { label: 'Manager Hub', icon: IconUserCheck },
    { label: 'Employee Relations', icon: IconHeart },
    { label: 'Employee Center Pro', icon: IconUsers },
    { label: 'HR Case & Knowledge', icon: IconQuestionMark },
  ];

  // Filter items based on searchValue (case-insensitive)
  const filteredHome = homeItem.label.toLowerCase().includes(searchValue.toLowerCase())
    ? [homeItem]
    : [];
  const filteredHrItems = hrItems.filter(item =>
    item.label.toLowerCase().includes(searchValue.toLowerCase())
  );

  // Adjust modal height based on results
  const resultCount = filteredHome.length + filteredHrItems.length;
  const modalHeight = resultCount === 0
    ? 220
    : Math.min(120 + resultCount * 56, 600); // 56px per item, min 120px, max 600px

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      centered
      size="50rem"
      withCloseButton={false}
      padding={0}
      radius="0.625rem"
      overlayProps={{
        opacity: 0,
        blur: 0,
      }}
      styles={{
        body: { padding: 0 },
        content: { minHeight: modalHeight, maxHeight: 600, transition: 'min-height 0.2s' }
      }}
    >
      <Box className={styles.searchModal}>
        <Box className={styles.searchInputContainer}>
          <IconSearch size={20} className={styles.searchIcon} />
          <TextInput
            placeholder="Search commands..."
            value={searchValue}
            onChange={(e) => setSearchValue(e.currentTarget.value)}
            className={styles.searchInput}
            variant="unstyled"
            autoFocus
          />
        </Box>

        <Box className={styles.searchResults}>
          <Stack gap="xs">
            {/* Home section */}
            {filteredHome.length > 0 && (
              <Box>
                <Text size="sm" fw={600} c="dimmed" className={styles.sectionTitle}>
                  General
                </Text>
                <Stack gap={2}>
                  <UnstyledButton
                    key={homeItem.label}
                    className={`${styles.searchResultItem} ${styles.highlighted}`}
                    onClick={() => {
                      navigate('/dashboard');
                      if (onClose) onClose();
                    }}
                  >
                    <Group gap="sm">
                      <homeItem.icon size={16} />
                      <Text size="sm">{homeItem.label}</Text>
                    </Group>
                  </UnstyledButton>
                </Stack>
              </Box>
            )}
            {/* HR section */}
            {filteredHrItems.length > 0 && (
              <Box>
                <Text size="sm" fw={600} c="dimmed" className={styles.sectionTitle}>
                  HR
                </Text>
                <Stack gap={2}>
                  {filteredHrItems.map((item) => (
                    <UnstyledButton
                      key={item.label}
                      className={styles.searchResultItem}
                      onClick={() => {
                        if (item.label === 'Employee Journeys') {
                          navigate('/dashboard/employee-journeys');
                          if (onClose) onClose();
                        }
                        // Add more navigation logic for other items if needed
                      }}
                    >
                      <Group gap="sm">
                        <item.icon size={16} />
                        <Text size="sm">{item.label}</Text>
                      </Group>
                    </UnstyledButton>
                  ))}
                </Stack>
              </Box>
            )}
            {/* No results */}
            {filteredHome.length === 0 && filteredHrItems.length === 0 && (
              <Box p="md">
                <Text size="sm" c="dimmed" ta="center">
                  No results found.
                </Text>
              </Box>
            )}
          </Stack>
        </Box>



        <Box className={styles.searchFooter}>
          <Group gap="md">
            <Group gap="xs">
              <Box className={styles.keyboardKey}>
                <IconArrowUp size={12} />
              </Box>
              <Box className={styles.keyboardKey}>
                <IconArrowDown size={12} />
              </Box>
              <Text size="xs" c="dimmed">to navigate</Text>
            </Group>
            <Group gap="xs">
              <Box className={styles.keyboardKey}>
                <Text size="xs">enter</Text>
              </Box>
              <Text size="xs" c="dimmed">to select</Text>
            </Group>
            <Group gap="xs">
              <Box className={styles.keyboardKey}>
                <Text size="xs">esc</Text>
              </Box>
              <Text size="xs" c="dimmed">to close</Text>
            </Group>
          </Group>
        </Box>
      </Box>
    </Modal>
  );
}