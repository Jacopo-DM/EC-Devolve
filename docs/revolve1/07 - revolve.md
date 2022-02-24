# Installing Revolve On Mac M1

This is the final part of the installation process.

We move back to our main directory.

```bash
cd /path/to/Revolve-EC
```

---

## Fixing Error In Files
Three of the installation files have errors that need to be fixed for this installation to work, so we have to open them up in our favourite editor (in my case [vs-code](https://code.visualstudio.com/))

### CMakeLists.txt
The first file we will fix can be opened with:
```bash
code cpprevolve/revolve/gazebo/CMakeLists.txt
```

Here we will change all instances of `find_package(gazebo 10` to `find_package(gazebo 11`.
this should appear **twice** in the file ([credits](https://github.com/ci-group/revolve/wiki/Installation-Instructions-for-Revolve)).


### requirements.txt
The second file we will fix can be opened with::
```bash
code requirements.txt
```

Here there are two changes we need to make, the first is removing the version constraint on the `futures` package:

From: `futures==3.0.2` to `futures` (line 3)

The second is commenting out the MultiNEAT installation step (which we already completed previously):

From: `thirdparty/MultiNEAT` to `# thirdparty/MultiNEAT` (line 19)


### supervisor_multi.py
The final file to fix can be opened with:
```bash
code pyrevolve/util/supervisor/supervisor_multi.py
```

This is a tricky change, but one that will break the gazebo process unexpectedly at a later stage.
In the file we must find the line `env['DYLD_LIBRARY_PATH'] = gazebo_libraries_path`, which for me is line 262, and change it to `env['DYLD_LIBRARY_PATH'] = "/opt/homebrew/Caskroom/miniforge/base/envs/ec-64/bin/gzserver"`

The `"/opt/homebrew/Caskroom/miniforge/base/envs/ec-64/bin/gzserver"` part of this line, is the path to the gzserver script in your conda installation, this should be similar if all the steps until now have been followed, but the exact location of this script for your installation can be found using:

```bash
which gzserver
```
```
# Expected output:
  /opt/homebrew/Caskroom/miniforge/base/envs/ec-64/bin/gzserver
```
The output of this command should be the string following `env['DYLD_LIBRARY_PATH'] =`


### Downloading These Files
If you want the exact files I used, or compare your changes with the ones I made, you can [click here to download](../files//fixes.zip) these 3 files.

---

## More Prerequisites

Now that we made fixes to these files, we need to install more conda packages (installing all the requirements in a single step breaks the installation, hence the division).
```
conda install protobuf gsl yaml-cpp -y
```

---

## Installing CPP Revolve
After successful completion of all the steps until now, we can move on to the installation of CPP revolve.
Firstly, from the `Revolve-EC` directory, we need to move one directory up, and export a new symbol:

```bash
cd ..
export SIM_HOME=`pwd`
```

We then go back into the `Revolve-EC` folder, and export another symbol:
```bash
cd Revolve-EC
export REV_HOME=`pwd`
```

Now we need to create a build directory and enter it:
```bash
mkdir -p build
cd build
```

Here we have bunch of new symbols to export:
```bash
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/usr/local
export CPATH=${CPATH}:/usr/local/include
export LIBRARY_PATH=${LIBRARY_PATH}:/usr/local/lib
```

```bash
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/opt/homebrew/opt/tbb@2020_u3
export CPATH=${CPATH}:/opt/homebrew/opt/tbb@2020_u3/include
export LIBRARY_PATH=${LIBRARY_PATH}:/opt/homebrew/opt/tbb@2020_u3/lib
```

```bash
export DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH:/opt/local/lib
```

Once that's done, we can run our cmake and make process:
```bash
cmake .. -DCMAKE_BUILD_TYPE="Release"
make -j4
```
```bash
# Expected output:
  [...]
  [100%] Built target RobotControlPlugin
```

---

## Installing Python Revolve

Now we got to install the python requirements.

We go back to our main directory `Revolve-EC` from `build`:
```bash
cd ..
```

and we run:
```bash
MN_BUILD=boost pip3 install -r requirements.txt
```

Which should run without errors.

---

## Final Conda Installs

Once again, we need to install some conda packages

```bash
conda install pycairo openblas -y

```

This concludes the installation of Revolve.

---

<center>
  Installing Revolve is **done**
</center>