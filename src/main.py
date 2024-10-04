from lib._notionapi import NotionAPI

notionapi = NotionAPI()

if __name__ == '__main__':
    print(notionapi.add_db(name='島田拓斗', next_state='出勤'))
    # print(notionapi.add_id(id='test', name='test', attribute='ICカード', discription='test'))
    # print(notionapi.search_id(id_num='test'))
    # print(notionapi.remove_db(name='test'))
    # print(notionapi.remove_id(name='test'))