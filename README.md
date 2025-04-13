# VetAssist

A modern web application that helps veterinarians make informed clinical decisions by providing quick access to drug interaction data, dosage calculations, and differential diagnostics.

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Available Scripts](#available-scripts)
- [Project Scope](#project-scope)
- [Project Status](#project-status)
- [License](#license)

## Project Overview

VetAssist is designed to support veterinarians in their daily clinical practice by streamlining the medical decision-making process. The application addresses several key challenges that veterinarians face:

1. Lack of quick access to drug interaction information
2. Difficulty in precise dosage calculation for different animal species
3. Limited access to differential diagnostic information
4. Time constraints during visits

VetAssist solves these problems by providing three core modules:

- **Drug Interaction Search**: Check potential interactions between various medications
- **Dosage Calculator**: Calculate precise drug dosages based on animal weight and species
- **Treatment Vademecum**: Access information about potential conditions based on differential diagnostics

The application aims to save time for veterinary practitioners and minimize medical errors related to incorrect drug dosing or incomplete knowledge of potential health issues.

## Tech Stack

### Frontend
- **Astro 5**: Modern framework for building fast websites with hybrid static/dynamic rendering
- **React 19**: UI component library for building interactive interfaces
- **TypeScript 5**: Type-safe JavaScript for better code quality
- **Tailwind 4**: Utility-first CSS framework for responsive design
- **Shadcn/ui**: Component library built on Tailwind CSS

### Backend
- **Python**: Versatile programming language for algorithm implementation and AI integration
- **Django**: Web framework with built-in admin panel and authentication system

### Database
- **PostgreSQL**: Advanced relational database system for storing complex medication data

### AI Integration
- **Openrouter.ai**: AI service for flexible model selection and provider switching

### CI/CD and Hosting
- **GitHub Actions**: Automated CI/CD pipelines
- **DigitalOcean**: Cloud hosting with Docker containerization

## Getting Started

### Prerequisites

- Node.js v22.14.0 (recommended to use [nvm](https://github.com/nvm-sh/nvm))
- Python 3.8+ (for Django backend)
- PostgreSQL 13+

### Frontend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vetassist.git
   cd vetassist
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:4321`

### Backend Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the PostgreSQL database:
   ```bash
   # Create database and apply migrations
   python manage.py migrate
   ```

4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

## Available Scripts

In the project directory, you can run:

- `npm run dev`: Starts the Astro development server
- `npm run build`: Builds the application for production
- `npm run preview`: Preview the production build locally
- `npm run astro`: Run astro CLI commands
- `npm run lint`: Run ESLint to find problems in your code
- `npm run lint:fix`: Fix problems automatically when possible
- `npm run format`: Format code with Prettier

## Project Scope

### Key Features

1. **Drug Interaction Search Module**
   - Input multiple medications
   - Receive AI-generated interaction information
   - Add context to queries
   - Rate responses with thumbs up/down

2. **Dosage Calculator Module**
   - Select medication from predefined list
   - Input animal weight
   - Choose animal species and target unit
   - Display calculated dosage with conversion between units
   - Rate results with thumbs up/down

3. **Treatment Vademecum Module**
   - Enter keywords for diagnostic factors
   - Input values for factors
   - Generate AI-powered list of potential conditions
   - Add multiple factors simultaneously
   - Rate results with thumbs up/down

4. **User Account Management**
   - User registration and login
   - Password change and reset
   - Account deletion

### Not Included in MVP

- Advanced appointment management or treatment calendar
- Advanced patient data analysis
- Complex frontend design
- Notification system
- Integration with external veterinary hospital systems
- Custom medication database entries
- Advanced reporting
- Community features or discussion forums
- Mobile application (MVP is web-only)

## Project Status

VetAssist is currently in MVP (Minimum Viable Product) development stage. The application focuses on providing core functionality with a clean, usable interface rather than advanced features or complex design.

Version: 0.0.1

## License

This project is licensed under the MIT License - see the LICENSE file for details.
