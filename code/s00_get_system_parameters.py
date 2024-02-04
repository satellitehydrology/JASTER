from screeninfo import get_monitors
import platform

primary_monitor = get_monitors()[0]
screen_width  = primary_monitor.width
screen_height = primary_monitor.height

window_width  = int(screen_width/3)
window_height = int(screen_height/4)

OS = platform.system()
z = 5 if OS == 'Windows' else 0
TEXT = int(16 - z)