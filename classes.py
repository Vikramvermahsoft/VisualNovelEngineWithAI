import pyglet
import json
from pyglet import image
import time

'''Classes file is temporary and classes will be merged to main.py unless i can find a way to access Window as a variable without instancing it here '''

window = pyglet.window.Window()
window.close()
class Reader():
    def __init__(self):
        self.name = 'Reader'
        self.current_page = 0
        self.current_chapter=0
        #current page and chapter code for save/load
        self.timeline_content = ""
        self.label_content = ""
        #timeline content uploaded from timeline.json, transfer to label content for display
        self.label_content_index = 0
        self.latest_page = 0
        #latest page set to 0 every chapter. part of save load data?
        self.total_pages = 0
        #comes from timeline.json, how many pages in a chapter
        self.audio_que = ""
        print('Reader created')
    def timeline_read(self,timeline_id):
        self.current_page = timeline_id
        #chapter_num = 'chapter'+str(self.current_chapter)
        chapter_num = self.current_chapter
        page_num = str(self.current_page)
        f = open('timeline.json')
        data = json.load(f)
        print(timeline_id)
        print(data)
        print(data[0])
        print(data[chapter_num]['page%s'%page_num])
        #print(data[chapter_num][page_num])
        self.total_pages = len(data[chapter_num])-1
        #for i in data['content']:
        #    print(timeline_id)
        #    print(i)
        self.timeline_content = data[chapter_num]['page%s'%page_num][0]
        self.audio_que = data[chapter_num]['page%s'%page_num][1]
        animation_que = data[chapter_num]['page%s'%page_num][2]
        print(animation_que)
        print(type(animation_que))
        #below is logic to play sound with audio player whenever JSON includes data after the line data. logic for determining playback functions and sound selection in AudioPlayer

        f.close()
    def label_draw(self):
        label = pyglet.text.Label(self.label_content,
                font_name='Times New Roman',
                font_size=12,
                x=window.width//2,y=window.height//2,
                anchor_x = 'center', anchor_y='center')
        label.draw()

        #letter loading: label draws character array built from timeline content by method when LATEST
        print(self.timeline_content)
        #print('label drew')
        #print('timeline_id')
    def letter_load(self):
        print(self.current_page)
        if self.current_page < self.latest_page:
            print('BACKLOG')
            self.label_content_index = 0
            self.label_content = self.timeline_content
        if self.current_page == self.latest_page:
            print('LATEST')
            timeline_array = list(self.timeline_content);
            if self.label_content_index > len(timeline_array)-1:
                self.label_content = self.timeline_content
                #turn page animation trigger
                
                return
            else:
                self.label_content = self.label_content + timeline_array[self.label_content_index]
                self.label_content_index = self.label_content_index + 1
                #print('letter load test')
                #print('label content=', self.label_content)
                #print('label content index = ', self.label_content_index)
                #print('timeline array= ', timeline_array)
                #print(timeline_array[self.label_content_index-1])
               # if self.label_content_index >= len(timeline_array)-1:


            '''
                letter = self.label_content + letter + i
                self.label_content = str(letter)
                time.sleep(0.1)
                self.timeline_content = self.label_content
                self.label_draw()
             '''
    def img_draw(self):
        #timeline cues direct reader to load and blit and animate everything inside img_draw. img_draw must be made more robust and image files must draw from elsewhere
        pic = image.load('picture.png')
        pic.blit(0,0)
    def textbox(self, timeline_id):
        print(timeline_id)
    def list_of_actions(timeline_id):
        print(timeline_id)
    def turn_page():
        #loading pic while letter load
        #turns into
        #pic = image.load(turn page indicator.png)
        #pic.blit(0,0)
        pass
    def listen():
        pass
    def autoplayer():
        pass
class AudioPlayer():
    # def __init__(self):
    #     music_player = pyglet.media.Player()
    #     music = pyglet.media.load("theme0.wav")
    #     music_player.queue(music)
    #     #music_player.eos_action = pyglet.media.SourceGroup.loop
    #     music_player.play()
    def play(audio_que):
        print('AUDIO QUE:'+audio_que[1])
        if audio_que[0] == 'PLAY':
            player = pyglet.media.Player()
            source = pyglet.media.load(audio_que[1])
            player.queue(source)
            setattr(player,'loop',True)
            player.play()
            #print('playing'+audio_que[1])
        #check que string for commands: STOP, START, FADE, VOICE, BGM
        #VOICE LINE stop currently playing and play new ones
class AnimPlayer():
    def play():
        pass
