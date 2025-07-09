import { useState } from 'react';
import {
  Box,
  Group,
  ScrollArea,
  UnstyledButton,
  Text,
  ThemeIcon,
  ActionIcon,
  Stack,
} from '@mantine/core';
import {
  IconHome,
  IconUsers,
  IconDeviceDesktop,
  IconSettings,
  IconCreditCard,
  IconChartBar,
  IconScale,
  IconBuilding,
  IconBriefcase,
  IconShield,
  IconApps,
  IconSearch,
  IconChevronLeft,
  IconChevronRight,
  IconChevronDown,
  IconUserCircle,
  IconUserCheck,
  IconRoad,
  IconHeart,
  IconQuestionMark,
  IconBell,
} from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import styles from './Sidebar.module.css';
import { SearchModal } from '../searchModal/SearchModal';

const mockdata = [
  { label: 'Home', icon: IconHome, active: true },
  {
    label: 'HR',
    icon: IconUsers,
    initiallyOpened: false,
    links: [
      { label: 'Employee Journeys', icon: IconRoad },
      { label: 'Manager Hub', icon: IconUserCheck },
      { label: 'Employee Relations', icon: IconHeart },
      { label: 'Employee Center Pro', icon: IconUsers },
      { label: 'HR Case & Knowledge', icon: IconQuestionMark },
      { label: 'Announcements', icon: IconBell },
    ],
  },
//   { label: 'IT', icon: IconDeviceDesktop },
//   { label: 'Operations', icon: IconSettings },
//   { label: 'Finance', icon: IconCreditCard },
//   { label: 'Sales', icon: IconChartBar },
//   { label: 'Legal', icon: IconScale },
//   { label: 'Facilities', icon: IconBuilding },
//   { label: 'Marketing', icon: IconBriefcase },
//   { label: 'Security & Risk', icon: IconShield },
//   { label: 'Integrations', icon: IconApps },
];

function LinksGroup({ icon: Icon, label, links, active, collapsed, onHover, hoveredItem, activeSubItem, onClick }) {
  const hasLinks = Array.isArray(links);
  const isHovered = hoveredItem === label;
  const ChevronIcon = isHovered ? IconChevronDown : IconChevronRight;

  return (
    <Box className={styles.linkGroup}>
      <UnstyledButton
        onClick={onClick}
        onMouseEnter={() => hasLinks && onHover(label)}
        onMouseLeave={() => hasLinks && onHover(null)}
        className={`${styles.linkButton} ${active ? styles.linkButtonActive : ''}`}
        data-submenu-trigger={hasLinks ? label : undefined}
      >
        <Group justify="space-between" gap={0}>
          <Box style={{ display: 'flex', alignItems: 'center' }}>
            <Icon size={20} />
            {!collapsed && <Text size='14px'  className='link-group-text' ml="sm">{label}</Text>}
          </Box>
          {hasLinks && !collapsed && (
            <ChevronIcon
              size={16}
              className={`${styles.chevronIcon} ${isHovered ? styles.chevronRotated : styles.chevronDefault}`}
            />
          )}
        </Group>
      </UnstyledButton>
    </Box>
  );
}

export function Sidebar({ collapsed, onToggle }) {
  const [hoveredItem, setHoveredItem] = useState(null);
  const [submenuPosition, setSubmenuPosition] = useState({ top: 0 });
  const [activeLabel, setActiveLabel] = useState('Home');
  const [activeSubItem, setActiveSubItem] = useState(null);
  const [searchModalOpened, setSearchModalOpened] = useState(false);
  const navigate = useNavigate();

  const handleHover = (label) => {
    if (label) {
      const trigger = document.querySelector(`[data-submenu-trigger="${label}"]`);
      if (trigger) {
        const rect = trigger.getBoundingClientRect();
        setSubmenuPosition({ top: rect.top });
      }
    }
    setHoveredItem(label);
  };

  const handleSubItemClick = (parentLabel, subLabel) => {
    setActiveLabel(parentLabel);
    setActiveSubItem(subLabel);
    setHoveredItem(null);
    // Navigation logic for Employee Journeys
    if (parentLabel === 'HR' && subLabel === 'Employee Journeys') {
      navigate('/dashboard/employee-journeys');
    }
    // Add more navigation logic for other subitems if needed
  };

  const links = mockdata.map((item) => (
    <Box key={item.label}>
      <LinksGroup 
        {...item} 
        collapsed={collapsed} 
        onHover={handleHover}
        hoveredItem={hoveredItem}
        active={activeLabel === item.label}
        activeSubItem={activeSubItem}
        onClick={
          !item.links
            ? () => {
                setActiveLabel(item.label);
                setActiveSubItem(null);
                if (item.label === 'Home') {
                  navigate('/');
                }
                // Add more navigation logic for other main links if needed
              }
            : undefined
        }
      />
      {/* Separator after Home */}
      {item.label === 'Home' && (
        <Box className={styles.separator} />
      )}
    </Box>
  ));

  return (
    <>
    <Box className={`${styles.sidebar} ${collapsed ? styles.sidebarCollapsed : styles.sidebarExpanded}`}>
      <ActionIcon
        onClick={onToggle}
        variant="filled"
        size="sm"
        className={styles.toggleButton}
      >
        {collapsed ? <IconChevronRight size={14} /> : <IconChevronLeft size={14} />}
      </ActionIcon>

      {/* Header */}
      <Box className={styles.header}>
        <Group gap="sm">
          <ThemeIcon size={30} color="transparent">
            <img src="https://zeroq.hfapp.net/logo.svg" width="20" height="20" alt="ZeroQ" />
          </ThemeIcon>
          {!collapsed && (
            <Text 
              size="xl" 
              fw={400} 
              c="white"
              className={`${styles.logoText} ${collapsed ? styles.logoTextHidden : ''}`}
            >
              ZeroQ
            </Text>
          )}
        </Group>
      </Box>

      <UnstyledButton onClick={() => setSearchModalOpened(true)} className={styles.askAnything}>
        <Group gap="sm" justify={collapsed ? "center" : undefined}>
          <IconSearch className='ask-icon' size={20} style={{ minWidth: 20, minHeight: 20 }} />
          {!collapsed && <Text size="sm">Ask Anything</Text>}
        </Group>
      </UnstyledButton>

      {/* Navigation Links */}
      <ScrollArea className={styles.scrollArea}>
        <Stack gap="xs">
          {links}
        </Stack>
      </ScrollArea>

      {/* Submenu Portal - positioned outside sidebar */}
      {hoveredItem && (
        <Box
          className={styles.submenuPortal}
          onMouseEnter={() => setHoveredItem(hoveredItem)}
          onMouseLeave={() => setHoveredItem(null)}
          style={{ 
            left: collapsed ? '55px' : '260px',
            top: submenuPosition.top,
            height: 'auto',
            bottom: 'auto'
          }}
        >
          {/* Transparent bridge */}
          <Box className={styles.submenuBridge} />
          
          {mockdata.find(item => item.label === hoveredItem)?.links && (
            <Box className={styles.submenuContent}>
              <Text size="sm" fw={500} c="white" mb="sm" ml="xs">
                {hoveredItem}
              </Text>
              <Box className={styles.separator} />
              <Stack gap='2px' mb='0'>
                {mockdata.find(item => item.label === hoveredItem)?.links?.map((link) => (
                  <UnstyledButton
                    key={link.label}
                    className={`${styles.submenuItem} ${activeLabel === hoveredItem && activeSubItem === link.label ? styles.linkButtonActive : ''}`}
                    onClick={() => handleSubItemClick(hoveredItem, link.label)}
                  >
                    <Group gap="sm">
                      <link.icon size={16} />
                      <Text size="sm">{link.label}</Text>
                    </Group>
                  </UnstyledButton>
                ))}
              </Stack>
            </Box>
          )}
        </Box>
      )}
    </Box>
    
    <SearchModal
        opened={searchModalOpened}
        onClose={() => setSearchModalOpened(false)}
      />
      </>
  );
}
