import requests
import urllib


def checkCards(cardsURL, length, against, ending_message="!"):
    cardsObj = requests.get(cardsURL).json()
    
    cards = cardsObj["data"]
    for card in cards[:min(len(cards), length)]:
        if card["name"] in against:
            print("nuh uh! card " + card['name'] + " not legal" + ending_message)

    if length > len(cards) and cardsObj["has_more"] is True:
        checkCards(cardsObj["next_page"], length - len(cards), against)

    return


def get_deck(name):
    names = []
    with open(name) as file:
        ln = file.readline()
        while not ln.startswith("SB"):
            if ln is None:
                raise Exception()
            names.append(ln[ln.find("] ") + 2:].strip())
            ln = file.readline()
        mander = ln[ln.find("] ") + 2:]
    return names, mander


banned_searches = [
    ("f:edh id=w", 60),
    ("f:edh id=u", 60),
    ("f:edh id=b", 60),
    ("f:edh id=r", 60),
    ("f:edh id=g", 60),
    ("f:edh -t:land -otag:mana-rock id=c", 120),
    ("f:edh -t:land -otag:mana-rock id=wu", 12),
    ("f:edh -t:land -otag:mana-rock id=wb", 12),
    ("f:edh -t:land -otag:mana-rock id=wr", 12),
    ("f:edh -t:land -otag:mana-rock id=wg", 12),
    ("f:edh -t:land -otag:mana-rock id=ub", 12),
    ("f:edh -t:land -otag:mana-rock id=ur", 12),
    ("f:edh -t:land -otag:mana-rock id=ug", 12),
    ("f:edh -t:land -otag:mana-rock id=br", 12),
    ("f:edh -t:land -otag:mana-rock id=bg", 12),
    ("f:edh -t:land -otag:mana-rock id=rg", 12),
    ("f:edh t:land id=c", 60)
]

banned_searches_mander = [
    ("f:edh is:commander id=3", 60),
    ("f:edh is:commander id=4", 999),
    ("f:edh is:commander id=5", 30)
]

static_banlist = ["Sol Ring",
                  "Mana Vault"
                  ]

static_mander_banlist = ["Go-Shintai of Life's Origin",
                         "Avacyn, Angel of Hope",
                         "Baral, Chief of Compliance",
                         "Voja, Jaws of the Conclave",
                         "Kenrith, the Returned King"
                         ]


deck_cards, deck_mander = get_deck(input("file name??") + ".dck")

for searchstring, length in banned_searches:
    fullUrl = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode({'q': searchstring, 'order': 'edhrec'})

    checkCards(fullUrl, length, deck_cards)

for searchstring, length in banned_searches_mander:
    fullUrl = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode({'q': searchstring, 'order': 'edhrec'})

    checkCards(fullUrl, length, [deck_mander], " as your commander!")

checkCards("https://api.scryfall.com/cards/search?" + urllib.parse.urlencode({'q': "otag:face-commander"}), length, [deck_mander], " as your commander!")

for card in static_banlist:
    if card in deck_cards:
        print("nuh uh! card " + card['name'] + " not legal in this format! Blame Logan!!!")

for card in static_mander_banlist:
    if card == deck_mander:
        print("nuh uh! card " + card['name'] + " not legal in this format as your commander! Blame Logan!!!")


input("Press enter to exit...")  # ironic, isn't it
