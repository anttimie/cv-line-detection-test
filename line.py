import media

def main():
    filename = 'driving.mp4'
    player = media.Player(filename)
    player.play()

if __name__ == "__main__":
    main()