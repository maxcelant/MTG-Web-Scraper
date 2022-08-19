from bs4 import BeautifulSoup
import requests

# CARDKINGDOM_URL = f'https://www.cardkingdom.com/catalog/search?search=header&filter%5Bname%5D={card_name}'


def getCardName():
    cardName = input('Enter Card Name: ')
    limit = input('Top X Cards?: ')
    return cardName.lower(), limit


def fetchEbayData(cardName):
    URL = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2499334.m570.l1313&_nkw=mtg+{cardName}&_sacat=183454'
    response = requests.get(URL).text
    doc = BeautifulSoup(response, 'html.parser')
    names = doc.find_all("h3", {"class": "s-item__title"})
    prices = doc.find_all("span", {"class": "s-item__price"})
    page_links = doc.find_all("a", {"class": "s-item__link"})
    return names, prices, page_links


def filterEbayData(cardName, names, prices, page_links):
    priceToPage = {}
    # perform item limit on each var
    names = names[:30]
    prices = prices[:30]
    page_links = page_links[:30]

    for index, link in enumerate(page_links):
        name = str(names[index].string)
        if cardName not in name.lower():
            continue
        priceToPage[link['href']] = float(
            prices[index].string[1:]) if prices[index].string else 'No Price Given'

    return priceToPage


def sortPriceEbay(priceToPage):

    cards = []

    for link in priceToPage:
        if(priceToPage[link] == "No Price Given"):
            continue
        cards.append([priceToPage[link], link])  # (price, link)

    for i in range(len(cards)):
        for j in range(len(cards)):
            if float(cards[i][0]) < float(cards[j][0]):
                cards[i][0], cards[j][0] = cards[j][0], cards[i][0]

    return cards


def showTopPicks(cards, limit):
    for index, card in enumerate(cards):
        if index > limit:
            break
        print(f'Cost: ${card[0]}')
        print(f'Link: {card[1]}', end='\n\n')


if __name__ == '__main__':
    cardName, limit = getCardName()
    names, prices, page_links = fetchEbayData(cardName)
    priceToPage = filterEbayData(cardName, names, prices, page_links)
    sortedCards = sortPriceEbay(priceToPage)
    showTopPicks(sortedCards, int(limit))
