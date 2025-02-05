# Data Summary Viewer

## Overview
Data Summary Viewer is a web application that enables users to filter and view data from a MySQL database based on selected dates and usernames. The application is built with Svelte for the frontend and Flask for the backend.

## Project Structure
```
myproject/
├── .gitignore                 # Specifies files and directories to be ignored by Git
├── .vscode/
│   ├── settings.json          # VS Code settings (e.g., live server port)
├── backend_flask.py           # Flask backend that connects to MySQL and provides API endpoints
├── package.json               # Project metadata and dependencies
├── public/
│   ├── build/
│   │   ├── bundle.css         # Compiled CSS file
│   │   ├── bundle.js          # Compiled JavaScript file
│   ├── global.css             # Global styles for the application
│   ├── index.html             # Main HTML file containing the Svelte app
├── README.md                  # Project documentation (this file)
├── rollup.config.js           # Rollup module bundler configuration
├── scripts/
│   ├── setupTypeScript.js     # Script to enable TypeScript
├── src/
│   ├── App.svelte             # Main Svelte component
│   ├── main.js                # Entry point for the Svelte application
├── package-lock.json          # Dependency tree lock file
```

## Backend (Flask)
- Implemented in `backend_flask.py` using Flask.
- Connects to a MySQL database and provides two main API endpoints:
  - `/api/table_data`: Retrieves table data based on the provided start date, end date, and optional username.
  - `/api/usernames`: Fetches a list of unique usernames from the database.
- Uses `pymysql` for database interaction.
- Uses `flask_cors` to handle Cross-Origin Resource Sharing (CORS).

## Frontend (Svelte)
- Built using Svelte, a modern JavaScript framework.
- `App.svelte` is the main component that fetches and displays data.
- Users can filter data by selecting a username and date range using Flatpickr.
- Fetches data from the backend using the Fetch API and updates the table dynamically.

## Build and Configuration
- Uses Rollup as the module bundler, configured in `rollup.config.js`.
- Dependencies and scripts for building and running the app are listed in `package.json`.
- `setupTypeScript.js` can be used to configure TypeScript support.

## Styling
- Global styles are defined in `global.css`.
- Additional styles are included within Svelte components and `index.html`.

## Setup and Running the Application

### Prerequisites
- Node.js and npm installed
- Python and pip installed
- MySQL database set up

### Backend Setup
1. Install dependencies:
   ```sh
   pip install flask flask_cors pymysql
   ```
2. Start the Flask backend:
   ```sh
   python backend_flask.py
   ```

### Frontend Setup
1. Install dependencies:
   ```sh
   npm install
   ```
2. Build and run the frontend:
   ```sh
   npm run dev
   ```

### Running the Application
- The backend will be accessible at `http://127.0.0.1:5000/`.
- The frontend will be available at `http://localhost:5000/`.

## Future Enhancements
- Implement authentication for secure access.
- Improve UI/UX with better styling and interactions.
- Add pagination for large datasets.
- Extend API functionalities for more complex queries.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or contributions, feel free to reach out or submit a pull request.
