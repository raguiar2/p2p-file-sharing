import asyncio
import websockets
import multiprocessing
import requests
import functools
import json

MAIN_SERVER_URL = 'http://localhost:5000'
P2P_PORT_NO = 8765
CENTRAL_PORT_NO = 8000

async def download_song_from_host(websocket, path, song='', stop=None, address=''):
    file_bytes = await websocket.recv()
    print("< {}".format(file_bytes))
    f = open('./songs/{}-cloned'.format(song), 'w')
    f.write(file_bytes)
    f.close()
    await websocket.send("closed")
    stop.set_result(None)

async def download_server(stop, song, address):
    print("downloading song {} from address {}".format(song, address))
    async with websockets.serve(functools.partial(download_song_from_host, song=song, stop=stop, address=address), "localhost", P2P_PORT_NO):
        requests.post(MAIN_SERVER_URL + '/send_song', data={'song':song, 'address':address})
        await stop

# launch process in fg to listen to client for typing
# (P1)
# when client types in, send req to server for song
# wait for response, if 200, connect to other ip as server
# download byte-stream from them.
# save as mp3 in songs directory
def client_interface():
    while True:
        song = input("What song should I search for? ")
        print("Searching for song...")
        r = requests.get(MAIN_SERVER_URL + '?song={}'.format(song))
        if r.status_code != 200:
            print("Sorry! Something went wrong. Please try again")
            continue
        address = json.loads(r.content)['address']
        loop = asyncio.get_event_loop()
        stop = loop.create_future()
        print("address is", address)
        loop.run_until_complete(download_server(stop, song, address))

async def open_connection_to_host(address):
    import time
    time.sleep(3)
    uri = "ws://{}:{}".format(address, P2P_PORT_NO)
    async with websockets.connect(uri) as websocket:
        await websocket.send('Rui Aguiar')
        print("> {}".format('Rui Aguiar'))
        sent = await websocket.recv()
        print("< {}".format(sent))

# launch process in bg to listen to server
# (P2)
# wait for requests from central server (as a server, probably/websockets)
# on recieving one, connect as client to recieved ip address with socket
# pipe song through then close connection
# continue to wait for server
def connection_interface():
    # asyncio.get_event_loop().run_until_complete(open_connection_to_host('localhost'))
    pass

def main():
    p = multiprocessing.Process(target=connection_interface)
    p.start()
    client_interface()

if __name__ == '__main__':
    main()
