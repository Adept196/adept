# Adept
This is an infinitely extensible RPG created for CS 196 @ UIUC.

## Requirements and Dependences

This project depends on lots of Python packages. If you install these packages, you should be able to run Adept

* [Pygame](http://pygame.org/)
* [Pyyaml](http://pyyaml.org/)
* [noise](https://pypi.python.org/pypi/noise/)

I highly recommend installing all of them via [pip](https://pip.pypa.io/en/stable/), except Pygame. **Adept is only guarunteed to run bug-free if Pygame is installed from [source](https://bitbucket.org/pygame/pygame/src).**

## Installation and Use

* Clone the repository

```git clone https://github.com/Adept196/adept```

* Navigate into the repository and checkout the `develop` branch

```cd adept; git checkout develop```

On this branch, you'll find every feature discussed in the video *except* multithreaded chunk loading. We reworked the chunk system to make it a lot faster and better, but the semester ended before we resolved merge conflicts and merged it into this branch.

* Run the example game

```python main.py```

If you want to take a look our chunk rework and the current state of the editor, you can checkout a different branch.

* Checkout the `editor-draw-and-select-tool` branch

```git checkout editor-draw-and-select-tool```

Both the editor and the example game exhibit the effects of a reworked chunk system. You should notice that there is no noticable I/O freeze every time chunks are loaded and saved. This used to happen when moving to the edge of the screen, when new chunks must be loaded for the first time.

## Takeaways

We learned many things from this project. Some of the biggest were

* Coding best practices
..* Unit tests (we used [nose](https://nose.readthedocs.org/en/latest/))
..* Continuous integration (we used [Travis-CI](https://travis-ci.org/))
..* GitHub branching/merging best practices
..* How to actually do code reviews
..* It's not a good idea to put EVERY FILE IN THE SAME FOLDER
..* It's never a good idea to `git add -A`
* Making things go fast
..* Multithreading
..* High-level memory management (which data structure? etc)
* Making things cross-platform
..* Python
* Using team/organization technologies
..* Slack
..* Trello
..* GitHub
..* Travis-CI

## Authors

* [Thomas Fischer](https://github.com/gragas)
* [Benjamin Congdon](https://github.com/benjamincongdon)
* [Han Song Huang](https://github.com/hhuang97)
* [Sean Duffy](https://github.com/spduffy2)

## License

Do whatever you want