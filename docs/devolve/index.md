# About

---

## YAML Files
As it stands (05.11.21) Revolve accepts (and saves) robot morphologies in the YAML file format.
YAML files are used for 3 proposes:

1. As an output (storage) file for evolved Robot morphologies created in revolved (compatible with Gazebo).
2. As an input file to the "__INSERT_NAME__" script that generates the controller .config file to run on the raspberry pi.
3. As an input file to some plugin (**TODO: Needs research**) which returns an STL for 3D printing.

For these purposes, YAML files seem to work ok. However, two issues arise. Firstly, it makes it extremely hard to hand-design robots when necessary; as it is for my Robot Zoo project or, for example, when we desire to evolve a brain on a predefined morphology.
Secondly, it makes it hard to easily visualize robots, requiring the start of a Revolve instance, or the use of the unreliable PNG generator (which fails to show the z-dimension of morphologies).

## Creating A Yaml Editor & Visualisation Tool (Devolve)

To combat these issues I have written a visualization program that does the two following things:

1. Import YAML robots file for viewing
2. Make new, or edit, Robots from scratch

I will be using:

- [PyYaml](https://pyyaml.org/) for loading and dumping the files
- [Ursina](https://www.ursinaengine.org/) game engine to do the visualizations

I've called this project "Devolve" as a reference to "Revolve" from which it derives.

---

## Disclaimer
This app is in very early development stage, as such I can't promise it will be completely bug-free.

Feel free to ask me any questions you may have :)

---