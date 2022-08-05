from random import randint

import disnake

activities = [
    disnake.CustomActivity(
        name="Watching a movie",
        emoji="🎥",
        type=disnake.ActivityType.custom,
    ),
    disnake.CustomActivity(
        name="Listening to music",
        emoji="🎵",
        type=disnake.ActivityType.custom,
    ),
    disnake.CustomActivity(
        name="Playing games",
        emoji="🎮",
        type=disnake.ActivityType.custom,
    ),
    disnake.CustomActivity(
        name="Watching a stream",
        emoji="📺",
        type=disnake.ActivityType.custom,
    ),
]

activity = activities[randint(0, len(activities) - 1)]
