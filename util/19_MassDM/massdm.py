import requests
import threading
from colorama import Fore
from util.plugins.commun import setTitle, proxy, getheaders

def MassDM(token, channels, Message):
    for channel in channels:
        for user in [x["username"] + "#" + x["discriminator"] for x in channel["recipients"]]:
            try:
                setTitle(f"Messaging " + user)
                response = requests.post(f'https://discord.com/api/v9/channels/' + channel['id'] + '/messages',
                                         proxies=proxy(),
                                         headers={'Authorization': token},
                                         data={"content": f"{Message}"})
                if response.status_code == 204 or response.status_code == 200:
                    print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Messaged: " + user + Fore.RESET)
                elif response.status_code == 429:
                    print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Rate limited ({response.json().get('retry_after')}ms)")
                else:
                    print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Error: {response.status_code}")
            except Exception as e:
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} The following error has been encountered and is being ignored: {e}")

def main():
    setTitle("Mass DM")
    clear()
    massdmtitle()

    print(f"{y}[{w}+{y}]{w} Enter the token of the account you want to Spam")
    token = input(f"""{y}[{b}#{y}]{w} Token: """)
    print(f"\n{y}[{w}+{y}]{w} Message that will be sent to every friend")
    message = str(input(f"{y}[{b}#{y}]{w} Message: "))
    clear()
    processes = []
    global channelIds
    channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token))
    if not channelIds:
        print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} This guy is lonely, he ain't got no DM's...")
        input(f"\n{y}[{b}#{y}]{w} Press enter to continue")
        main()
    channelIds = channelIds.json()
    for channel in [channelIds[i:i + 3] for i in range(0, len(channelIds), 3)]:
        t = threading.Thread(target=MassDM, args=(token, channel, message))
        t.start()
        processes.append(t)
    for process in processes:
        process.join()
    input(f"\n{y}[{b}#{y}]{w} Press enter to continue")
    main()

if __name__ == "__main__":
    main()
