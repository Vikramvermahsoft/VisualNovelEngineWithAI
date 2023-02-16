import pyglet
import json

class Reader():
    def __init__(self):
        self.name = 'Reader'
        self.current_page = 0
        self.current_chapter=1
        self.timeline_content = ""
        self.latest_page = 0
        self.total_pages = 2
        print('Reader created')
    def timeline_read(self,timeline_id):
        self.current_page = timeline_id
        chapter_num = 'chapter'+str(self.current_chapter)
        page_num = str(self.current_page)
        f = open('timeline.json')
        data = json.load(f)
        print(timeline_id)
        print(data[chapter_num]['page%s'%page_num])
        self.total_pages = len(data[chapter_num])-1
        #for i in data['content']:
        #    print(timeline_id)
        #    print(i) 
        self.timeline_content = data[chapter_num]['page%s'%page_num][0] 
        f.close()
    def label_draw(self):
        label = pyglet.text.Label(self.timeline_content,
                font_name='Times New Roman',
                anchor_x = 'center', anchor_y='center')
        label.draw()
        if self.current_page < self.latest_page:
            print('BACKLOG')
        if self.current_page == self.latest_page:
            print('LATEST')
        #print('label drew')
        #print('timeline_id')
    def textbox(self, timeline_id):
        print(timeline_id)
    def list_of_actions(timeline_id):
        print(timeline_id)

