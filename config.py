"""
Configuration for LOL ELO System
"""

# Google Sheets
SHEET_ID = "1nRTW0IemmuWZ0LClblXwGbnbCKHQsdJU48z7PoPvrHM"
MATCHES_SHEET = "Matches"

# ELO Settings
INITIAL_ELO = 1500
K_FACTOR = 20

# Validation
TRAIN_TEST_SPLIT = 0.7  # 70% train, 30% test
RANDOM_SEED = 42