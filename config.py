"""
Configuration for LOL ELO System
"""

# Google Sheets
SHEET_ID = "1nRTW0IemmuWZ0LClblXwGbnbCKHQsdJU48z7PoPvrHM"
MATCHES_SHEET = "Matches"

# ELO Settings
K_FACTOR = 16  # Oder 16 für Simplicity
INITIAL_ELO = 1500
TRAIN_TEST_SPLIT = 0.7

# Scale Factors (optional)
USE_SCALE_FACTORS = False
SCALE_FACTORS = {
    '1-0': 1.00,
    '2-0': 1.00,
    '2-1': 0.50,
    '3-0': 1.00,
    '3-1': 0.90,
    '3-2': 0.80,
}

# Validation
TRAIN_TEST_SPLIT = 0.7  # 70% train, 30% test
RANDOM_SEED = 42