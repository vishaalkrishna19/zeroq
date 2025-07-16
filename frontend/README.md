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

## API Endpoints

Below are the main backend API endpoints used by the frontend:

| Endpoint                                      | Method | Description                                 |
| ---------------------------------------------- | ------ | ------------------------------------------- |
| `/api/auth/user/`                             | GET    | Get current authenticated user              |
| `/api/users/`                                 | GET    | List all users                              |
| `/api/users/{userId}/`                        | GET    | Get user details by ID                      |
| `/api/accounts/`                              | GET    | List all accounts                           |
| `/api/journey-templates/`                     | GET    | List all journey templates                  |
| `/api/journey-templates/`                     | POST   | Create a new journey template               |
| `/api/journey-templates/{templateId}/`        | GET    | Get a journey template by ID                |
| `/api/journey-templates/{templateId}/`        | PATCH  | Update a journey template by ID             |
| `/api/journey-templates/{templateId}/`        | DELETE | Delete a journey template by ID             |
| `/api/departments/`                           | GET    | List all departments                        |
| `/api/business-units/`                        | GET    | List all business units                     |
| `/api/auth/login/`                            | POST   | User login                                  |
| `/api/auth/logout/`                           | POST   | User logout                                 |
| `/api/auth/password/reset/`                   | POST   | Request password reset                      |
| `/api/auth/password/set/`                     | POST   | Set new password                            |

> **Note:** Some endpoints may be prefixed with `/api/v1/` depending on your backend configuration.

**Made with Mantine & React.**