
import pyglet
import sys
import os
from pyglet.window.event import WindowEventLogger
from pyglet.window import mouse
from pyglet.window import key
#import classes
import time
from datetime import datetime
import json
from pyglet import image
from pyglet.graphics import Batch

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
            #ESCAPE key pressed
            pyglet.app.exit()
        if KEY == 65470:
            #F1 pressed
            if self.game_state ==3:
                memory.save()
        if KEY == 65471:
            #F2 pressed
            memory.load()

    def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
        print(scroll_y)
        if self.game_state == 3:
            if scroll_y > 0 and reader.current_page > 0 and reader.current_page < reader.total_pages:
                reader.current_page = reader.current_page - 1
                reader.timeline_read(reader.current_page)
            if scroll_y < 0 and reader.current_page < reader.latest_page-1 and reader.current_page < reader.total_pages:
                reader.current_page = reader.current_page + 1
                reader.timeline_read(reader.current_page)

    def on_mouse_release(self,x,y,button, modifiers):
        print(button)
        if button == 1:
            #print('left click mouse')

            if self.game_state == 3:

            #if game in play mode
                #if Backlog
                if reader.current_page < reader.latest_page:
                    reader.label_content = ""
                    #turn page with BACKLOG
                    reader.current_page = reader.current_page + 1
                    #reader.timeline_read(reader.current_page)
                #if Current
                else:

                    #if currently letter loading
                    if reader.label_content_index < len(reader.timeline_array)-1:

                        print('currently letterloading, skipping')
                        #time.sleep(0.1)
                        #skip letterloading
                        #reader.label_content_index = 0
                        reader.label_content = ""
                        reader.label_content = reader.timeline_content

                        #reader.latest_page = reader.latest_page + 1

                        reader.label_content_index == len(reader.timeline_array)
                    #being Latest, if letterloading will load all the text without doing anything else,  increase
                    reader.latest_page = reader.latest_page + 1


                    #if letter loading finished
                    if reader.label_content_index > len(reader.timeline_array)-1:
                        if reader.current_page < reader.total_pages:
                            print('turn page')
                            reader.label_content_index = 0
                            reader.label_content = "";
                            reader.current_page = reader.current_page + 1
                            # if reader.current_page > reader.latest_page:
                            #     reader.latest_page = reader.latest_page + 1

                            #reader.latest_page = reader.latest_page + 1
                            if reader.latest_page == reader.total_pages:
                                print('CHAPTER END')

                        # if reader.current_page == reader.total_pages:
                        #
                        #     #reader.current_page = reader.current_page + 1
                        #
                        #     #reader.current_page = reader.total_pages + 2
                        #     reader.current_chapter = reader.current_chapter + 1
                        #     reader.latest_page = 0
                        #     reader.current_page = 0
                        #     print('new chapter started')

                    #reader.current_chapter = reader.current_chapter + 1
                    if reader.current_chapter == reader.total_chapters:
                        completion.route_finish()
                        pyglet.app.exit()
                reader.timeline_read(reader.current_page)

    def on_draw(self):
        self.clear()
        print('COMPLETION:%s'%completion.report())
        print("DATA LENGTH %s"%reader.total_chapters)
        print("CURRENT CHAPTER %s"%reader.current_chapter)
        print('TOTAL PAGES:%s'%reader.total_pages)
        #pyglet.graphics.Batch().draw()
        #print(self.game_state)
        #mouse click logic; detecting mouse on every draw frame
        if self.game_state == 1:
            reader.menu_draw()
        if self.game_state == 3:
            reader.img_draw()
            reader.character_draw()
            reader.letter_load()
            print("INVERSION:%d" % reader.inversion)
            reader.label_draw(reader.inversion)

            if reader.current_page < reader.latest_page:
                #backlog
                pass
            else:
                if reader.current_page == reader.total_pages:

                    #reader.current_page = reader.current_page + 1

                    #reader.current_page = reader.total_pages + 2
                    reader.current_chapter = reader.current_chapter + 1
                    if reader.current_chapter == reader.total_chapters:
                        completion.route_finish()
                        pyglet.app.exit()

                    reader.latest_page = 0
                    reader.current_page = 0
                    print('new chapter started')
                #new chapter
                if reader.label_content_index > len(reader.timeline_array)-1:
                    print("Letter loading finished")
                    if reader.current_page == 0:
                    #if new chapter
                        reader.save_label_draw()
            reader.speaker_label_draw()




        if mousebuttons[mouse.LEFT] is True:
            print('left click mouse')

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
        self.speaker_content =""
        #timeline content uploaded from timeline.json, transfer to label content for display
        self.label_content_index = 0
        self.latest_page = 0
        #latest page set to 0 every chapter. part of save load data?
        self.total_pages = 0
        #comes from timeline.json, how many pages in a chapter
        self.total_chapters = 1
        self.audio_que = ""
        self.animation_que = {}
        self.animation_counter = 0
        self.image_array = []
        self.timeline_array = []
        self.character_que = {}
        self.inversion = 0
        #self.page_location = 720
        print('Reader created')
    def timeline_read(self,timeline_id):
        self.current_page = timeline_id
        #chapter_num = 'chapter'+str(self.current_chapter)
        chapter_num = self.current_chapter
        page_num = str(self.current_page)
        f = open('timeline.json')
        data = json.load(f)
        #print(timeline_id)
        #print(data)
        #print(data[0])
        #print(data[chapter_num]['page%s'%page_num])
        #print(data[chapter_num][page_num])
        # print("DATA LENGTH %s"%len(data))
        # print("CURRENT CHAPTER %s"%self.current_chapter)
        self.total_chapters = len(data)
        if self.current_chapter == self.total_chapters:
            completion.route_finish()
            print("route:%d" % completion.report())
        else:
            self.total_pages = len(data[chapter_num])-1
            #for i in data['content']:
            #    print(timeline_id)
            #    print(i)
            timeline_que = data[chapter_num]['page%s'%page_num][0]
            audio_que = data[chapter_num]['page%s'%page_num][1]
            animation_que = data[chapter_num]['page%s'%page_num][2]
            character_que = data[chapter_num]['page%s'%page_num][3]

            #if timeline_que != None:
            if len(timeline_que)>0:
                #if timeline_que[1]:
                self.timeline_content = timeline_que[1]
                #if timeline_que[0]:
                self.speaker_content = timeline_que[0]
                if len(timeline_que)>2:
                    self.inversion = timeline_que[2]
            else:
                self.timeline_content = ""
                self.speaker_content = ""
            if len(audio_que)>0:
                self.audio_que = audio_que
            else:
                self.audio_que = ["",""]
            if len(animation_que)>0:
                self.animation_que = animation_que
            if len(character_que)>0:
                self.character_que = character_que
            else:
                self.character_que = []

        #print(self.animation_que)
        #print(type(self.animation_que))
        #below is logic to play sound with audio player whenever JSON includes data after the line data. logic for determining playback functions and sound selection in AudioPlayer

        f.close()
    def label_draw(self, inversion):
        print("CURRENT PAGE:%s"%self.current_page)
        print("LATEST PAGE:%s"%self.latest_page)

        # document_content = "{.margin_left '150px'}{font_name 'Chrono Cross'}{font_size 28}"+self.label_content+"{color (0, 0, 0, 255)}"
        if inversion == 1:
            print("INVERTED")
            document_content = ""
            document_content = "{.margin_left '150px'}{font_name 'Chrono Cross'}{font_size 28}{color (255, 255, 255, 255)}"+self.label_content
        else:
            document_content = "{.margin_left '150px'}{font_name 'Chrono Cross'}{font_size 28}"+self.label_content

        document = pyglet.text.decode_attributed(document_content)
        #document.font_name = 'Chrono Cross'
        #document.font_size = 24
        #document.anchor_x = 'center'
        #document.anchor_y = 'center'
        # label = pyglet.text.HTMLLabel('<font face="Chrono Cross" size="24" color=(0, 0, 0, 255)>'+self.label_content+'</font>',
        #         #font_name='Chrono Cross',
        #         #font_size=24,
        #         x=window.width//2,y=window.height//2,
        #         anchor_x = 'center',
        #         anchor_y='center',
        #         #color=(0, 0, 0, 255)
        #         )
        width = window.width//1.35
        height = window.height//2
        layout = pyglet.text.layout.TextLayout(document, width ,height, wrap_lines=True, multiline=True)

        #label.draw()
        layout.draw()

        #letter loading: label draws character array built from timeline content by method when LATEST
        #print(self.timeline_content)
        #print('label drew')
        #print('timeline_id')
    def save_label_draw(self):
        document_content1 = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}New Chapter: Press F1 to SAVE game"

        document1 = pyglet.text.decode_attributed(document_content1)

        width = window.width//1.35
        height = 50
        layout1 = pyglet.text.layout.TextLayout(document1, width ,height, wrap_lines=True, multiline=True)

        #label.draw()
        layout1.draw()
    def speaker_label_draw(self):
        if len(self.speaker_content) == 0:
            pass
        else:
            document_content2 = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}{bold True}"+self.speaker_content+":"


            document2 = pyglet.text.decode_attributed(document_content2)

            width = window.width//1.35
            height = window.height//2
            layout2 = pyglet.text.layout.TextLayout(document2, width ,height, wrap_lines=True, multiline=True)

            #label.draw()
            layout2.draw()

    def letter_load(self):
        #print(self.current_page)
        #print('Label content index:' + str(self.label_content_index))
        if self.current_page < self.latest_page:
            print('BACKLOG')
            self.label_content_index = 0
            self.label_content = self.timeline_content
        if self.current_page == self.latest_page and self.latest_page != self.total_pages:
            print('LATEST')
            self.timeline_array = list(self.timeline_content);
            print(self.timeline_array)
            if self.label_content_index > len(self.timeline_array)-1:
                print('letter loading finished')
                self.label_content = self.timeline_content
                #turn page animation trigger

                return
            else:
                print('CURRENT CHARACTER')
                #print(self.timeline_array[self.label_content_index])
                #line break for / character or check array length
                # if self.timeline_array[self.label_content_index] == '/':
                #     self.label_content = self.label_content + '\\'
                #     #self.page_location= self.page_location - 10
                #     self.label_content_index = self.label_content_index + 1


                #add current_character to current label content
                current_character = self.timeline_array[self.label_content_index]
                self.label_content = self.label_content + current_character
                print(self.label_content)
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

        print('img_draw called')
        frames = self.animation_que
        #print(len(frames))
        #image_array = self.image_array
        count = self.animation_counter
        if count < len(frames) and len(frames) > 0:
            print(count)
            current_pic = pyglet.image.load(frames[count-1])
            #print(f"{current_pic} = CURRENT PIC")
            #pic = image.load(current_pic)
            pic = current_pic
            pic.blit(0,0)
        #Test reaction images below
        #test_pic = pyglet.image.load('picture.png')
        #test_pic.blit(0,0)

    def character_draw(self):
        #two options here:
            #have a naming convention for file names
            #have character name[0] pull a seperate json of filenames based on emotion[1]
        #for the beta let us stick with the first option while including the design for the second
        if len(self.character_que) != 0:
            character_frames = self.character_que[0]
            character_side = self.character_que[1]
            test_pic = pyglet.image.load(character_frames)
            if character_side == "left":
                test_pic.blit(0,0)
            if character_side == "right":
                test_pic.blit(1000,0)


    def page_turn_draw(self):
        print('page_turn_draw called')

        '''
        frames = self.animation_que
        print(len(frames))
        image_array = self.image_array
        if self.animation_counter > len(frames):
            self.animation_counter = 0
            print('loop reset')
        if self.animation_counter < len(frames):
            count = self.animation_counter
            print(count)
            current_pic = pyglet.image.load(frames[count])

            image_array.append(
                pyglet.image.AnimationFrame(current_pic, duration=0.1)
            )
            print('appended {y}'.format(y=frames[count]))
            self.animation_counter = count + 1
        #print(image_array)
        '''
        '''
        image_array = self.image_array
        print(image_array)
        current_animation = pyglet.image.Animation(frames=image_array)
        sprite = pyglet.sprite.Sprite(
            img = current_animation
        )
        sprite.scale = .25
        print(sprite)
        print(image_array)
        print(current_animation)
        sprite.draw()
        print('sprint drew')
        '''
        '''
        current_pics = self.animation_que
        #animation = pyglet.image.AbstractImageSequence
        frames = []
        frames.append(
            pyglet.image.AnimationFrame(current_pics, duration=0.1)
        )
        for x in range(len(current_pics)):
            print(current_pics[x])
            image = pyglet.image.load(
                current_pics[x].format(x = x)

            )
            print(image)
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2
            frames.append(
                pyglet.image.AnimationFrame(image, duration=0.1)
            )

        current_animation = pyglet.image.Animation(frames=frames)
        sprite = pyglet.sprite.Sprite(
            img = current_animation
        )
        '''
        #animation.__setitem__ = self.animation_que
        #print(current_pic)
        #pic = image.load(current_pic)
        #pic.blit(0,0)
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
    def menu_draw(self):

        menu_label = pyglet.text.Label('Press SPACE to begin, F2 to LOAD chapter',
                      font_name='Chrono Cross',
                      font_size=36,
                      x=10, y=10,
                      color=(0, 255, 0, 255))
        #chrono_cross = menu_label.get_style("Chrono Cross")
        # menu_label.set_style(0,
        #
        # {
        #     "color": (255, 255, 255,1)
        # })
        #menu_label.set_style("Chrono Cross",color=(255,255,255,1))
        menu_label.draw()

class Memory():
    def __init__(self):
        #there needs to be an if else that looks for exisitng save file upon start up, perhaps new method. this method will trigger at game_state
        self.dictionary = {
            "name":"autosave",
            "chapter":"",
            "completion":0,
            "date_saved":""
        }
    def save(self):
        self.dictionary['chapter'] = reader.current_chapter
        print(datetime.now())
        self.dictionary['date_saved'] = str(datetime.now())
        with open('save_data.json', 'w') as outfile:
            json.dump(self.dictionary, outfile)
        #print(self.dictionary)
    def load(self):
        with open('save_data.json', 'r') as openfile:
            json_object = json.load(openfile)
        #print(json_object)
        self.dictionary['chapter'] = json_object['chapter']
        reader.current_chapter = self.dictionary['chapter']
        reader.latest_page = 0
        #print(self.dictionary)

class Completion():
    def __init__(self):
        self.current_route = Memory().dictionary['completion']
    def route_finish(self):
        self.current_route = self.current_route + 1
        Memory().dictionary['completion'] = self.current_route
    def report(self):
        return Memory().dictionary['completion']

class AudioPlayer():
    # def __init__(self):
    #     music_player = pyglet.media.Player()
    #     music = pyglet.media.load("theme0.wav")
    #     music_player.queue(music)
    #     #music_player.eos_action = pyglet.media.SourceGroup.loop
    #     music_player.play()
    def play(audio_que):
        #print('AUDIO QUE:'+audio_que[1])
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
    clock = pyglet.clock
    window = Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    window.set_size(1280, 720)

    # cursor = pyglet.image.load('cursor.png')
    # image_cursor = pyglet.window.ImageMouseCursor(cursor, 16, 8)
    # window.set_mouse_cursor(image_cursor)

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
    memory = Memory()
    completion = Completion()
    print('COMPLETION:%s'%completion.report())
    #print('reader test')
    #page = classes.Page()
    #start_menu = classes.Start_menu()

    #pyglet.sprite.Sprite(img=pyglet.image.load('picture.png')).draw()

    pyglet.font.add_file('Chrono Cross.ttf')
    pyglet.font.load('Chrono Cross')
    # Get the font name used at character index 0
    #font_name = document.get_style('Chrono Cross', 0)

    # Set the font name and size for the first 5 characters
    #document.set_style(0, 5, dict(font_name='Chrono Cross', font_size=12))

    # def callback(dt):
    #     print(f"{dt} seconds since last callback")
    # def drawFrames(dt):
    #     print("frame drawn")
    def tick(dt):
        #print('tick')
        print(f"{dt} seconds since last callback")

        if window.game_state == 0:
            #bootup
            window.game_state = 1
        if window.game_state == 1:
            #startmenu
            #reader.menu_draw()
            print('game state = 1')

            #start menu binary choice tree
            if keys[key.SPACE]:
                #if mousebuttons[mouse.LEFT] is True:
                window.game_state = 2

                #setattr(music_player,'loop',False)
                music_player.pause()

        if window.game_state == 2:
            #main menu
            window.game_state = 3
            #get load information from main to present menus
        if window.game_state == 3:
            current_timeline = reader.timeline_read(reader.current_page)
            print(current_timeline)
            if reader.audio_que != None:
                music_que = reader.audio_que[0]
                if not music_que:
                    pass
                else:
                    music = pyglet.media.load(reader.audio_que[1])
                    if reader.current_page == reader.latest_page:
                        if music_player.playing == True:
                            if reader.audio_que[0] == 'STOP':
                                music_player.pause()
                        else:
                            if music_player.playing != True:
                                if reader.audio_que[0] == 'PLAY':
                                    music_player.queue(music)
                                    music_player.next_source()
                                    music_player.play()

            #reader.letter_load()
            #reader.label_draw()
            '''
            Animation code below. called every draw frame, if timeline->reader->image_array variable is not empty
            '''

            frames = reader.animation_que
            frames_length = len(frames)
            image_array = reader.image_array
            count = reader.animation_counter

            if frames_length > 0:
                print('images present')

                if len(image_array) <= frames_length:
                    #increment frame counter
                    #current frame(stored in class, accessed and updated from here), total frames, starting frame, next frame,
                    print('animation counter:{}'.format(count))
                    if count < frames_length:
                        print(count)
                        '''
                        current_pic = pyglet.image.load(frames[count])

                        image_array.append(
                            #pyglet.resource.image(frames[count])
                            pyglet.image.AnimationFrame(current_pic, duration=0.1)
                        )
                        print('appended {y}'.format(y=frames[count]))
                        print(len(image_array))
                        '''
                        count = count + 1
                        reader.animation_counter = count
                        print('new count: {}'.format(count))
                        #reader.img_draw()


                    if count == frames_length or count > frames_length:
                        count = 0
                        reader.animation_counter = count
                        print('loop reset')

                if len(image_array) == frames_length:

                    reader.image_array = image_array

                    ''' Animate here?'''

                    #ani = pyglet.image.Animation.from_image_sequence(image_array, duration=0.1, loop=True)

                    '''
                    current_animation = pyglet.image.Animation(frames=image_array)
                    sprite = pyglet.sprite.Sprite(
                        img = current_animation
                    )
                    sprite.scale = .25
                    '''
                    #sprite.draw()
                    #print('sprite drawn')

                    image_array = []
                    reader.image_array = image_array
                    print('ANIMATIONS CLEARED')









    clock.schedule_interval(tick, 0.04)
    window.push_handlers(mousebuttons)
    window.push_handlers(keys)
    #glClearColor(0.5,1,0.7,1)
    print('app will run')
    pyglet.app.run()
    print('app ran')
'''
    image_array = reader.image_array
    print(image_array)
    if(len(image_array)>1):

        current_animation = pyglet.image.Animation(frames=image_array)
        sprite = pyglet.sprite.Sprite(
            img = current_animation
        )
        sprite.scale = .25
        print(sprite)
        print(image_array)
        print(current_animation)
        sprite.draw()
        print('sprint drew')
'''

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
