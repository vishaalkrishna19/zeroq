import { useState } from 'react';
import { Box, UnstyledButton, Text } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import styles from './SearchButton.module.css';
import { SearchModal } from '../searchModal/SearchModal';

export function SearchButton({ sidebarCollapsed }) {
  const [searchModalOpened, setSearchModalOpened] = useState(false);

  return (
    <>
      <Box className={`${styles.searchButtonContainer} ${sidebarCollapsed ? styles.sidebarCollapsed : styles.sidebarExpanded}`}>
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

      <SearchModal
        opened={searchModalOpened}
        onClose={() => setSearchModalOpened(false)}
      />
    </>
  );
}
