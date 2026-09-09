# Plant Disease Detection

A Streamlit application that classifies plant leaf images and stores user accounts and detection history in MySQL.

## Features

- User signup, login, and password reset
- Plant leaf image upload
- Disease prediction using a trained TensorFlow model
- Prediction confidence display
- MySQL-backed detection history
- Admin view for users and previous detections

## Project Structure

```text
app/                 Streamlit pages and application entry point
backend/             MySQL connection and authentication logic
ml_model/            Prediction code and trained model location
dataset_small/       Local training data, ignored by Git
```

## Requirements

- Python 3.10 or newer
- MySQL Server running on `127.0.0.1:3306`
- A copy of the trained model at `ml_model/model.h5`

## Installation

Open PowerShell in the project directory and create a virtual environment:

```powershell
python -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
```

Install the Python dependencies:

```powershell
python -m pip install streamlit tensorflow numpy pillow pandas mysql-connector-python bcrypt
```

## Database Setup

Create the database and tables in MySQL:

```sql
CREATE DATABASE plantdisease;

USE plantdisease;

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(100) NOT NULL UNIQUE,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL
);

CREATE TABLE detections (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(100) NOT NULL,
	image_path VARCHAR(500),
	disease_name VARCHAR(255),
	confidence FLOAT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The application connects as the MySQL `root` user on port `3306`. Store the database password in an environment variable instead of putting it in source code:

```powershell
$env:MYSQL_PASSWORD = "your-mysql-password"
```

Do not commit the password or a `.env` file. `.env` is already excluded by `.gitignore`.

## Run the Application

From the project root, with the virtual environment activated:

```powershell
python -m streamlit run app/streamlit_app.py
```

Open the URL shown by Streamlit, usually `http://localhost:8501`.

## Notes

- `ml_model/model.h5` is ignored by Git because trained models can be large. Place a local copy in `ml_model/` before using image prediction.
- `dataset_small/` is ignored by Git and is only needed for model training.
- Uploaded images are stored locally in an ignored `uploads/` directory.
- To train a model using the local dataset, run `ml_model/classifier.py` from the project root.

## Security

Never commit database passwords, API keys, `.env` files, model training data containing private information, or uploaded images. If a credential is accidentally pushed, revoke or change it and remove it from the repository history.
