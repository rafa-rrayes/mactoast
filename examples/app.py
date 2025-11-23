import rumps
from mactoast import show_toast
from mactoast.styles import show_info, show_warning, show_error, show_success
import time
class AwesomeToastsApp(rumps.App):
    def __init__(self):
        super(AwesomeToastsApp, self).__init__("Awesome App")
        self.menu = ["Info", "Warning", "Error", "Success"]

    @rumps.clicked("Info")
    def info(self, _):
        show_info(
            message="This is some information.",
            display_duration=1.0,
            fade_duration=1.0,
        )
    @rumps.clicked("Warning")
    def warning(self, _):
        show_warning(
            message="Warning! Check this out.",
            display_duration=0.3,
            fade_duration=0.3,
            font_size=18,
        )
        show_warning(
            message="Warning! Check this out.",
            display_duration=0.3,
            fade_duration=0.3,
            font_size=18,
        )
        show_warning(
            message="Warning! Check this out.",
            display_duration=0.3,
            fade_duration=0.3,
            font_size=18,
        )
    @rumps.clicked("Error")
    def error(self, _):
        show_error(
            message="This is an error message.",
            display_duration=1.0,
            fade_duration=1.0,
            width=300,
            height=80,
            corner_radius=15,
            position=(1200, 800),
            
        )
    @rumps.clicked("Success")
    def success(self, _):
        show_success(
            message="This is a success message.",
            display_duration=1.0,
            fade_duration=1.0,
            width=300,
            height=80,
            corner_radius=15,
        )

if __name__ == "__main__":
    AwesomeToastsApp().run()
