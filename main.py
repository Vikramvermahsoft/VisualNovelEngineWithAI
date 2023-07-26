import pyglet
from pyglet.window.event import WindowEventLogger
from pyglet.window import mouse
from pyglet.window import key
#import classes
import time
import json
from pyglet import image

'''Due to unknown reason, Window class must be defined in main.py rather than among the rest in classes.py'''


class Window(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        print('Window created')
        self.game_state = 0
        print('window test')

    def game_state_handler(state_variable):
        if state_variable == 0:
            self.game_state = 0
            #reset
        if state_variable == 1:
            self.game_state = 1
            #menu starts
            #save reader state/save data
            #close reader and other
        if state_variable == 2:
            self.game_state = 2
            #play

            #open reader


        #game state 0 = startup
        #game state 1 = home menu
        #game state 2 = play
        pass

    def on_key_press(self, KEY, MOD):
        print(KEY)
        if KEY == key.LCTRL:
            print('LCTRL pressed')
        if KEY == key.C:
            print('C Key Pressed')
        if KEY == 65307:
            pyglet.app.exit()
    def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
        print(scroll_y)
        if scroll_y > 0 and reader.current_page > 0:
            reader.current_page = reader.current_page - 1
            reader.timeline_read(reader.current_page)
        if scroll_y < 0 and reader.current_page < reader.latest_page-1:
            reader.current_page = reader.current_page + 1
            reader.timeline_read(reader.current_page)
    def on_draw(self):
        self.clear()
        #print(self.game_state)
        if self.game_state == 0:
            #bootup
            self.game_state = 1
        if self.game_state == 1:
            #startmenu
            menu_label = pyglet.text.Label('Press SPACE to begin',
                          font_name='Times New Roman',
                          font_size=36,
                          x=10, y=10)
            menu_label.draw()
            #start menu binary choice tree
            if keys[key.SPACE]:
                #if mousebuttons[mouse.LEFT] is True:
                self.game_state = 2
                current_timeline = reader.timeline_read(reader.current_page)
                print(current_timeline)
                #setattr(music_player,'loop',False)
                music_player.pause()
                music = pyglet.media.load("theme1.wav")
                music_player.queue(music)
                music_player.next_source()


        #get load information from main to present menus
        if self.game_state == 2:


            music_player.play()
            reader.letter_load()
            reader.label_draw()
            reader.img_draw()

        #mouse click logic; detecting mouse on every draw frame
            if mousebuttons[mouse.LEFT] is True:
                print('left click mouse')

                if reader.current_page < reader.total_pages:
                    print('turn page')
                    reader.label_content_index = 0
                    reader.label_content = "";
                    reader.current_page = reader.current_page + 1
                    if reader.current_page > reader.latest_page:
                        reader.latest_page = reader.latest_page + 1
                if reader.current_page == reader.total_pages:
                    print('last page in chapter')
                    #reader.current_page = reader.current_page + 1
                    time.sleep(0.1)
                    #reader.current_page = reader.total_pages + 2
                    reader.current_chapter = reader.current_chapter + 1
                    reader.latest_page = 0
                    reader.current_page = 0
                #play audio on click, might move feels delayed
                if len(reader.audio_que) > 0:
                    audioPlayer = AudioPlayer()
                    audioPlayer.play(reader.audio_que)
                #reader.current_chapter = reader.current_chapter + 1
                reader.timeline_read(reader.current_page)
                #timeline_read is method for displaying line; takes page num
                time.sleep(0.1)
                #reader.label_content = "";
                #print(reader.latest_page)
                #print(reader.total_pages)
            if mousebuttons[mouse.RIGHT] is True:
                print('right click mouse')


                #if mousebuttons[mouse.LEFT] is False and reader.current_page == reader.total_pages:
                #print('last page in chapter')
                #reader.timeline_read(reader.current_page)
'''
            if reader.current_page == reader.total_pages:
                print('last page in chapter')
                reader.timeline_read(reader.current_page)
                time.sleep(0.1)
                reader.current_page = reader.current_page + 1
            if mousebuttons[mouse.LEFT] is True and reader.current_page > reader.total_pages:
                print('new chapter')
                reader.current_chapter = reader.current_chapter + 1
                reader.current_page = 0
                reader.latest_page = 0
                reader.timeline_read(reader.current_page)
'''
''' CLASSES.PY MERGE'''
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

if __name__ == '__main__':

    window = Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    print('main test')
    mousebuttons = mouse.MouseStateHandler()
    keys = key.KeyStateHandler()

    music_player = pyglet.media.Player()
    music = pyglet.media.load("theme0.wav")
    music_player.queue(music)
    setattr(music_player,'loop',True)

    #music_player.eos_action = pyglet.media.SourceGroup.loop
    music_player.play()

    #intros in game state 0, click to skip
    #if game_state = 0:
    #play intros
    #time.sleep()->game_state = 1
    #when game state 0 reaches end, switch to game state 1 and begin menu
    #load save data somewhere in here
    #if game_state = 1
    #load menu buttons
    #reader = classes.Reader()
    reader = Reader()
    print('reader test')
    #page = classes.Page()
    #start_menu = classes.Start_menu()

    window.push_handlers(mousebuttons)
    window.push_handlers(keys)
    #glClearColor(0.5,1,0.7,1)
    print('app will run')
    pyglet.app.run()
    print('app ran')

'''
    Modification of on_draw event in Window
    to draw images, UI, textbox
    Anything that changes to user needs to ultimately be updated here
    All controls go here as well
'''
'''
@window.event
def on_draw():
    window.clear()
    reader.label_draw()
    if mousebuttons[mouse.LEFT] is True:
        print('Left click mouse')
        reader.current_page = reader.current_page + 1
        reader.timeline_read(reader.current_page)
    if mousebuttons[mouse.RIGHT] is True:
        pass
'''
#event_logger = WindowEventLogger()
#window.push_handlers(event_logger)
#print(event_logger)
#print('App tick')
#pyglet.app.run()
