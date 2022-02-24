# Installing MultiNEAT

The installation of MultiNEAT is divided into two parts, the Python installation and the C++ library installation. The order we install these matters, we start with the Python installation.


---
## Python Installation

### Set Up
After activating our new env with:
```bash
conda activate ec-64
```

As well as having followed the previous steps (installing prerequisites and gazebo).

We need to go to the MultiNEAT subdirectory, which (assuming you're in the Revolve-EC folder) is done with:
```bash
cd thirdparty/MultiNEAT
```

### Installing Requirements
Once in the right directory, the first step of the requirements installation process is as follows:
```bash
conda install --file requirements.txt -y
```

### Boost Install
Finally, we need to run the boost installation of MultiNEAT with the following command:
```bash
MN_BUILD=boost pip3 install .
```

### Checking The MultiNEAT Install
Leaving the MultiNEAT sub-directory, back to the main Revolve-EC folder:
```bash
cd ../..
```

!!! warning
    Exiting the MultiNEAT subdirectory is essential for the next command to work.


We can check that the python installation was successful with the following command:
```bash
python -c "import multineat"
```

We expect this to return blank (not raise any errors).

---

## C++ Installation

Still, with the `ec-64` env active, we go back to the MultiNEAT subdirectory
```bash
cd thirdparty/MultiNEAT
```

We make a directory `build` and we enter it:
```bash
mkdir -p build
cd build
```

Finally, we run the necessary `cmake` and `make` processes (the sudo command will request the user password):
```bash
cmake ..
make -j4 ..
sudo make -j4 install
```
```bash
# Expected output
    [...]
    [100%] Built target MultiNEAT
    Install the project...
    [...]
```

<!-- Finally we can remove the build folder:
```bash
cd ..
rm -r build
```` -->

---

<center>
    Installing MultiNEAT is **done**
</center>