import os
from stuff.media import Player
from dotenv import load_dotenv

load_dotenv()

def main():
    filename = os.getenv("VIDEOPATH")
    player = Player(filename)
    player.play()

if __name__ == "__main__":
    main()