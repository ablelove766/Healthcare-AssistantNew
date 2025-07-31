# Microsoft Teams App Deployment

This directory contains the Microsoft Teams app manifest and related files for deploying the Healthcare Assistant as a Teams app.

## Files

- `manifest.json` - Teams app manifest file
- `icon-color.png` - Color icon (192x192px) - **REQUIRED**
- `icon-outline.png` - Outline icon (32x32px) - **REQUIRED**

## Deployment Steps

### 1. Create Icons

You need to create two icon files:

- **icon-color.png**: 192x192 pixels, color icon for the app
- **icon-outline.png**: 32x32 pixels, outline/monochrome icon

### 2. Create App Package

1. Place the icon files in this directory
2. Create a ZIP file containing:
   - manifest.json
   - icon-color.png
   - icon-outline.png

### 3. Upload to Teams

1. Open Microsoft Teams
2. Go to Apps → Manage your apps
3. Click "Upload an app" → "Upload a custom app"
4. Select your ZIP file
5. Follow the installation prompts

### 4. Configure App

The app will be available at:
- **Chat Tab**: https://healthcare-assistant-hla0.onrender.com/teams
- **Configuration**: https://healthcare-assistant-hla0.onrender.com/teams/config

## App Features

- Personal chat interface optimized for Teams
- Real-time healthcare assistance
- Patient information lookup
- Secure iframe embedding
- Teams SDK integration

## Security

The app is configured with appropriate security headers for Teams embedding:
- Frame ancestors allow Teams domains
- CSP policies for secure content loading
- CORS headers for cross-origin requests

## Support

For issues or questions, check the main application logs or contact the development team.
