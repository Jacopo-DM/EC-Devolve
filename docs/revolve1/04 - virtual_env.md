# Making Our Conda Environment

Now that we have Mini-forge, we can start installing Conda packages.
To know what packages we can install, we got to find a list of all available packages.
One such list, for conda-forge, can be found
[here](https://conda.anaconda.org/conda-forge/).

If we select the `osx-arm64` tab, we can further see what packages have arm (M1) integration.<br>
As can be noted, the packages we need (eg. gazebo) are not under this tab.

Indeed, if we run `conda install gazebo`
we get the following error:

```
PackagesNotFoundError: The following packages are not available from current channels:

  - gazebo
```

We need to create a `osx-64` environment,
this can easily be done. <br>
However, before we can move onwards, we need some preparation.

<!-- ## Getting The `requirements.txt`

In the later steps of [Revolve installation](revolve.md),
we are asked to make a virtual env, using a given `requirements.txt`.

Ideally, the env we are about to create would be sufficient,
therefore we go to the main folder, and we find the file `requirements.txt`.

 -->

---

## Setting Up An Intel Conda Environment

In this step, we set up an appropriate "[anaconda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)" that ensures only versions of libraries compatible with M1 are installed.

Following [this git issue](https://github.com/conda-forge/miniforge/issues/165#issuecomment-860233092)
The solution posted by `isuruf` worked great for me.

!!! Warning
    The official instructions indicate using python version 3.7.
    I've had problems with 3.7, particularly with MultiNEAT,
    so a safer option, in this case, is Python 3.8

Create a Python environment called `ec-64`:
```bash
CONDA_SUBDIR=osx-64 conda create -n ec-64 python=3.8 -y
```

Activate the newly created env:
```bash
conda activate ec-64
```

Check  if Python recognizes the correct OS version:
```bash
python -c "import platform;print(platform.machine())"
```

```bash
# Expected output:
    x86_64
```

Set the correct `CONDA_SUBDIR` configuration variable:
```bash
conda env config vars set CONDA_SUBDIR=osx-64
```

```bash
# Expected output:
    To make your changes take effect please reactivate your environment
```

Deactivate env and re-activate to ensure changes take effect:
```bash
conda deactivate && conda activate ec-64
```

Check that the configuration variable is properly set:
```bash
echo "CONDA_SUBDIR: $CONDA_SUBDIR"
```

```bash
# Expected output:
  CONDA_SUBDIR: osx-64
```

---


<center>
  Creating an isolated conda env is **done**
</center>
