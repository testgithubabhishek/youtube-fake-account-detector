# YouTube Fake Account Detector

A Python web application that analyzes YouTube comments and flags potentially suspicious accounts based on similarities between comment text.

## Overview

The YouTube Fake Account Detector retrieves comments using the YouTube Data API v3 and analyzes their textual similarity. It helps identify patterns where different authors post highly similar comments, which may warrant further investigation.

**Important:** Similar comments do not prove that an account is fake. The application provides heuristic flags for further review, not definitive account verification.

## Features

- **YouTube input:** Accepts YouTube video URLs or video IDs.
- **Comment retrieval:** Fetches available comments using the YouTube Data API v3.
- **Text preprocessing:** Normalizes comment text by converting it to lowercase, removing punctuation, and normalizing whitespace.
- **Text similarity analysis:** Uses TF-IDF vectorization and cosine similarity to compare comments.
- **Suspicious-pattern identification:** Flags authors associated with highly similar comments posted under different author names, using a similarity threshold greater than 0.8.
- **Interactive web interface:** Provides a Streamlit interface for running the analysis.
- **Cloud deployment:** Runs locally and is deployed using Streamlit Community Cloud.

## Technology Stack

- Python
- Streamlit
- YouTube Data API v3
- Google API Python Client
- Pandas
- scikit-learn
- Git and GitHub

## How It Works

1. The user enters a YouTube video URL or video ID.
2. The application extracts the video ID, excluding URL parameters such as timestamps.
3. The application retrieves available comments through the YouTube Data API.
4. Comment text is normalized during preprocessing.
5. TF-IDF converts the text into numerical vectors.
6. Cosine similarity is used to compare comment vectors.
7. Authors associated with highly similar comments from different author names are flagged for further review.

The similarity threshold is a heuristic, not a validated measure of whether an account is fake.

## Getting Started

### Prerequisites

- Python installed on your computer
- A Google Cloud project with the YouTube Data API v3 enabled
- A valid YouTube Data API key

### 1. Clone the repository

```bash
git clone https://github.com/testgithubabhishek/youtube-fake-account-detector.git
cd youtube-fake-account-detector
```

### 2. Install dependencies

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

Create a `.streamlit` directory in the project root if it does not already exist. Inside it, create `secrets.toml`:

```toml
YOUTUBE_API_KEY = "YOUR_ACTUAL_API_KEY"
```

Replace the placeholder with your own API key.

**Security:** Never commit your real API key to GitHub. Ensure `.streamlit/secrets.toml` is listed in `.gitignore`.

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Deployment

The application is deployed through Streamlit Community Cloud using the GitHub repository.

For cloud deployment:

1. Connect the GitHub repository to Streamlit Community Cloud.
2. Set `app.py` as the main application file.
3. Add `YOUTUBE_API_KEY` to the app's Secrets settings.
4. Deploy the application.

Do not upload your local `secrets.toml` file.

## Limitations

- YouTube API quota limits may restrict the number of requests.
- Videos with disabled comments or restricted access may not provide comment data.
- Similar comments can occur naturally, including through repeated phrases or common expressions.
- The heuristic may produce false positives and false negatives.
- The application does not establish the actual identity, intent, or authenticity of an account.
- Detection results depend on the comments available to the application.

## Future Improvements

- Add automated unit and integration tests.
- Separate comment retrieval, preprocessing, and detection into reusable modules.
- Add configurable analysis parameters and clearer explanations for flagged results.
- Evaluate the heuristic against a labelled dataset before reporting detection metrics.
- Introduce a FastAPI backend with documented REST endpoints.

## Repository

GitHub: https://github.com/testgithubabhishek/youtube-fake-account-detector

