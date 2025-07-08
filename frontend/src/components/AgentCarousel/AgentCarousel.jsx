import { useState } from 'react';
import { Box, Text, Group, ActionIcon } from '@mantine/core';
import { Carousel } from '@mantine/carousel';
import { IconChevronLeft, IconChevronRight, IconSparkles } from '@tabler/icons-react';
import styles from './AgentCarousel.module.css';

const agentData = [
	{
		title: 'Benefits Explainer',
		description: 'Explains benefits packages and enrollment options.',
	},
	{
		title: 'Workspace Setup',
		description: 'Guides through workspace and tools setup.',
	},
	{
		title: 'System Access',
		description: 'Helps with system access requests and tracking.',
	},
	{
		title: 'Tax Form Helper',
		description: 'Assists with tax form completion and filing.',
	},
	{
		title: 'Training Scheduler',
		description: 'Schedules and tracks required training sessions.',
	},
	{
		title: 'Team Introducer',
		description: 'Introduces team members and structure.',
	},
];

const AgentCarousel = () => {
	const [embla, setEmbla] = useState(null);
	const [canScrollPrev, setCanScrollPrev] = useState(false);
	const [canScrollNext, setCanScrollNext] = useState(true);

	const handlePrev = () => {
		if (embla) embla.scrollPrev();
	};

	const handleNext = () => {
		if (embla) embla.scrollNext();
	};

	const handleEmblaChange = (emblaApi) => {
		setCanScrollPrev(emblaApi.canScrollPrev());
		setCanScrollNext(emblaApi.canScrollNext());
	};

	return (
		<Box className={styles.container}>
			<Group gap='sm' mb='md'>
				<IconSparkles size={20} color='#6366f1' />
				<Text className={styles.title}>
					AI-powered assistants to enhance the onboarding experience.
				</Text>
			</Group>

			<Box className={styles.carouselContainer}>
				<ActionIcon
					variant='outline'
					size='sm'
					onClick={handlePrev}
					disabled={!canScrollPrev}
					className={styles.arrowButton}
					style={{
						position: 'absolute',
						left: '10px',
						top: '50%',
						transform: 'translateY(-50%)',
						zIndex: 1,
					}}
				>
					<IconChevronLeft size={16} />
				</ActionIcon>

				<Carousel
					getEmblaApi={setEmbla}
					onSlide={handleEmblaChange}
					slideSize='280px'
					slideGap='16px'
					align='start'
					slidesToScroll={1}
					withControls={false}
					withIndicators={false}
					loop={false}
					containScroll='trimSnaps'
					className={styles.carousel}
				>
					{agentData.map((agent, index) => (
						<Carousel.Slide key={index}>
							<Box className={styles.card}>
								<Box className={styles.iconContainer}>
									<IconSparkles size={20} color='#6366f1' />
								</Box>
								<Text className={styles.cardTitle}>{agent.title}</Text>
								<Text className={styles.cardDescription}>
									{agent.description}
								</Text>
							</Box>
						</Carousel.Slide>
					))}
				</Carousel>

				<ActionIcon
					variant='outline'
					size='sm'
					onClick={handleNext}
					disabled={!canScrollNext}
					className={styles.arrowButton}
					style={{
						position: 'absolute',
						right: '10px',
						top: '50%',
						transform: 'translateY(-50%)',
						zIndex: 1,
					}}
				>
					<IconChevronRight size={16} />
				</ActionIcon>
			</Box>
		</Box>
	);
};

export default AgentCarousel;