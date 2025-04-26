# VoyagerVerse Sharing Instructions

This document provides instructions for sharing your VoyagerVerse prototype with others.

## Option 1: Quick Sharing with Ngrok (Recommended)

I've created a simple deployment script that will automatically set up a public URL for your VoyagerVerse prototype using Ngrok. This is the easiest way to share your project.

```bash
# Install the required dependency
pip install pyngrok

# Run the deployment script
python deploy.py
```

The script will:
1. Start your FastAPI server locally
2. Create a secure public URL using Ngrok
3. Display the URL you can share with others
4. Optionally open the demo pages in your browser

Share the generated URL with others, and they'll be able to access your VoyagerVerse prototype without installing anything!

## Option 2: Docker Deployment

For a more permanent solution, you can use Docker:

```bash
# Build the Docker image
docker build -t voyagerverse .

# Run the Docker container
docker run -p 8000:8000 voyagerverse
```

You can then share the Docker image with others, or deploy it to a cloud platform that supports Docker containers.

## Option 3: GitHub Repository

Share your GitHub repository with others, and they can follow the installation instructions in the README.md file to set up the project locally.

```bash
# Push your changes to GitHub
git add .
git commit -m "Final hackathon version"
git push origin main
```

Share the repository URL: `https://github.com/Enigma3999/VoyagerVerse-Agentic-AI`

## Option 4: Cloud Deployment

For a more permanent solution, you can deploy to a cloud platform:

### Render.com (Free tier available)

1. Create an account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main_v2:app --host 0.0.0.0 --port 10000`

### Heroku

1. Create a `Procfile` with: `web: uvicorn main_v2:app --host=0.0.0.0 --port=${PORT:-8000}`
2. Deploy with Heroku CLI: `heroku create voyagerverse && git push heroku main`

## Important Notes

- If you're sharing with developers, remind them to add their own OpenAI API key to the `.env` file
- The demo works without an API key, but will use fallback responses instead of generating new content
- Make sure to point users to the correct demo URLs:
  - Simple Chat Demo: `/simple-chat`
  - Simple Agent UI: `/simple-agent`
  - Conversation Demo: `/conversation-demo`
  - Agent Calling Demo: `/agent-calling-demo`
