from lib._notionapi import NotionAPI
from lib._card import CardReader

notionapi  = NotionAPI()
cardreader = CardReader()

def main():
    while True:
        #最初に表示
        print("Please Touch")
        #タッチ待ち
        cardreader.read()
        #リリース時の処理
        print("【 Released 】")

if __name__ == '__main__':
    main()
    # print(notionapi.add_db(name='島田拓斗', next_state='出勤'))
    # print(notionapi.add_id(id='test', name='test', attribute='ICカード', discription='test'))
    # print(notionapi.search_id(id_num='test'))
    # print(notionapi.remove_db(name='test'))
    # print(notionapi.remove_id(name='test'))