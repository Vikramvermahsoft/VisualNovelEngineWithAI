import pyglet
import json

class Reader():
    def __init__(self):
        self.name = 'Reader'
        self.current_page = 0
        self.timeline_content = ""
        print('Reader created')
    def timeline_read(self,timeline_id):
        self.current_page = timeline_id

        f = open('timeline.json')
        data = json.load(f)
        print(timeline_id)
        print(data['content'][self.current_page])
        #for i in data['content']:
        #    print(timeline_id)
        #    print(i) 
        self.timeline_content = data['content'][self.current_page] 
        f.close()
    def label_draw(self):
        label = pyglet.text.Label(self.timeline_content,
                font_name='Times New Roman',
                anchor_x = 'center', anchor_y='center')
        label.draw()
        #print('label drew')
        #print('timeline_id')
    def textbox(self, timeline_id):
        print(timeline_id)

