import pyglet
from pyglet.window.event import WindowEventLogger
from pyglet.window import mouse
from pyglet.window import key
import classes
import time

class Window(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
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
            
    def on_draw(self):
        self.clear()
        reader.label_draw()
        if mousebuttons[mouse.LEFT] is True and reader.current_page < reader.total_pages:
            print('left click mouse')
            reader.current_page = reader.current_page + 1
            if reader.current_page > reader.latest_page:
                reader.latest_page = reader.latest_page + 1
            reader.timeline_read(reader.current_page)
            time.sleep(0.1)
            print(reader.latest_page)
            print(reader.total_pages)
        if mousebuttons[mouse.RIGHT] is True:
            print('right click mouse')

if __name__ == '__main__':
    window = Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    mousebuttons = mouse.MouseStateHandler()
    reader = classes.Reader()
    #page = classes.Page()
    #start_menu = classes.Start_menu()
    current_timeline = reader.timeline_read(reader.current_page)
    print(current_timeline)
    window.push_handlers(mousebuttons)
    #glClearColor(0.5,1,0.7,1)
    pyglet.app.run()
    print('app ran')

'''Modificaiton of on_draw event in Window
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
