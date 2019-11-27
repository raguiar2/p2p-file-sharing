import requests
import json

PORT_NO = 8000
CENTRAL_SERVER_ADDR = 'localhost:5000'

def get_song_from_address(address, song):
    print("Downloading song...")
    r = requests.get("http://{}:{}/request_song?song={}".format(address, PORT_NO, song))
    if r.status_code != 200:
        print("Sorry! Something went wrong getting the song. Please try again later")
        return
    open('./songs/{}-copy.mp3'.format(song), 'wb').write(r.content)
    print("Song downloaded! You can find it in the songs file")

def main():
    while True:
        song = input("Enter the name of a song you would like to download: ")
        r = requests.get("http://{}/lookup_song?song={}".format(CENTRAL_SERVER_ADDR, song))
        if r.status_code != 200:
            print("Sorry! We could not find that song. Try another")
            continue
        address = json.loads(r.content)['address']
        get_song_from_address(address, song)

if __name__ == '__main__':
    main()
