import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Mousewheel } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import styles from './AgentCarousel.module.css';

const onBoardingAgentData = [
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
	{
		title: 'Team Introducer',
		description: 'Introduces team members and structure.',
	},
	{
		title: 'Team Introducer',
		description: 'Introduces team members and structure.',
	},
];

const offBoardingAgentData = [
	{
		title: 'Exit Documentation',
		description: 'Manages exit paperwork and compliance requirements.',
	},
	{
		title: 'Asset Recovery',
		description: 'Tracks and manages return of company assets.',
	},
	{
		title: 'Access Revocation',
		description: 'Handles system access deactivation and security clearance.',
	},
	{
		title: 'Knowledge Transfer',
		description: 'Facilitates documentation and handover of responsibilities.',
	},
	{
		title: 'Exit Interview',
		description: 'Conducts exit interviews and collects feedback.',
	},
	{
		title: 'Final Payroll',
		description: 'Manages final payroll processing and tax documentation.',
	},
	{
		title: 'Benefits Cancellation',
		description: 'Assists with cancellation of benefits and subscriptions.',
	},
];

function GradientSparkleIcon() {
	return (
		<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28">
			<defs>
				<linearGradient
					id="gradient_0"
					gradientUnits="userSpaceOnUse"
					x1="21.296358"
					y1="11.796358"
					x2="-2.2963583"
					y2="11.796358"
				>
					<stop offset="0" stopColor="#4D79FF" />
					<stop offset="1" stopColor="#5F1ACD" />
				</linearGradient>
			</defs>
			<path
				fill="url(#gradient_0)"
				transform="matrix(0.707107 0.707107 -0.707107 0.707107 13.435 2.95639e-05)"
				d="M2.7824855 16.217514L2.7824855 16.217514L2.7824855 16.217514C5.1708455 12.057608 5.1708455 6.9423923 2.7824855 2.7824855L2.7824855 2.7824855L2.7824855 2.7824855C6.9423923 5.1708455 12.057608 5.1708455 16.217514 2.7824855L16.217514 2.7824855L16.217514 2.7824855C13.829154 6.9423923 13.829154 12.057608 16.217514 16.217514L16.217514 16.217514L16.217514 16.217514C12.057608 13.829154 6.9423923 13.829154 2.7824855 16.217514Z"
			/>
		</svg>
	);
}

const AgentCarousel = ({ onSwiperInit, onSlideChange, journeyType = 'On-boarding' }) => {
	const agentData =
		journeyType === 'Off-boarding' ? offBoardingAgentData : onBoardingAgentData;

	return (
		<Swiper
			modules={[Navigation, Mousewheel]}
			spaceBetween={6}
			onSwiper={onSwiperInit}
			onSlideChange={onSlideChange}
			className={styles.swiper}
			mousewheel={{ forceToAxis: true }}
			breakpoints={{
				320: {
					slidesPerView: 1,
					spaceBetween: 12,
				},
				480: {
					slidesPerView: 1.3,
					spaceBetween: 14,
				},
				768: {
					slidesPerView: 1.8,
					spaceBetween: 12,
				},
				1024: {
					slidesPerView: 2.5,
					spaceBetween: 12,
				},
				1200: {
					slidesPerView: 3,
					spaceBetween: 12,
				},
				1400: {
					slidesPerView: 3.5,
					spaceBetween: 10,
				},
			}}
			freeMode={false}
			watchSlidesProgress={true}
			loop={false}
		>
			{agentData.map((agent, index) => (
				<SwiperSlide key={index} className={styles.swiperSlide}>
					<div className={styles.card}>
						<div className={styles.cardContent}>
							<div className={styles.iconContainer}>
								<GradientSparkleIcon />
							</div>
							<h3 className={styles.cardTitle}>{agent.title}</h3>
							<p className={styles.cardDescription}>
								{agent.description}
							</p>
						</div>
					</div>
				</SwiperSlide>
			))}
		</Swiper>
	);
};

export default AgentCarousel;