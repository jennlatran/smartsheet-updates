# Smartsheet Design Project Updater

A lightweight browser tool for reading and updating a Smartsheet design project plan. Claude acts as a secure proxy for Smartsheet API calls, eliminating CORS issues without a backend.

## Features

- Connect to Smartsheet using a personal API token
- Browse and select any sheet from your account
- View all rows and columns in a clean table
- Add new project rows directly from the UI
- Refresh sheet data on demand

## Usage

> **Important:** Open the file via a local HTTP server — browsers block API calls from `file://` pages.

1. Start a local server in this directory:
   ```
   python3 -m http.server 8080
   ```
2. Open [http://localhost:8080](http://localhost:8080) in your browser
3. Paste your Smartsheet API token (Account → Personal Settings → API Access) and click **Connect**
4. Select **Design Project Plan** (or any sheet) from the dropdown and click **Load**
5. View projects, add new rows, or click **Ask Claude for weekly review** for a status summary

## Notes

- The API token is used only within your session and is never stored or sent anywhere except Smartsheet's API
- Smartsheet API calls are made directly from the browser using your Bearer token
