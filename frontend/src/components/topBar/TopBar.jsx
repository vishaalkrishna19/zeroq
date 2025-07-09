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
import { useNavigate } from 'react-router-dom';

export function TopBar() {
  const [searchModalOpened, setSearchModalOpened] = useState(false);
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      // Call Django's logout endpoint
      await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        },
        credentials: 'include',
      });
      
      // Clear local storage
      localStorage.removeItem('authToken');
      localStorage.removeItem('username');
      
      // Redirect to login page
      navigate('/login');
      
    } catch (error) {
      console.error('Logout error:', error);
      // Even if logout fails, clear local storage and redirect
      localStorage.removeItem('authToken');
      localStorage.removeItem('username');
      navigate('/login');
    }
  };

  return (
    <>
      <Box className={styles.topBar}>
        {/* Left Section - Logo */}
        <Box className={styles.leftSection}>
          <Text className={styles.logo}>Zero Q</Text>
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
              <Menu.Item onClick={handleSignOut}>Sign out</Menu.Item>
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
