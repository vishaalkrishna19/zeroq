import { useEffect, useState } from 'react';
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
  IconSwitchHorizontal,
  IconPlus,
  IconSettings,
  IconLogout,
  IconDashboard,
} from '@tabler/icons-react';
import styles from './TopBar.module.css';
import { SearchModal } from '../searchModal/SearchModal';
import { useNavigate } from 'react-router-dom';

export function TopBar() {
  const [searchModalOpened, setSearchModalOpened] = useState(false);
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [firstName, setFirstName] = useState('');
  
    useEffect(() => {
      const authToken = localStorage.getItem('authToken');
      if (!authToken) return;

      // Always fetch current user data from /api/auth/user/ first to ensure we have the correct user
      fetch('http://localhost:8000/api/auth/user/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${authToken}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      })
        .then(res => res.ok ? res.json() : Promise.reject())
        .then(data => {
          if (data.pk) {
            console.log('Current user ID from auth/user:', data);
            // Update localStorage with current user ID
            localStorage.setItem('userId', data.pk);
            
            // Fetch detailed user data
            fetch(`http://localhost:8000/api/users/${data.pk}/`, {
              method: 'GET',
              headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json',
              },
              credentials: 'include',
            })
              .then(res => res.ok ? res.json() : Promise.reject())
              .then(userData => {
                console.log('User data:', userData);
                setRole(userData.role_name || '');
                setFirstName(userData.first_name || '');
              })
              .catch(() => {});
          }
        })
        .catch(() => {});
    }, []);

    console.log('User role:', role); 

  const handleSignOut = async () => {
    try {
      await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        },
        credentials: 'include',
      });
      
      // Clear all stored user data
      localStorage.removeItem('authToken');
      localStorage.removeItem('username');
      localStorage.removeItem('userId'); // Add this line
      
      navigate('/login');
      
    } catch (error) {
      console.error('Logout error:', error);

      // Clear all stored user data
      localStorage.removeItem('authToken');
      localStorage.removeItem('username');
      localStorage.removeItem('userId'); // Add this line
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

          {/* User Profile Avatar Dropdown */}
          <Menu shadow="md" width={200}>
            <Menu.Target>
              <Avatar size={32} className={styles.profileAvatar} style={{ cursor: 'pointer' }}>
                {firstName ? firstName[0].toUpperCase() : 'U'}
              </Avatar>
            </Menu.Target>
            <Menu.Dropdown className={styles.menuDropdown}>
            {(role.toLowerCase() === 'administrator' || role.toLowerCase() === 'admin') && (
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconDashboard size={16} />}
                onClick={() => navigate('/dashboard')}
              >
                Dashboard
              </Menu.Item>
            )}
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconSettings size={16} />}
              >
                Settings
              </Menu.Item>
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconLogout size={16} />}
                onClick={handleSignOut}
              >
                Sign out
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>

          {/* Company Account Dropdown */}
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
            <Menu.Dropdown className={styles.menuDropdown}>
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconSwitchHorizontal size={16} />}
              >
                Switch workspace
              </Menu.Item>
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconPlus size={16} />}
              >
                Add workspace
              </Menu.Item>
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconSettings size={16} />}
              >
                Settings
              </Menu.Item>
              <Menu.Item 
                className={styles.menuItem}
                leftSection={<IconLogout size={16} />}
                onClick={handleSignOut}
              >
                Sign out
              </Menu.Item>
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
