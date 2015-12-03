import sys
import pygame
import unittest
from buffalo import utils
from buffalo.scene import Scene
from buffalo.tray import Tray

class TestScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.trays.add(Tray((5,5), (150, 150)))

    def on_escape(self):
        sys.exit()

    def blit(self):
        pass

class TestCharacter(unittest.TestCase):
    def tear_down(self):
        pygame.quit()

    def test_creation(self):
        if not utils.init(
                caption="Adept",
                fullscreen=True       
        ):
            print("buffalo.utils failed to initialize")
            pygame.quit()
            raise RuntimeError
        utils.set_scene(TestScene())
        for _ in range(5):
            utils.scene.logic()
            utils.scene.update()
            utils.scene.render()
            utils.delta = utils.clock.tick( utils.FRAMES_PER_SECOND )
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
