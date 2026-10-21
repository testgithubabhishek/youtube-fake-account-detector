
import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# YouTube API setup
API_KEY = st.secrets["YOUTUBE_API_KEY"]

# Function to fetch comments
def fetch_comments(video_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        ).execute()

        while response:
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": comment["authorDisplayName"],
                    "comment": comment["textOriginal"]
                })

            if "nextPageToken" in response:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=response["nextPageToken"],
                    maxResults=100
                ).execute()
            else:
                break
    except Exception as e:
        st.error(f"Error fetching comments for {video_id}: {e}")
    return pd.DataFrame(comments)

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to find similar comments
def find_similar_comments(comments, threshold=0.8):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(comments)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    similar_pairs = []
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            if similarity_matrix[i, j] > threshold:
                similar_pairs.append((i, j))
    return similar_pairs

# Streamlit UI
st.set_page_config(
    page_title="YouTube Fake Account Detector",
    layout="centered"
)

# Welcome section
st.title("🎭 YouTube Fake Account Detector")
st.write(
    "🚀 Detect bot-generated comments and fake accounts "
    "based on repetitive comment patterns."
)

# Button to open YouTube
st.markdown("### 🔗 Get YouTube Video IDs")
st.write(
    "To analyze comments, you need YouTube video IDs. "
    "Click the button below to open YouTube and copy the ID "
    "from the video URL."
)
st.markdown(
    "[![Open YouTube](https://img.shields.io/badge/"
    "Open%20YouTube-red?logo=youtube)](https://www.youtube.com/)"
)

# Example instructions
st.info(
    "**How to Get Video ID?**\n\n"
    "- Open a YouTube video.\n"
    "- Look at the URL "
    "(e.g., `https://www.youtube.com/watch?v=**abcd1234xyz**`).\n"
    "- Copy the part after `v=` (e.g., `abcd1234xyz`)."
)

# Select number of video IDs
st.subheader("🔢 Select Number of YouTube Videos to Analyze")
num_videos = st.selectbox(
    "How many video IDs do you want to enter?",
    [1, 2, 3, 4, 5]
)

# Collect video IDs
video_ids = []
for i in range(num_videos):
    video_id = st.text_input(f"Enter Video ID {i+1}:", "")
    if video_id:
        video_ids.append(video_id)

# Show clickable links for entered video IDs
if video_ids:
    st.subheader("🔗 Your YouTube Video Links")
    for vid in video_ids:
        st.markdown(
            f"[Watch Video](https://www.youtube.com/watch?v={vid}) 🎬"
        )

# Analyze button
if st.button("🔍 Analyze"):
    if not video_ids:
        st.error("⚠️ Please enter at least one video ID.")
    else:
        st.info("⏳ Fetching comments... This may take a few seconds.")

        # Fetch comments for all videos
        all_comments = pd.concat(
            [fetch_comments(vid) for vid in video_ids],
            ignore_index=True
        )

        if all_comments.empty:
            st.error(
                "❌ No comments found. Please check your video IDs "
                "and try again."
            )
        else:
            # Preprocess comments
            all_comments["cleaned_comment"] = (
                all_comments["comment"].apply(preprocess_text)
            )

            # Find similar comments
            similar_pairs = find_similar_comments(
                all_comments["cleaned_comment"]
            )

            # Identify fake accounts
            fake_accounts = set()
            for i, j in similar_pairs:
                if (
                    all_comments.iloc[i]["author"]
                    != all_comments.iloc[j]["author"]
                ):
                    fake_accounts.add(all_comments.iloc[i]["author"])
                    fake_accounts.add(all_comments.iloc[j]["author"])

            # Display results
            st.subheader("📊 Results")
            st.write(
                f"**🕵️‍♂️ Fake Accounts Detected: "
                f"{len(fake_accounts)}**"
            )

            if fake_accounts:
                st.table(
                    pd.DataFrame({
                        "Fake Accounts": list(fake_accounts)
                    })
                )
            else:
                st.success("✅ No fake accounts detected!")

# Footer
st.markdown("---")
st.write("Developed with by [Abhishek]")
