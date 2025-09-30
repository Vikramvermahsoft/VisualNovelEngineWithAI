import pyglet

# test = pyglet.media.load("resources/media/theme0.wav")
# print(test)

source = pyglet.media.load("resources/media/theme0.wav", streaming=False)
player = pyglet.media.Player()
player.queue(source)
player.play()

pyglet.app.run()
