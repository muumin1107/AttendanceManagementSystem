from lib._notionapi import NotionAPI
from lib._cardreader import CardReader

notionapi  = NotionAPI()
cardreader = CardReader()

def main():
    print(cardreader.read_card())
    return

if __name__ == '__main__':
    main()