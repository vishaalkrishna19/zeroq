import { useState } from 'react';
import {
  Group,
  ActionIcon,
  Box,
  Avatar,
  Menu,
  UnstyledButton,
  Text,
} from '@mantine/core';
import {
  IconSearch,
  IconHelp,
  IconChevronDown,
} from '@tabler/icons-react';
import styles from './TopBar.module.css';
import { SearchModal } from '../searchModal/SearchModal';

export function TopBar() {
  const [searchModalOpened, setSearchModalOpened] = useState(false);

  return (
    <>
      <Box className={styles.topBar}>
        {/* Left Section - Logo */}
        <Box className={styles.leftSection}>
          <Text className={styles.logo}>ZeroQ</Text>
        </Box>

        {/* Center Section - Search Button */}
        <Box className={styles.centerSection}>
          <UnstyledButton
            className={styles.searchButton}
            onClick={() => setSearchModalOpened(true)}
          >
            <Box className={styles.searchButtonLeft}>
              <IconSearch size={16} />
              <Text className={styles.searchPlaceholder}>Search</Text>
            </Box>
            <Box className={styles.searchKeyboardShortcuts}>
              <Box className={styles.searchKeyboardShortcut}>
                CMD ⌘
              </Box>
              <Box className={styles.searchKeyboardShortcut}>
                K
              </Box>
            </Box>
          </UnstyledButton>
        </Box>

        {/* Right Section - Actions and Profile */}
        <Box className={styles.rightSection}>
          <ActionIcon className={styles.iconButton} variant="subtle">
            <IconHelp size={28} />
          </ActionIcon>

          <Avatar size={32} className={styles.profileAvatar}>
            U
          </Avatar>

          <Menu shadow="md" width={200}>
            <Menu.Target>
              <UnstyledButton className={styles.profileSection}>
                <Group gap={8}>
                  <img
                    src="https://s3.us-west-2.amazonaws.com/assets.www.happyfox.com/media/images/Slack.original.svg"
                    className={styles.companyLogo}
                    alt="Company Logo"
                   
                  />
                  <Text className={styles.companyText}>Company account</Text>
                  <IconChevronDown size={12} />
                </Group>
              </UnstyledButton>
            </Menu.Target>
            <Menu.Dropdown>
              <Menu.Item>Account settings</Menu.Item>
              <Menu.Item>Sign out</Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </Box>
      </Box>

      <SearchModal
        opened={searchModalOpened}
        onClose={() => setSearchModalOpened(false)}
      />
    </>
  );
}
