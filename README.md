# Django YouTube Uploader

## Overview
This Django application allows users to upload videos to YouTube using the YouTube Data API. It integrates Google OAuth2 for authentication and provides a simple interface for uploading videos.

---

## Features
- **Google OAuth2 Authentication**:
  - Users can log in using their Google accounts.
  - OAuth2 tokens are securely stored for authenticated API requests.
- **YouTube Video Upload**:
  - Users can upload videos directly to their YouTube channels.
  - Video metadata (title, description, tags, etc.) is customizable.
- **Role-Based Access**:
  - Only authenticated users can access the upload functionality.
- **Django Forms**:
  - A form-based interface for video uploads.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/django-youtube-uploader.git
cd django-youtube-uploader
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google OAuth2
- Obtain OAuth2 credentials from the [Google Cloud Console](https://console.cloud.google.com/).
- Download the `client_secret.json` file and place it in your project directory.
- Update the `settings.py` file with the path to your `client_secret.json` file:
  ```python
  GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = "path/to/client_secret.json"
  YT_JSON_FILE = "path/to/client_secret.json"
  YT_CLIENT_SECRET = "your-client-secret"
  ```

### 5. Configure the Database
Run migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Visit the application at `http://127.0.0.1:8000`.

---

## Usage

### 1. Log In
- Navigate to the home page.
- Log in using your Google account.

### 2. Upload a Video
- After logging in, click the "Add a video" button.
- Use the form to upload a video and provide metadata (title, description, tags, etc.).

### 3. View Results
- After uploading, you will be redirected to the results page.

---

## Project Structure
```
Django_youtube/
├── core/
│   ├── models.py        # Models for storing OAuth credentials
│   ├── views.py         # Views for authentication and video upload
│   ├── forms.py         # Form for video uploads
│   ├── templates/       # HTML templates for the application
├── users/
│   ├── templates/       # User-specific templates (e.g., index.html)
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

---

## Key Views

### 1. **Home View**
The `HomeView` provides a form for uploading videos to YouTube.

#### Code:
```python
class HomeView(FormView):
    template_name = 'home.html'
    form_class = YoutubeUploadForm

    def form_valid(self, form):
        file_name = form.cleaned_data['video'].temporary_file_path()
        credentials_dict = model_to_dict(GoogleOAuthCredential.objects.get(client_secret=settings.YT_CLIENT_SECRET))
        credential = credentials.Credentials(**credentials_dict)
        youtube = build('youtube', 'v3', credentials=credential)
        body = {
            'snippet': {
                'title': 'Video uploaded using django',
                'description': 'This video has been uploaded using Django and Youtube Data API.',
                'tags': 'django,api',
                'categoryId': '27'
            },
            'status': {
                'privacyStatus': 'unlisted'
            }
        }
        insert_request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=MediaFileUpload(file_name, chunksize=-1, resumable=True))
        response = insert_request.execute()
        return redirect('result/')
```

---

### 2. **Google OAuth2 Callback View**
Handles the OAuth2 callback after user authentication.

#### Code:
```python
class Oauth2CallbackView(View):
    def get(self, request, *args, **kwargs):
        if not xsrfutil.validate_token(
                settings.SECRET_KEY, request.GET.get('state').encode(),
                request.user):
            return HttpResponseBadRequest()
        global flow
        credentials = flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(
            GoogleAPIOauthInfo, 'id', request.user.id, 'credentials')
        storage.put(credentials)
        return redirect('/upload/')
```

---

### 3. **Index View**
The index page displays a welcome message and login options.

#### Code:
```python
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'index.html')
```

---

## Dependencies
- **Django**: Backend framework
- **Google API Client**: For interacting with the YouTube Data API
- **OAuth2Client**: For handling Google OAuth2 authentication
- **Python**: Programming language

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---