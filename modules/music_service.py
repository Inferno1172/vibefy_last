import streamlit as st

def get_mood_keywords(mood):
    """
    Maps moods to YouTube search keywords
    """
    mood_keywords = {
        "joy": ["upbeat happy music", "positive vibes", "dance party", "celebration songs"],
        "sadness": ["sad songs", "emotional music", "healing music", "comfort songs"],
        "anger": ["intense rock music", "powerful anthems", "release anger music", "heavy metal"],
        "disgust": ["cleansing music", "fresh start songs", "renewal music", "calming instrumental"],
        "fear": ["calming music", "peaceful instrumental", "anxiety relief music", "soothing sounds"],
        "surprise": ["epic orchestral", "wonderful discovery music", "magical soundtrack", "uplifting orchestral"],
        "neutral": ["chill music", "relaxing background", "study music", "lo-fi beats"]
    }
    return mood_keywords.get(mood, ["chill music"])

def search_songs(mood, user_input="", num_results=5):
    """
    Returns emotion-specific music recommendations
    """
    print(f"🎵 Searching for {mood} music...")
    
    # Emotion-specific song libraries
    emotion_songs = {
        "joy": [
            {
                "video_id": "ZbZSe6N_BXs",  # Pharrell Williams - Happy
                "title": "Happy - Pharrell Williams",
                "thumbnail": "https://img.youtube.com/vi/ZbZSe6N_BXs/hqdefault.jpg",
                "description": "The ultimate happy anthem!"
            },
            {
                "video_id": "ru0K8uYEZWw",  # Katrina & The Waves - Walking On Sunshine
                "title": "Walking On Sunshine - Katrina & The Waves", 
                "thumbnail": "https://img.youtube.com/vi/ru0K8uYEZWw/hqdefault.jpg",
                "description": "Pure sunshine energy!"
            },
            {
                "video_id": "fWNaR-rxAic",  # Bobby McFerrin - Don't Worry Be Happy
                "title": "Don't Worry Be Happy - Bobby McFerrin",
                "thumbnail": "https://img.youtube.com/vi/fWNaR-rxAic/hqdefault.jpg",
                "description": "The classic feel-good song"
            },
            {
                "video_id": "C-u5WLJ9Yk4",  # ABBA - Dancing Queen
                "title": "Dancing Queen - ABBA",
                "thumbnail": "https://img.youtube.com/vi/C-u5WLJ9Yk4/hqdefault.jpg",
                "description": "Feel like dancing!"
            },
            {
                "video_id": "JGhoLcsr8GA",  # Taylor Swift - Shake It Off
                "title": "Shake It Off - Taylor Swift",
                "thumbnail": "https://img.youtube.com/vi/JGhoLcsr8GA/hqdefault.jpg",
                "description": "Shake off the negativity!"
            }
        ],
        
        "sadness": [
            {
                "video_id": "hLQl3WQQoQ0",  # Adele - Someone Like You
                "title": "Someone Like You - Adele",
                "thumbnail": "https://img.youtube.com/vi/hLQl3WQQoQ0/hqdefault.jpg",
                "description": "Heartfelt ballad for emotional moments"
            },
            {
                "video_id": "nSDgHBxUbVQ",  # Billie Eilish - when the party's over
                "title": "when the party's over - Billie Eilish",
                "thumbnail": "https://img.youtube.com/vi/nSDgHBxUbVQ/hqdefault.jpg",
                "description": "Gentle and melancholic"
            },
            {
                "video_id": "rYEDA3JcQqw",  # Radiohead - Creep
                "title": "Creep - Radiohead",
                "thumbnail": "https://img.youtube.com/vi/rYEDA3JcQqw/hqdefault.jpg",
                "description": "Raw emotional expression"
            },
            {
                "video_id": "WIF4_Sm-rgQ",  # Sam Smith - Stay With Me
                "title": "Stay With Me - Sam Smith",
                "thumbnail": "https://img.youtube.com/vi/WIF4_Sm-rgQ/hqdefault.jpg",
                "description": "Soulful and vulnerable"
            },
            {
                "video_id": "J_8xCOSg-1U",  # Lewis Capaldi - Someone You Loved
                "title": "Someone You Loved - Lewis Capaldi",
                "thumbnail": "https://img.youtube.com/vi/J_8xCOSg-1U/hqdefault.jpg",
                "description": "Powerful emotional release"
            }
        ],
        
        "anger": [
            {
                "video_id": "fJ9rUzIMcZQ",  # Queen - Bohemian Rhapsody
                "title": "Bohemian Rhapsody - Queen",
                "thumbnail": "https://img.youtube.com/vi/fJ9rUzIMcZQ/hqdefault.jpg",
                "description": "Epic emotional journey"
            },
            {
                "video_id": "hTWKbfoikeg",  # Nirvana - Smells Like Teen Spirit
                "title": "Smells Like Teen Spirit - Nirvana",
                "thumbnail": "https://img.youtube.com/vi/hTWKbfoikeg/hqdefault.jpg",
                "description": "Raw grunge energy"
            },
            {
                "video_id": "llyiQ4Xo8aE",  # Linkin Park - In The End
                "title": "In The End - Linkin Park",
                "thumbnail": "https://img.youtube.com/vi/llyiQ4Xo8aE/hqdefault.jpg",
                "description": "Channel your frustration"
            },
            {
                "video_id": "5abamRO41fE",  # Rage Against The Machine - Killing In The Name
                "title": "Killing In The Name - Rage Against The Machine",
                "thumbnail": "https://img.youtube.com/vi/5abamRO41fE/hqdefault.jpg",
                "description": "Powerful protest anthem"
            },
            {
                "video_id": "v2AC41dglnM",  # AC/DC - Thunderstruck
                "title": "Thunderstruck - AC/DC",
                "thumbnail": "https://img.youtube.com/vi/v2AC41dglnM/hqdefault.jpg",
                "description": "High-energy rock release"
            }
        ],
        
        "disgust": [
            {
                "video_id": "GxBSyx85Kp8",  # Clean Bandit - Symphony
                "title": "Symphony - Clean Bandit ft. Zara Larsson",
                "thumbnail": "https://img.youtube.com/vi/GxBSyx85Kp8/hqdefault.jpg",
                "description": "Cleansing and beautiful"
            },
            {
                "video_id": "QcIy9NiNbmo",  # Katy Perry - Firework
                "title": "Firework - Katy Perry",
                "thumbnail": "https://img.youtube.com/vi/QcIy9NiNbmo/hqdefault.jpg",
                "description": "Rise above negativity"
            },
            {
                "video_id": "X46t8ZFqUB4",  # Sia - The Greatest
                "title": "The Greatest - Sia",
                "thumbnail": "https://img.youtube.com/vi/X46t8ZFqUB4/hqdefault.jpg",
                "description": "Find your inner strength"
            },
            {
                "video_id": "09R8_2nJtjg",  # Maroon 5 - Sugar
                "title": "Sugar - Maroon 5",
                "thumbnail": "https://img.youtube.com/vi/09R8_2nJtjg/hqdefault.jpg",
                "description": "Sweet escape from negativity"
            },
            {
                "video_id": "LjhCEhWiKXk",  # Coldplay - Paradise
                "title": "Paradise - Coldplay",
                "thumbnail": "https://img.youtube.com/vi/LjhCEhWiKXk/hqdefault.jpg",
                "description": "Escape to better places"
            }
        ],
        
        "fear": [
            {
                "video_id": "WIm1GgfRz6M",  # John Legend - All of Me
                "title": "All of Me - John Legend",
                "thumbnail": "https://img.youtube.com/vi/WIm1GgfRz6M/hqdefault.jpg",
                "description": "Soothing and reassuring"
            },
            {
                "video_id": "k4V3Mo61fJM",  # Ed Sheeran - Perfect
                "title": "Perfect - Ed Sheeran",
                "thumbnail": "https://img.youtube.com/vi/k4V3Mo61fJM/hqdefault.jpg",
                "description": "Calming romantic ballad"
            },
            {
                "video_id": "Ra-Om7UMSJc",  # Norah Jones - Don't Know Why
                "title": "Don't Know Why - Norah Jones",
                "thumbnail": "https://img.youtube.com/vi/Ra-Om7UMSJc/hqdefault.jpg",
                "description": "Gentle jazz comfort"
            },
            {
                "video_id": "tArt_7GYnqE",  # Enya - Only Time
                "title": "Only Time - Enya",
                "thumbnail": "https://img.youtube.com/vi/tArt_7GYnqE/hqdefault.jpg",
                "description": "Peaceful and ethereal"
            },
            {
                "video_id": "1mB0tG1-mkk",  # Israel Kamakawiwo'ole - Somewhere Over The Rainbow
                "title": "Somewhere Over The Rainbow - Israel Kamakawiwo'ole",
                "thumbnail": "https://img.youtube.com/vi/1mB0tG1-mkk/hqdefault.jpg",
                "description": "Hopeful and calming"
            }
        ],
        
        "surprise": [
            {
                "video_id": "dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
                "title": "Never Gonna Give You Up - Rick Astley",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
                "description": "The ultimate surprise song!"
            },
            {
                "video_id": "9bZkp7q19f0",  # PSY - Gangnam Style
                "title": "Gangnam Style - PSY",
                "thumbnail": "https://img.youtube.com/vi/9bZkp7q19f0/hqdefault.jpg",
                "description": "Unexpected global phenomenon"
            },
            {
                "video_id": "kJQP7kiw5Fk",  # Luis Fonsi - Despacito
                "title": "Despacito - Luis Fonsi",
                "thumbnail": "https://img.youtube.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
                "description": "Surprise viral hit"
            },
            {
                "video_id": "L_jWHffIx5E",  # Smash Mouth - All Star
                "title": "All Star - Smash Mouth",
                "thumbnail": "https://img.youtube.com/vi/L_jWHffIx5E/hqdefault.jpg",
                "description": "Meme-worthy surprise"
            },
            {
                "video_id": "d-diB65scQU",  # Lady Gaga - Bad Romance
                "title": "Bad Romance - Lady Gaga",
                "thumbnail": "https://img.youtube.com/vi/d-diB65scQU/hqdefault.jpg",
                "description": "Unexpected pop masterpiece"
            }
        ],
        
        "neutral": [
            {
                "video_id": "5qap5aO4i9A",  # Lofi Hip Hop Radio
                "title": "Lofi Hip Hop Radio - beats to relax/study to",
                "thumbnail": "https://img.youtube.com/vi/5qap5aO4i9A/hqdefault.jpg",
                "description": "Perfect chill background music"
            },
            {
                "video_id": "DWcJFNfaw9c",  # Coffee Shop Radio
                "title": "Coffee Shop Radio - 24/7 chill vibes",
                "thumbnail": "https://img.youtube.com/vi/DWcJFNfaw9c/hqdefault.jpg",
                "description": "Relaxing cafe atmosphere"
            },
            {
                "video_id": "mLPTX3lqV5Q",  # Jazz & Bossa Nova Music
                "title": "Jazz & Bossa Nova Radio",
                "thumbnail": "https://img.youtube.com/vi/mLPTX3lqV5Q/hqdefault.jpg",
                "description": "Smooth background jazz"
            },
            {
                "video_id": "bP9g4TzkOzQ",  # Chillhop Music
                "title": "Chillhop Essentials - Summer 2023",
                "thumbnail": "https://img.youtube.com/vi/bP9g4TzkOzQ/hqdefault.jpg",
                "description": "Relaxing electronic beats"
            },
            {
                "video_id": "7NOSDKb0HlU",  # Classical Music for Studying
                "title": "Classical Music for Studying",
                "thumbnail": "https://img.youtube.com/vi/7NOSDKb0HlU/hqdefault.jpg",
                "description": "Peaceful classical selection"
            }
        ]
    }
    
    # Return songs for the detected mood, or neutral as fallback
    songs = emotion_songs.get(mood, emotion_songs["neutral"])
    return songs[:num_results]

# Test function
if __name__ == "__main__":
    # Test all emotions
    emotions = ["joy", "sadness", "anger", "disgust", "fear", "surprise", "neutral"]
    for emotion in emotions:
        print(f"\n🎵 {emotion.upper()} songs:")
        songs = search_songs(emotion, num_results=2)
        for song in songs:
            print(f"  - {song['title']}")