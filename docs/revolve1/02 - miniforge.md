# Anaconda / Miniforge

[Anconda](https://www.anaconda.com/) is a python and data science package manager.

[Miniconda](https://docs.conda.io/en/latest/miniconda.html)
is an installation option for Anaconda which is lighter
(doesn't install all the GUI frill)
and generally much leaner / faster to use
(in my humble opinion).

Anaconda makes use of many different development channels
(besides the main one from the people of Anaconda)
effectively increasing the number of packages that can be installed through the Anaconda pipeline.

[Conda-forge](https://conda-forge.org/) is one such channel,
and it's widely recognized as the best
(most up-to-date and with most options).


[Mini-forge](https://github.com/conda-forge/miniforge#miniforge)
is a Minconda install that comes with Conda-forge as its main channel.
Mini-forge's selling point is the rapid adoption of new hardware.

<center>
    **Exactly what we need for our (unstable) M1 Mac. <br>
    Thus, "Mini-forge" will be the version of Anaconda we will use.**
</center>

---

## Installation of Mini-forge

Following the installation of Homebrew ([Prerequisites](01 - prerequisites.md)), we can simply write:

```bash
brew install --cask miniforge
```

!!! Warning
    I don't think this is compatible with any other version of Anaconda,
    so make sure to uninstall any other version of Anaconda you may have installed on your system.
    <br><br>
    ***Make sure to export/save all your environments, or they WILL be lost*** <br>
    (I went through the pain of exporting and reinstalling all my environments, so should you)


---

<center>
   Installing Anaconda is **done**
</center>