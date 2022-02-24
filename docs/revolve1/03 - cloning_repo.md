# Cloning The Revolve Repo

Inspiration: [Installation Instructions for Revolve](https://github.com/ci-group/revolve/wiki/Installation-Instructions-for-Revolve)

---

## Main Directory

We start by opening (in the terminal) a folder where you're comfortable installing Revolve.

```bash
cd /link/to/your/directory
```

Then we can pull the repository
```bash
git clone https://github.com/ci-group/revolve.git Revolve-EC --recursive
```

The `Revolve-EC` at the end of `git clone` is what I want to call the folder,
choose whatever you like, default is: `revolve`

Enter the directory:
```bash
cd Revolve-EC
```

From this point on, this location is what I refer to as "main directory".

---

## EC Research Branch

After downloading the project, we need to choose a branch to work on: <br>
mine will be `ec_2021_research`.

We move branches by doing:


```bash
git checkout ec_2021_research
```
```bash
# Expected output:
    branch 'ec_2021_research' set up to track 'origin/ec_2021_research'.
    Switched to a new branch 'ec_2021_research'
```

Next, we need to pull the submodules which aren't downloaded by default:

```bash
git submodule update --init --recursive
```
```bash
# Expected output:
    Submodule 'thirdparty/MultiNEAT' (https://github.com/ci-group/MultiNEAT.git) registered for path 'thirdparty/MultiNEAT'
    Cloning into '/link/to/your/directory/Revolve-EC/thirdparty/MultiNEAT'...
    Submodule path 'thirdparty/MultiNEAT': checked out '7f40de3631b37270c73f367eb41456d3f1b09be5'
```

---

## MultiNEAT
Finally, we get the latest version of MultiNEAT, the latest version prevents bugs in later steps:
```bash
cd thirdparty/MultiNEAT
git checkout master
```

```bash
# Expected output:
    Previous HEAD position was 7f40de3 Simplified python binding compilation
    Switched to branch 'master'
    Your branch is up to date with 'origin/master'.
```

Pull all required submodules of MultiNEAT
```bash
git submodule update --init --recursive
```
```bash
# Expected output:
    Submodule 'thirdparty/boost-python' (https://github.com/boostorg/python) registered for path 'thirdparty/boost-python'
    Cloning into '/link/to/your/directory/Revolve-EC/thirdparty/MultiNEAT/thirdparty/boost-python'...
    Submodule path 'thirdparty/boost-python': checked out 'aee2667407736593bfbc81836e64d9d743d10481'
```

---

<center>
   Cloning the Revolve repository is **done**
</center>
