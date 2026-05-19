# Smartsheet Design Project Updater

A lightweight browser tool for reading and updating a Smartsheet design project plan. Claude acts as a secure proxy for Smartsheet API calls, eliminating CORS issues without a backend.

## Features

- Connect to Smartsheet using a personal API token
- Browse and select any sheet from your account
- View all rows and columns in a clean table
- Add new project rows directly from the UI
- Refresh sheet data on demand

## Usage

1. Open `index.html` in a Claude artifact or compatible environment
2. Paste your Smartsheet API token (Account → Personal Settings → API Access)
3. Select a sheet from the dropdown and click **Load**
4. View, add, or update rows as needed

## Notes

- The API token is used only within your session and is never stored
- Designed to run inside Claude Code as an embedded artifact
