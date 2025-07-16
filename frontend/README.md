# ZeroQ Frontend

ZeroQ is a modern employee journey management platform. This frontend is built with **React** and uses **Mantine** for UI components, styling, and layouts. It features onboarding/offboarding workflows, AI-powered assistants, analytics, and seamless third-party integrations.

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

### Authentication Endpoints
| Endpoint                                      | Method | Description                                 | Used In |
| ---------------------------------------------- | ------ | ------------------------------------------- | ------- |
| `/api/auth/user/`                             | GET    | Get current authenticated user              | Dashboard.jsx |
| `/api/auth/login/`                            | POST   | User login                                  | ApiService.login() |
| `/api/auth/logout/`                           | POST   | User logout                                 | ApiService.logout() |
| `/api/auth/csrf/`                             | GET    | Get CSRF token for authentication          | ApiService.getCSRFToken() |

### User Management Endpoints
| Endpoint                                      | Method | Description                                 | Used In |
| ---------------------------------------------- | ------ | ------------------------------------------- | ------- |
| `/api/users/`                                 | GET    | List all users                              | OnBoardingFormPage.jsx, OffBoardingFormPage.jsx, UpdateFormPage.jsx |
| `/api/users/{userId}/`                        | GET    | Get user details by ID                      | Dashboard.jsx |

### Journey Template Endpoints
| Endpoint                                      | Method | Description                                 | Used In |
| ---------------------------------------------- | ------ | ------------------------------------------- | ------- |
| `/api/boarding/templates/`                    | GET    | List all journey templates (with filters)  | OnBoardingTemplate.jsx, OffBoardingTemplate.jsx |
| `/api/boarding/templates/`                    | POST   | Create a new journey template               | OnBoardingFormPage.jsx, OffBoardingFormPage.jsx, OffBoardingForm.jsx |
| `/api/boarding/templates/{templateId}/`       | GET    | Get a journey template by ID                | UpdateFormPage.jsx, UpdateOffBoardingFormPage.jsx |
| `/api/boarding/templates/{templateId}/`       | PUT    | Update a journey template by ID             | UpdateFormPage.jsx, UpdateOffBoardingFormPage.jsx |
| `/api/boarding/templates/{templateId}/`       | DELETE | Delete a journey template by ID             | OnBoardingTemplate.jsx, OffBoardingTemplate.jsx |

### Organization Data Endpoints
| Endpoint                                      | Method | Description                                 | Used In |
| ---------------------------------------------- | ------ | ------------------------------------------- | ------- |
| `/api/accounts/`                              | GET    | List all accounts                           | OnBoardingFormPage.jsx, OffBoardingFormPage.jsx, OffBoardingForm.jsx, UpdateFormPage.jsx |
| `/api/boarding/templates/departments/`        | GET    | List all departments                        | OnBoardingTemplate.jsx, OffBoardingTemplate.jsx |
| `/api/boarding/templates/business_units/`     | GET    | List all business units                     | OnBoardingTemplate.jsx, OffBoardingTemplate.jsx |

### Query Parameters Used
- **For Journey Templates (`/api/boarding/templates/`)**:
  - `journey_type`: Filter by 'onboarding' or 'offboarding'
  - `department`: Filter by department
  - `business_unit`: Filter by business unit
  - `is_active`: Filter by active/draft status

### Authentication Headers
All API requests include:
- `Authorization: Bearer {token}` (from localStorage)
- `X-CSRFToken: {csrfToken}` (obtained from `/api/auth/csrf/`)
- `Content-Type: application/json`

> **Note:** All endpoints are prefixed with `http://localhost:8000` in development mode.

## Screenshots

### Employee Journeys

![Employee Journeys Screenshot](./screenshots/employee-journeys.png)

### Stats

![Stats Screenshot](./screenshots/stats.png)

**Made with Mantine & React.**