# StudyAI Prompt Generator

Android/Kivy app that accepts a photo or audio file and returns a ready-to-copy AI prompt.

## Project files
- `main.py`: Android app
- `buildozer.spec`: Buildozer Android configuration
- `.github/workflows/android.yml`: GitHub Actions APK build
- `backend/app.py`: Flask API that calls the OpenAI API
- `backend/render.yaml`: Render deployment blueprint

## Important: deploy the backend first
The Android app does not keep your OpenAI API key. The key must stay on the server.

1. Push this project to your GitHub repository.
2. Create an OpenAI API key in your API account. API usage may cost money and is separate from a ChatGPT subscription. Do not paste the key into `main.py`, GitHub commits, or chat messages.
3. Deploy the `backend` folder as a web service on a Python host such as Render. You can use `backend/render.yaml` as a guide.
4. In the backend service's environment settings, add `OPENAI_API_KEY` with your API key as its value.
5. After deployment, open the backend root URL; it should show `{"status":"StudyAI backend is running"}`.
6. Edit `main.py` and replace `https://YOUR-BACKEND-URL.onrender.com/generate` with your real backend URL plus `/generate`. Example shape: `https://your-service.onrender.com/generate`.
7. Commit the change to GitHub.

## Build the APK
1. Open the `Study-Ai` repository on GitHub.
2. Make sure `main.py`, `buildozer.spec`, and `.github/workflows/android.yml` are in the repository root / indicated path.
3. Open **Actions** and choose **Build StudyAI APK**.
4. Tap **Run workflow**, or push a commit to `main`.
5. When the workflow succeeds, open the run and download the `StudyAI-APK` artifact.

If the Docker build step says `Unknown command/target buildozer`, the workflow's `args` should be `android debug` (not `buildozer android debug`) because the container already runs Buildozer as its entrypoint.

## Supported file types
- Images: PNG, JPG, JPEG, WEBP
- Audio: MP3, M4A, WAV, OGG, WEBM, MP4, FLAC

## Notes
- Internet connection is required.
- Image/audio content is sent to your configured backend and then to the AI API to create the prompt.
- The backend limits uploads to 20 MB.
- Do not upload private or sensitive files.
