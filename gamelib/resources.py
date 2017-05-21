"""
1. Drop this module into your game folder.
2. Tweak pyglet.resource.path[].
3. Insert custom resource loading (streaming sounds, fonts).
4. Import the module.
5. Refer to images and sounds as resources.your_resource. Automatically updates
	when you add new resources to your folder.
"""

import pyglet, os

#Change this to fit your folder structure
pyglet.resource.path=['data']
pyglet.resource.reindex()

exclude = ['unwanted_file_example']

function_pairs = {
	#'ext':(func, {args})
	#I only implemented the most common formats. Copy/paste to do more.
	'bmp':(pyglet.resource.image,{}),
	'gif':(pyglet.resource.image,{}),
	'png':(pyglet.resource.image,{}),
	'mp3':(pyglet.resource.media,{'streaming':False}),
	'ogg':(pyglet.resource.media,{'streaming':False}),
	'wav':(pyglet.resource.media,{'streaming':False}),
	'ttf':(pyglet.resource.add_font,{})
}

for path in pyglet.resource.path:
	for file_name in os.listdir(path):
		name, ext = os.path.splitext(file_name)
		if name not in exclude:
			for key, (func, kwargs) in function_pairs.iteritems():
				if ext == '.'+key and os.path.exists(path):
					globals()[name] = func(file_name,**kwargs)


#custom stuff
for img in [bullet, missile]:
    img.anchor_x, img.anchor_y = img.width // 2, img.height - 4

for img in [copter, drone, gunner, flare1, flare2, flare3, flare4, flare5, 
            turret, boss_arm, boss_head, boss_track, drone1, drone2, drone3, 
            charger, charger_burn, enemy_bullet, blimp1, blimp2, blimp3]:
    img.anchor_x, img.anchor_y = img.width // 2, img.height // 2
    
for img in [scaffold]:
    img.anchor_x, img.anchor_y = img.width // 2, 0 

pyglet.font.load(prstartk)


heligrid = pyglet.image.ImageGrid(heli,4,1)
for i in heligrid:
    i.anchor_x = 64
    i.anchor_y = 18
heli = heligrid.get_animation(0.03)

drone = pyglet.image.Animation.from_image_sequence([drone1,drone2,drone3,drone2],0.08)
blimp = pyglet.image.Animation.from_image_sequence([blimp1,blimp2,blimp3,blimp2],0.08)