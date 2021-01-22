import media
import visual
import frame

def main():
    filename = 'video.mp4'
    player = media.Player(filename)
    player.play()

if __name__ == "__main__":
    main()