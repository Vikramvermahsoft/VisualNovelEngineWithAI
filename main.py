import pyglet
from pyglet.window.event import WindowEventLogger
from pyglet.window import mouse
from pyglet.window import key
import classes
import time

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

        #get load information from main to present menus
        if self.game_state == 2:

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
            '''if reader.current_page == reader.total_pages:
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
if __name__ == '__main__':
    
    window = Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    print('main test')
    mousebuttons = mouse.MouseStateHandler()
    keys = key.KeyStateHandler()
    #intros in game state 0, click to skip
    #if game_state = 0:
    #play intros
    #time.sleep()->game_state = 1
    #when game state 0 reaches end, switch to game state 1 and begin menu
    #load save data somewhere in here
    #if game_state = 1
    #load menu buttons
    reader = classes.Reader()
    print('reader test')
    #page = classes.Page()
    #start_menu = classes.Start_menu()
    current_timeline = reader.timeline_read(reader.current_page)
    print(current_timeline)
    window.push_handlers(mousebuttons)
    window.push_handlers(keys)
    #glClearColor(0.5,1,0.7,1)
    print('app will run')
    pyglet.app.run()
    print('app ran')

'''Modification of on_draw event in Window
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
