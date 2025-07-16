# ZeroQ Frontend

ZeroQ is a modern employee journey management platform. This frontend is built with **React** and uses **Mantine** for UI components, styling, and layouts. It features onboarding/offboarding workflows, AI-powered assistants, analytics, and seamless third-party integrations.

## Features

- Employee onboarding & offboarding journey templates
- AI-powered assistant carousel
- Analytics dashboards
- Integration with external apps (HappyFox, BambooHR, Pipedrive, etc.)
- Responsive layouts with Mantine
- Protected routes and authentication
- Command/search modal (Cmd+K)
- Custom theming and standardized spacing

## Tech Stack

- [React](https://react.dev/)
- [Mantine](https://mantine.dev/)
- [Vite](https://vitejs.dev/)
- [Swiper](https://swiperjs.com/) (carousel)
- [Tabler Icons](https://tabler-icons.io/)
- [React Router](https://reactrouter.com/)
- [React Hot Toast](https://react-hot-toast.com/)

## Getting Started

### Prerequisites

- Node.js (v18 or above recommended)
- npm or yarn

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-org/zeroq.git
   cd zeroq/frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install

   ```

### Running the Development Server

```bash
npm run dev

```

- The app will be available at [http://localhost:5173](http://localhost:5173) (default Vite port).

### Building for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── theme.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── README.md
└── ...
```

## Usage Notes

- **Authentication:** Uses localStorage for auth token management.
- **Protected Routes:** Only authenticated users can access dashboard and journey pages.
- **Search Modal:** Press `Cmd+K` (Mac) or `Ctrl+K` (Windows/Linux) to open the command/search modal.
- **Custom Theme:** All spacing, colors, and component overrides are managed in `src/theme.js`.

**Made with Mantine & React.**