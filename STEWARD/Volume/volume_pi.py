import keyboard  # For key detection
import subprocess  # To run shell commands

class VolumeController:
    def __init__(self):
        self.step = 5  # Volume step (5%)
        self.min_volume = 0
        self.max_volume = 100

    def get_volume(self):
        # Get current volume using amixer (ALSA)
        cmd = "amixer get Master | grep -o '[0-9]*%' | head -n 1 | tr -d '%'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        try:
            return int(result.stdout.strip())
        except:
            return 50  # Default if error

    def set_volume(self, level):
        level = max(self.min_volume, min(self.max_volume, level))
        # Set volume using amixer
        subprocess.run(f"amixer set Master {level}%", shell=True)
        print(f"Volume: {level}%")

    def increase_volume(self):
        current = self.get_volume()
        self.set_volume(current + self.step)

    def decrease_volume(self):
        current = self.get_volume()
        self.set_volume(current - self.step)

def main():
    print("Volume control started. Press ↑/↓ arrows to adjust volume. Press ESC to quit.")
    controller = VolumeController()

    keyboard.add_hotkey('up', controller.increase_volume)
    keyboard.add_hotkey('down', controller.decrease_volume)

    keyboard.wait('esc')
    print("Volume control exited.")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Required libraries not found. Install them with:")
        print("pip install keyboard")
    except Exception as e:
        print(f"Error: {e}")
