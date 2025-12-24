# Dogger 2.0 - Backend Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- pip (Python package manager)

### Installation Steps

1. **Create Virtual Environment**
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup PostgreSQL Database**
```bash
# Create database
createdb dogger_db

# Or using psql:
psql -U postgres
CREATE DATABASE dogger_db;
\q
```

4. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run Migrations**
```bash
python manage.py makemigrations clinic
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Create Media Directories**
```bash
mkdir -p media/patients/photos
mkdir -p media/patients/qr
mkdir -p media/signatures
mkdir -p media/lab/results
mkdir -p logs
```

8. **Run Development Server**
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

---

## 🔑 Environment Variables

Required variables in `.env`:
```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=dogger_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# CORS (Frontend URLs)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# OpenAI Whisper (for voice transcription)
OPENAI_API_KEY=sk-your-openai-key-here

# Clinic Info
CLINIC_PHONE=+91-9876543210
CLINIC_EMAIL=contact@dogger.clinic
CLINIC_LICENSE=VET-LICENSE-123
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user info

### Patients
- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Create new patient (multipart/form-data)
- `GET /api/patients/{id}/` - Get patient details
- `PATCH /api/patients/{id}/` - Update patient
- `DELETE /api/patients/{id}/` - Delete patient
- `GET /api/patients/{id}/medical_history/` - Get complete medical history
- `POST /api/patients/{id}/upload_photo/` - Upload patient photo

### Owners
- `GET /api/owners/` - List all owners
- `POST /api/owners/` - Create new owner
- `GET /api/owners/{id}/` - Get owner details
- `GET /api/owners/{id}/patients/` - Get owner's patients

### Medical Records
- `GET /api/medical-records/` - List medical records
- `POST /api/medical-records/` - Create consultation record
- `GET /api/medical-records/{id}/` - Get record details
- `POST /api/medical-records/{id}/add_prescription/` - Add prescription

### Vaccinations
- `GET /api/vaccinations/` - List vaccinations
- `POST /api/vaccinations/` - Record new vaccination
- `GET /api/vaccinations/due_soon/` - Get upcoming vaccinations

### Lab Tests
- `GET /api/lab-tests/` - List lab tests
- `POST /api/lab-tests/` - Order new lab test
- `POST /api/lab-tests/{id}/update_results/` - Update test results

### Voice Transcription
- `POST /api/whisper/transcribe/` - Transcribe audio to English text
  - Body: multipart/form-data with 'audio' field
  - Returns: `{ text: "...", language: "ta/en" }`

### Passbook & Sharing
- `GET /api/patients/{id}/passbook/` - Get patient health passbook
- `POST /api/patients/{id}/share-url/` - Create shareable link
- `GET /api/share/{short_code}/` - Access shared content (public)

### PDF Generation
- `GET /api/pdf/prescription/{record_id}/` - Download prescription PDF
- `GET /api/pdf/vaccination/{vaccination_id}/` - Download vaccination certificate
- `GET /api/pdf/health-certificate/{patient_id}/` - Download health certificate
- `GET /api/pdf/lab-report/{lab_test_id}/` - Download lab report

### Analytics
- `GET /api/analytics/overview/` - Dashboard KPIs
- `GET /api/analytics/revenue/?days=30` - Revenue analytics

### Search
- `GET /api/search/?q=keyword` - Global search

---

## 🎤 Whisper Integration (Tamil → English)

### Backend Implementation

The backend handles Whisper transcription in `WhisperTranscribeView`:

1. **Client sends audio file** (FormData with 'audio' field)
2. **Backend calls OpenAI Whisper API** with language auto-detection
3. **If Tamil detected**, translate to English using Whisper's translate endpoint
4. **Return English text** to frontend

### Expected Request Format
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.webm');

const response = await fetch('/api/whisper/transcribe/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: formData
});

const data = await response.json();
// data.text = English transcription
```

### Response Format
```json
{
  "success": true,
  "data": {
    "text": "Coughing for three days",
    "original_text": "மூன்று நாட்களாக இருமல்",
    "language": "ta",
    "translated": true
  }
}
```

---

## 📄 PDF Generation

PDFs are generated using ReportLab with:
- Clinic letterhead (emerald green header)
- Professional layout
- Patient info box
- Content sections
- Footer with signature area and clinic seal

All PDFs are A4 size and print-ready.

---

## 🔐 Authentication & Permissions

### JWT Authentication
- Access tokens expire after 8 hours
- Refresh tokens expire after 7 days
- Include token in header: `Authorization: Bearer <token>`

### User Roles
- `admin` - Full access
- `doctor` - Medical records, prescriptions
- `receptionist` - Patient registration, payments
- `lab_tech` - Lab test management

---

## 🗄️ Database Schema

### Main Models
- **User** - Extended Django user with role and clinic info
- **Owner** - Pet owners/clients
- **Patient** - Pets with photo, QR code, medical summary
- **MedicalRecord** - Consultations/visits
- **Prescription** - Medications linked to medical records
- **Vaccination** - Vaccination records with certificates
- **LabTest** - Laboratory tests with results
- **SharedURL** - Short-lived signed URLs for sharing
- **Payment** - Billing and payment records
- **Subscription** - Premium feature access
- **AuditLog** - Action tracking for compliance

---

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test clinic

# With coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment (Render)

### Build Command
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### Start Command
```bash
gunicorn dogger.wsgi:application
```

### Environment Variables (Production)
Set all variables from `.env.example` in Render dashboard:
- Set `DEBUG=False`
- Set proper `ALLOWED_HOSTS`
- Use production database credentials
- Add HTTPS URLs to `CORS_ALLOWED_ORIGINS`

---

## 📝 Management Commands

### Create Sample Data (Development)
```bash
python manage.py shell

from clinic.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# Create doctor user
doctor = User.objects.create_user(
    username='doctor1',
    password='password123',
    first_name='Dr. John',
    last_name='Smith',
    role='doctor',
    email='doctor@example.com'
)

# Create owner
owner = Owner.objects.create(
    name='Raj Kumar',
    phone='9876543210',
    email='raj@example.com',
    city='Cumbum'
)

# Create patient
patient = Patient.objects.create(
    pet_name='Bruno',
    species='dog',
    breed='Labrador',
    gender='male',
    owner=owner,
    created_by=doctor
)
```

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check credentials in .env
```

### Migration Issues
```bash
# Reset migrations (development only!)
python manage.py migrate clinic zero
rm clinic/migrations/0*.py
python manage.py makemigrations clinic
python manage.py migrate
```

### Media Files Not Serving
```bash
# Check MEDIA_ROOT exists
mkdir -p media

# In development, Django serves media automatically
# In production, use Nginx or cloud storage (S3)
```

### CORS Errors
```bash
# Add frontend URL to CORS_ALLOWED_ORIGINS in settings.py
# Example: http://localhost:5173
```

---

## 📚 Additional Resources

- Django REST Framework Docs: https://www.django-rest-framework.org/
- ReportLab User Guide: https://www.reportlab.com/docs/reportlab-userguide.pdf
- OpenAI Whisper API: https://platform.openai.com/docs/guides/speech-to-text

---

## 🔄 Next Steps

After backend setup:
1. ✅ Verify API endpoints with Postman/Thunder Client
2. ✅ Test authentication flow
3. ✅ Create sample data
4. ✅ Move to **STAGE 2: Frontend Setup**