import os

import mapManager

class PluginManager:
    """
    Manages which plugins are loaded.
    It should be noted that plugins are not objects themselves.
    A plugin is not an object implemented in this program.
    The name plugin refers to any Map, Skill, etc.
    """

    BASE_PATH = [""] # BASE_PATH is a list version of the base path in which PluginManager
                     # will search for plugins. For example, if the base path should be
                     # a/anotherfolder/ then BASE_PATH should equal ["a","anotherfolder"]
    mapNames  = []   # mapNames is a list of strings which represent the names of maps that
                     # should be loaded

    @staticmethod
    def loadPlugins():
        """
        loadPlugins loads all the plugins that are checked in the plugins manager file
        """
        with open(os.path.join(*list(PluginManager.BASE_PATH + ["plugins.txt"]))) as pfile:
            for line in pfile:
                words = line.split()
                if len(words) >= 2:
                    if words[0] == "map":
                        PluginManager.mapNames.append(words[1])
        mapManager.MapManager.loadMaps()
