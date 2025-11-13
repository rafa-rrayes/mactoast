import rumps
from mactoast import show_embedded, show_standalone, show_auto
class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App")
        self.menu = ["Preferences", "Silly button", "Say hi"]

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        t = show_auto(
            message="Hello, World!",
            display_duration=1.0,
            fade_duration=1.0,
            width=300,
            height=100,
        )
        t.show()
if __name__ == "__main__":
    AwesomeStatusBarApp().run()
