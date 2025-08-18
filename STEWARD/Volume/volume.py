import keyboard  # for key press detection
import pycaw.pycaw as pycaw  # for volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class VolumeController:
    def __init__(self):
        # Initialize volume control interfaces
        devices = pycaw.AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            pycaw.IAudioEndpointVolume._iid_, 
            CLSCTX_ALL, 
            None)
        self.volume = cast(interface, POINTER(pycaw.IAudioEndpointVolume))
        
    def get_volume(self):
        # Get current volume (0.0 to 1.0 scale)
        return self.volume.GetMasterVolumeLevelScalar()
    
    def set_volume(self, level):
        # Set volume (clamped between 0.0 and 1.0)
        level = max(0.0, min(1.0, level))
        self.volume.SetMasterVolumeLevelScalar(level, None)
    
    def increase_volume(self, step=0.05):
        current = self.get_volume()
        self.set_volume(current + step)
        print(f"Volume increased to: {int(self.get_volume() * 100)}%")
    
    def decrease_volume(self, step=0.05):
        current = self.get_volume()
        self.set_volume(current - step)
        print(f"Volume decreased to: {int(self.get_volume() * 100)}%")

def main():
    print("Volume control started. Press up/down arrows to adjust volume. Press ESC to quit.")
    controller = VolumeController()
    
    # Register hotkeys
    keyboard.add_hotkey('up', controller.increase_volume)
    keyboard.add_hotkey('down', controller.decrease_volume)
    
    # Wait for ESC key to exit
    keyboard.wait('esc')
    print("Volume control exited.")

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("Required libraries not found. Please install them with:")
        print("pip install keyboard pycaw comtypes")
    except Exception as e:
        print(f"An error occurred: {e}")
