import { useState, useEffect } from 'react';
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
import { useNavigate, useLocation } from 'react-router-dom';
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
  const [activeLabel, setActiveLabel] = useState(null);
  const [activeSubItem, setActiveSubItem] = useState(null);
  const [searchModalOpened, setSearchModalOpened] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/dashboard') {
      setActiveLabel('Home');
      setActiveSubItem(null);
    } else if (location.pathname === '/dashboard/employee-journeys') {
      setActiveLabel('HR');
      setActiveSubItem('Employee Journeys');
    }
  }, [location.pathname]);

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

    if (parentLabel === 'HR' && subLabel === 'Employee Journeys') {
      navigate('/dashboard/employee-journeys');
    }

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
                  navigate('/dashboard');
                }
               
              }
            : undefined
        }
      />
    
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


      <Box className={styles.header}>
        <Group gap="sm">
          <ThemeIcon size={30} color="transparent">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 563 563" fill="none">
                  <rect width="563" height="563" rx="144" fill="white" fillOpacity="0.1"/>
                  <rect x="2" y="2" width="559" height="559" rx="142" stroke="white" strokeOpacity="0.1" strokeWidth="4"/>
                  <path d="M295.849 99.0146C395.827 100.281 476.483 181.721 476.483 282V294L476.469 296.365C476.015 332.209 465.254 365.567 447.016 393.616L499.739 441.364C513.657 453.969 514.723 475.471 502.118 489.39C489.513 503.308 468.012 504.373 454.094 491.768L307.159 358.701C293.241 346.096 292.177 324.595 304.781 310.677C317.386 296.759 338.887 295.693 352.806 308.298L395.558 347.016C403.815 331.151 408.483 313.121 408.483 294V282C408.483 218.487 356.996 167 293.483 167H269.483C252.313 167 236.022 170.765 221.389 177.512L168.611 129.29C196.919 110.554 230.739 99.4753 267.118 99.0146L269.483 98.9999H293.483L295.849 99.0146ZM170.615 223.23C160.37 240.429 154.483 260.527 154.483 282V294C154.483 355.207 202.3 405.244 262.616 408.796L332.659 472.794C320.779 475.385 308.468 476.825 295.849 476.985L293.483 477H269.483L267.118 476.985C167.927 475.729 87.7544 395.556 86.4979 296.365L86.4833 294V282C86.4833 242.825 98.7921 206.526 119.754 176.758L170.615 223.23ZM62.5565 74.3661C75.4049 61.0779 96.4626 60.5195 109.994 72.955L110.633 73.5565L130.132 92.4101L130.755 93.0282C143.639 106.133 143.79 127.198 130.941 140.486C118.093 153.775 97.0352 154.334 83.5038 141.898L82.8651 141.296L63.3671 122.443L62.744 121.825C49.8594 108.72 49.7082 87.6548 62.5565 74.3661Z" fill="white"/>
                </svg>
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

      <ScrollArea className={styles.scrollArea}>
        <Stack gap="xs">
          {links}
        </Stack>
      </ScrollArea>

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
