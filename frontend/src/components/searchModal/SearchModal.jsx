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
} from '@tabler/icons-react';
import styles from './SearchModal.module.css';

export function SearchModal({ opened, onClose }) {
  const [searchValue, setSearchValue] = useState('');

  const hrItems = [
    { label: 'Employee Journeys', icon: IconRoad },
    { label: 'Manager Hub', icon: IconUserCheck },
    { label: 'Employee Relations', icon: IconHeart },
    { label: 'Employee Center Pro', icon: IconUsers },
    { label: 'HR Case & Knowledge', icon: IconQuestionMark },
  ];

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
        opacity: 0.3,
        blur: 3,
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
            <Box>
              <Text size="sm" fw={600} c="dimmed" className={styles.sectionTitle}>
                HR
              </Text>
              <Stack gap={2}>
                {hrItems.map((item, index) => (
                  <UnstyledButton
                    key={item.label}
                    className={`${styles.searchResultItem} ${index === 0 ? styles.highlighted : ''}`}
                  >
                    <Group gap="sm">
                      <item.icon size={16} />
                      <Text size="sm">{item.label}</Text>
                    </Group>
                  </UnstyledButton>
                ))}
              </Stack>
            </Box>

            
          </Stack>
        </Box>

        <Divider />

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