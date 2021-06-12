import requests
from threading import Thread, activeCount

threadc = 5
groupids = open('groupids.txt','r').read().splitlines()

def scrape(gid):
    try:
        r = requests.get(f'https://groups.roblox.com/v1/groups/{gid}').json()
        fname = ''.join(x for x in r['name'] if x.lower() in 'abcdefghijklmnopqrstuvwxyz1234567890 ') + f' ({gid})'
        members = r['memberCount']
    except:
        fname = gid
        members = '?'
    print(f'Started scraping {fname} ({members} members) | {len(groupids)} groups remaining')
    fname = f'output/{fname}'
    cursor = ''
    while 1:
        try:
            r = requests.get(f'https://groups.roblox.com/v1/groups/{gid}/users?sortOrder=Asc&limit=100&cursor={cursor}')
            users = [f'{x["user"]["username"]}\n' for x in r.json()['data']]
            with open(f'{fname}.txt', 'a') as f:
                f.writelines(users)
            cursor = r.json()['nextPageCursor']
            if not cursor: break
        except Exception as e:
            print(e)

while 1:
    if groupids and (activeCount() < threadc+1):
        groupid = groupids.pop()
        Thread(target=scrape, args=(groupid,)).start()
    if activeCount() == 1: break

input('Finished!')
