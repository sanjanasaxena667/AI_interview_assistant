# AI Interview Coach

A modern, polished React web application for AI-driven interview preparation. Practice your interview skills with personalized AI coaching, get real-time feedback, and track your progress over time. Built an end-to-end AI-powered interview simulator using Ollama to run LLMs locally, enabling resume & job description analysis via Tesseract OCR and generating role-specific technical and behavioral questions. Developed a real-time voice interaction pipeline leveraging OpenAI Whisper for speech-to-text and Microsoft Edge TTS for AI-driven interviewer voice, supporting both voice and text-based responses.Engineered an automated evaluation & analytics system using the Qwen model for answer scoring (0–10 scale), feedback generation, and performance tracking dashboards to deliver actionable interview insights.

## Features

- 🎨 **Beautiful Modern UI** - Warm, welcoming color palette with glassmorphism effects
- 🌓 **Dark/Light Theme** - Seamless theme toggle with smooth transitions
- 📊 **Comprehensive Analytics** - Track your progress with detailed charts and metrics
- 🎯 **Multiple Interview Types** - Technical, HR/Behavioral, and Behavioral interviews
- 🎥 **Multi-modal Analysis** - Video, audio, and text-based interview modes
- 📈 **Progress Tracking** - Monitor your improvement over time
- 💬 **Real-time Feedback** - Get instant AI-powered feedback on your responses

## Tech Stack

- **React** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **React Router** - Navigation

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-interviewer
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable components
│   └── Navbar.tsx   # Navigation bar with theme toggle
├── contexts/         # React contexts
│   └── ThemeContext.tsx  # Theme management
├── pages/            # Page components
│   ├── LandingPage.tsx
│   ├── UploadPage.tsx
│   ├── SetupPage.tsx
│   ├── LoadingPage.tsx
│   ├── InterviewRoom.tsx
│   ├── FeedbackPage.tsx
│   └── DashboardPage.tsx
├── App.tsx           # Main app component
├── main.tsx          # Entry point
└── style.css         # Global styles and Tailwind directives
```

## Color Scheme

### Light Theme
- Primary: Warm coral (#FF6B6B) to peachy orange gradient
- Secondary: Soft amber (#FFA94D)
- Background: Cream/off-white (#FFF8F3)
- Text: Warm dark grey (#2D3436)

### Dark Theme
- Primary: Vibrant coral (#FF8787)
- Secondary: Golden amber (#FFB84D)
- Background: Deep warm charcoal (#1A1A1D)
- Text: Warm white (#FAF3E0)

## Features Overview

### Landing Page
- Hero section with animated 3D avatar
- Feature cards showcasing key capabilities
- Call-to-action buttons

### Upload Page
- Drag-and-drop file uploads for resume and job description
- Progress indicators
- Role and experience level selection

### Setup Page
- Interview type selection (Technical, HR, Behavioral)
- Mode selection (Video, Audio, Text)
- Difficulty slider
- Estimated time display

### Loading Page
- Animated progress indicators
- Step-by-step status updates
- Smooth transitions

### Interview Room
- Split-screen layout
- Question display with timer
- Video preview and recording controls
- Microphone level visualizer
- Progress tracking

### Feedback Page
- Overall score with circular progress chart
- Category scores (Verbal, Non-verbal, Technical)
- Performance over time chart
- Question-by-question breakdown
- Improvement suggestions

### Dashboard
- Statistics overview
- Growth curve visualization
- Recent sessions table
- Filtering options

## Customization

### Colors
Edit `tailwind.config.js` to customize the color palette.

### Fonts
The app uses Google Fonts (Outfit, Space Grotesk). You can change fonts in `index.html` and `tailwind.config.js`.

### Animations
Framer Motion animations can be customized in individual components.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

