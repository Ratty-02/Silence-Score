# Silence-Score

Behavioral Productivity Detection System
Silence Score is a behavioral productivity analysis system that detects fake productivity by analyzing real interaction patterns instead of relying only on time tracking.
Traditional productivity tools measure how long a system is active. Silence Score focuses on how consistently and meaningfully a user interacts with their system.

-->Problem Statement:
Time-based productivity metrics fail to capture cognitive effort.
Users may appear busy (apps open, tabs active) while being mentally idle.
Silence Score answers one question:
Was the user actually working, or just appearing productive?

-->Solution Overview
The system logs real user activity and derives behavioral features to compute a Silence Score (0–100), classifying work into:
Deep Work
Shallow Work
Fake Productivity
The approach is explainable, lightweight, and privacy-aware.

--> How It Works
Activity Logging
Keyboard key presses
Mouse movement distance
Active application
Fixed time windows
Feature Engineering
Interaction density
App switching frequency
Input consistency
Idle patterns
Scoring Engine
Rule-based weighted scoring
Focuses on consistency over duration
Behavior Classification
Deep Work
Shallow Work
Fake Productivity
Visualization
Silence Score timeline
Behavioral insights

--> Tech Stack
Python
Pandas, NumPy
Matplotlib
pynput (keyboard & mouse logging)
psutil (process monitoring)

-->Privacy & Ethics
No personal content is recorded
Only interaction counts and application names are logged
No data is uploaded or shared
Activity logs are excluded from version control using .gitignore
This project is intended only for educational and self-analysis purposes.

--> Why This Project Matters
Uses self-generated real-world data
Avoids black-box machine learning
Focuses on explainability
Solves a relatable, real productivity problem
Demonstrates end-to-end system design

--> Future Enhancements
Unsupervised clustering (K-Means)
Burnout detection patterns
Streamlit dashboard
Cross-platform activity abstraction

-->How to Run
1. Install dependencies
pip install -r requirements.txt
2. Run activity logger
python src/logger.py
Let it run while you work for 20–60 minutes, then stop it.
3. Analyze & visualize
python src/visualize.py

👤 Author
Rehan Azad
Computer Science Student
Interested in data analysis, machine learning fundamentals, and problem-solving



