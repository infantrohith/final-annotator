# Final Annotator - Production Ready Image Annotation Tool

A robust, feature-rich image annotation platform built for computer vision projects. Designed for production use with a modern tech stack, smooth canvas interactions, and comprehensive annotation capabilities.

## 🚀 Features

### Core Features
- **Image Upload**: Single and batch upload with drag-and-drop support
- **Smooth Annotation Canvas**: High-performance canvas with no lag or glitches
- **Multiple Annotation Types**: Bounding boxes, polygons, and point annotations
- **Vision Tasks**: Auto-annotation with object detection and classification
- **Model Training**: Train custom ML models on annotated data
- **Dataset Export**: Export in COCO, YOLO, and Pascal VOC formats
- **Project Management**: Organize images into projects
- **Responsive Design**: Mobile-friendly interface

### Technical Features
- ✅ Full authentication system with JWT tokens
- ✅ Database connection pooling for optimal performance
- ✅ Image lazy loading and pagination
- ✅ Real-time loading spinners and progress indicators
- ✅ Toast notifications for user feedback
- ✅ Keyboard shortcuts for efficient workflow
- ✅ Error handling with proper HTTP status codes
- ✅ Input validation (frontend + backend)
- ✅ SQL injection prevention
- ✅ File type validation
- ✅ Efficient canvas rendering

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **SQLAlchemy**: Powerful SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Robust relational database
- **PyTorch**: Deep learning framework for model training
- **OpenCV**: Computer vision library

### Frontend
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **Zustand**: Lightweight state management
- **Tailwind CSS**: Utility-first CSS framework
- **Canvas API**: High-performance drawing
- **Axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Production web server (optional)

## 📋 Prerequisites

- Docker and Docker Compose
- Git
- 4GB+ RAM recommended
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd final-annotator
```

### 2. Configure Environment

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Backend Settings
BACKEND_PORT=8000
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_ORIGINS=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:password@db:5432/final_annotator
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=final_annotator

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Settings
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:8000
```

**⚠️ IMPORTANT**: Change the `SECRET_KEY` and `JWT_SECRET_KEY` to random, secure values in production!

### 3. Build and Start

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Create Your First Account

1. Navigate to http://localhost:3000
2. Click "Register"
3. Create your account
4. Start annotating!

## 📖 Usage Guide

### Creating a Project

1. Click "New Project" button
2. Enter project name and description
3. Click "Create"

### Uploading Images

1. Click "Upload Images"
2. Drag and drop images or click to browse
3. Select single or multiple images
4. Click "Upload"

### Annotating Images

1. Click on any image to open the annotation canvas
2. Set your label in the left sidebar
3. Press `B` or click "Bounding Box" to enable drawing mode
4. Click and drag on the image to create annotations
5. Annotations are automatically saved

### Keyboard Shortcuts

- `B` - Toggle bounding box mode
- `Delete` - Delete selected annotation
- `Ctrl+S` - Save (auto-saves)
- `Esc` - Cancel drawing mode

### Auto-Annotation

1. Open an image in the annotation canvas
2. Click "Auto Annotate"
3. Wait for the AI to detect objects
4. Review and adjust annotations as needed

### Exporting Dataset

1. Navigate to a project
2. Click "Export"
3. Choose format (COCO, YOLO, or Pascal VOC)
4. Download the exported dataset

### Training a Model

1. Create annotations for your images
2. Navigate to the Models section
3. Click "Create Model"
4. Configure training parameters
5. Click "Train"
6. Monitor training progress

## 🔧 Development

### Backend Development

```bash
# Enter backend container
docker-compose exec backend bash

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run tests
pytest

# Format code
black .
```

### Frontend Development

```bash
# Enter frontend container
docker-compose exec frontend sh

# Install new package
npm install <package-name>

# Lint code
npm run lint

# Build for production
npm run build
```

## 📁 Project Structure

```
final-annotator/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configuration
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── utils/            # Utility functions
│   │   └── main.py           # FastAPI app
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── store/            # State management
│   │   ├── hooks/            # Custom hooks
│   │   ├── types/            # TypeScript types
│   │   └── utils/            # Utility functions
│   └── package.json          # Node dependencies
├── docker/
│   ├── backend.Dockerfile    # Backend container
│   └── frontend.Dockerfile   # Frontend container
├── docker-compose.yml        # Multi-container setup
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection prevention via SQLAlchemy
- File type validation
- CORS configuration
- Environment-based secrets
- Input sanitization

## 🚀 Production Deployment

### Option 1: Docker (Recommended)

1. Set production environment variables
2. Build with production flag:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Manual Deployment

**Backend:**
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm install
npm run build
# Serve dist/ with nginx or similar
```

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart db

# View database logs
docker-compose logs db
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Backend API Errors

```bash
# Check backend logs
docker-compose logs backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Restart backend
docker-compose restart backend
```

### Port Already in Use

```bash
# Change ports in .env file
BACKEND_PORT=8001
FRONTEND_PORT=3001

# Restart services
docker-compose down
docker-compose up -d
```

## 🧪 Testing

### Run Backend Tests

```bash
docker-compose exec backend pytest
```

### Run Frontend Tests

```bash
docker-compose exec frontend npm test
```

## 📊 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- React team for the UI library
- All open-source contributors

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at /docs

---

**Built with ❤️ for the Computer Vision Community**
