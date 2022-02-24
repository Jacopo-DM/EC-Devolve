# Pre-requirements

Inspiration: [Install Gazebo on Mac OS X](https://github.com/ci-group/revolve/wiki/Installation-Instructions-for-Gazebo#install-gazebo-on-mac-os-x)
from the [Revolve Wiki](https://github.com/ci-group/revolve/wiki#tutorials).

---


## Running Commands

In these instructions, when instructed to "run a command" of the format:

```bash
some-command some-arguments
```

The user is expected to run the command in the [Terminal](https://en.wikipedia.org/wiki/Terminal_(macOS)) app or any other similar application (eg. [iTerm](https://iterm2.com/))

If the command has some expected outputs, I will use the following format to show this:

```bash
# Expected output:
    some-output
```

Where everything indented after `# Expected output:` is what you'd expect to see in the terminal.

---

## Install [Xcode](https://developer.apple.com/xcode/)

Xcode is the first prerequisite required for the installation.
There are three ways to install Xcode:

- Running the command line instruction `xcode-select --install` in the terminal.
- Agreeing when prompted during the Homebrew installation (next step)
- Download `Xcode` from the [AppStore](https://www.apple.com/app-store/)

The last option takes up more space and installs the Xcode GUI, but it's the method I would suggest, as it minimizes bugs.

!!! warning "Open Xcode"
    **This is important: open `Xcode` once before running, and confirm the user agreement!**

---

## Install [Homebrew](https://brew.sh/)
This is a *must have* package-manager for mac.

[Following the installation instructions]((https://brew.sh/)) on the Homebrew main page, we run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## Install [XQuartz](https://www.xquartz.org/)
The next requirement is Xquartz, which we install using the command:

```bash
brew install xquartz
```

---

## Install Other Miscellaneous Homebrew Dependencies

These are packages that work best when installed using Homebrew

```bash
brew install nlopt bullet libpqxx
```

<!-- ## <center> From this point on, folllowing the Wiki is a ***TRAP.*** <br> it won't work. </center> -->

---

<center>
   Installing prerequisites is **done**
</center>