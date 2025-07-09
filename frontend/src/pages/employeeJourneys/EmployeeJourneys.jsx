import { Box, Group, ActionIcon, Text } from '@mantine/core';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';
import { useState } from 'react';
import {TopBar} from '../../components/topbar/Topbar';
import EmployeeHeader from '../../components/employeeHeader/EmployeeHeader';
import styles from './EmployeeJourneys.module.css';
import AgentCarousel from '../../components/AgentCarousel/AgentCarousel';
import OnBoardingTemplate from '../../components/onBoarding/OnBoardingTemplate';

function GradientSparkleIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28">
      <defs>
        <linearGradient id="gradient_0" gradientUnits="userSpaceOnUse" x1="21.296358" y1="11.796358" x2="-2.2963583" y2="11.796358">
          <stop offset="0" stopColor="#4D79FF"/>
          <stop offset="1" stopColor="#5F1ACD"/>
        </linearGradient>
      </defs>
      <path fill="url(#gradient_0)" transform="matrix(0.707107 0.707107 -0.707107 0.707107 13.435 2.95639e-05)" d="M2.7824855 16.217514L2.7824855 16.217514L2.7824855 16.217514C5.1708455 12.057608 5.1708455 6.9423923 2.7824855 2.7824855L2.7824855 2.7824855L2.7824855 2.7824855C6.9423923 5.1708455 12.057608 5.1708455 16.217514 2.7824855L16.217514 2.7824855L16.217514 2.7824855C13.829154 6.9423923 13.829154 12.057608 16.217514 16.217514L16.217514 16.217514L16.217514 16.217514C12.057608 13.829154 6.9423923 13.829154 2.7824855 16.217514Z"/>
    </svg>
  );
}

const EmployeeJourneys = () => {
  const [carouselRef, setCarouselRef] = useState(null);
  const [canScrollPrev, setCanScrollPrev] = useState(false);
  const [canScrollNext, setCanScrollNext] = useState(true);

  const handlePrev = () => {
    if (carouselRef) carouselRef.slidePrev();
  };

  const handleNext = () => {
    if (carouselRef) carouselRef.slideNext();
  };

  const handleSlideChange = (swiper) => {
    setCanScrollPrev(!swiper.isBeginning);
    setCanScrollNext(!swiper.isEnd);
  };

  return (
    <>
        <TopBar />
        <Box className={styles.container}>
        
        <Box className={styles.employeeHeader}>
            <EmployeeHeader />
        </Box>
        
        <Box className={styles.carouselBackground}>
          <Box className={styles.carouselHeader}>
            <Group gap="sm">
              <GradientSparkleIcon />
              <Text className={styles.carouselTitle}>
                AI-powered assistants to enhance the onboarding experience.
              </Text>
            </Group>
            
            <Group gap="xs">
              <ActionIcon
                variant="outline"
                size="sm"
                onClick={handlePrev}
                disabled={!canScrollPrev}
                className={styles.arrowButton}
              >
                <IconChevronLeft size={16} />
              </ActionIcon>
              <ActionIcon
                variant="outline"
                size="sm"
                onClick={handleNext}
                disabled={!canScrollNext}
                className={styles.arrowButton}
              >
                <IconChevronRight size={16} />
              </ActionIcon>
            </Group>
          </Box>
          
          <AgentCarousel 
            onSwiperInit={setCarouselRef}
            onSlideChange={handleSlideChange}
          />
        </Box>
        
        <OnBoardingTemplate />
        </Box>
    </>
  );
};

export default EmployeeJourneys;
