# Using Devolve

In this section, I will explain how to use Devolve

---

## Camera Control

Once the app is selected, the camera controls are easy:

### Zooming (Scroll)
You can zoom by **scrolling the mouse-wheel**

<center>
<video autoplay loop width="500">
  <source src="../vids/zoom.mp4" type="video/mp4">
</video>
</center>

### Rotating (Right Hold)
You can rotate the model by **right-clicking, holding the click and moving the mouse**.

<center>
<video autoplay loop width="500">
  <source src="../vids/rotate.mp4" type="video/mp4">
</video>
</center>

### Panning (Center Hold)
You can pan the view by **middle-clicking the mouse, holding the click and moving the mouse**.

<center>
<video autoplay loop width="500">
  <source src="../vids/pan.mp4" type="video/mp4">
</video>
</center>

### Change View
Clicking the "Change View" will toggle between four different views/camera positions:

- Frontal
- Diagonal
- Side-view
- Top-view


<center>
<img src="../imgs/view.jpg" width="650"/>
</center>

---

## Building Models

We can build models by adding and removing blocks from the core.

### Adding Blocks (Left Click)

When hovering over a block, it will flash **lime**, which means a block can be added. <br>
A block can be added by **left-clicking** on the surface on which to add the block.

!!! warning "Side Compatibility"
    Not all sides are compatible with addition; only 'up', 'down', 'left' and 'right'. <br>
    'Front' and 'back' don't have any mounting points

<center>
<video autoplay loop width="500">
  <source src="../vids/add.mp4" type="video/mp4">
</video>
</center>


### Remove Blocks (Right Click)

When hovering over a block, it will flash **lime**, which means a block can be removed (besides the core). <br>
A block can be removed by **right-clicking** on them.

<center>
<video autoplay loop width="500">
  <source src="../vids/remove.mp4" type="video/mp4">
</video>
</center>

!!! warning "Deleting A Parent"
    If you delete a block to which other blocks are attached as children, the whole branch will be removed

### Brushes

We have two different types of blocks we can build robots with: `Bricks` and `Hinges`, both can have a `Normal` orientation, or can be `Rotated` by 90 degrees.

Left-clicking on the control buttons on the bottom of the screen will either toggle `Normal` to `Rotated` (left button) or `Brick` to `Hinge` (right button).

These four options are colour coded, reflected by the colour of the button on the left:

- Brick, Normal: Orange
- Brick, Rotated: Light blue
- Hinge, Normal: Purple
- Hinge, Rotated: Turquoise


<center>
<img src="../imgs/brushes.jpg" width="650"/>
</center>

---

## Saving YAML

Once we have created a desirable model, we can save it by clicking "Save Yaml".

This will open a prompt, select the desired output directory, write the name of the output file in the text field.

Complete the operation, clicking the "Save" button, the new YAML file can now be found under the correct directory and name.

<center>
<img src="../imgs/cross.jpg" width="600"/>
</center>

!!! note "Save Name"
    Using both `[NAME]` and `[NAME].yaml` as file names in the text field will produce a file called `path/to/file/[NAME].yaml` <br>
    eg. `cross` or `cross.yaml` -> `path/to/file/cross.yaml`


### Clearning
Clicking the "Clear Canvas" button will remove the entire model and produce a clean canvas with only a `Core` at the centre (identical to when the app is initially opened).

---

## Loading YAML
Given a set of YAML files, we can open them into Devolve using the "Load YAML" button.
This will open a prompt, similar to saving, double-clicking on the desired file will load it into the canvas.

!!! note "Other Files"
    By default, "Load YAML" will only show files ending with `.yaml` as well as directories.

### Devolve vs Revolve
Here we see a comparison of a loaded model seen from the side, and the same model loaded in Revolve.

<center>
<img src="../imgs/228_dev_diag.jpg" width="500"/>
<img src="../imgs/228_rev.jpg" width="500"/>
</center>

### Devolve vs PNG Generator

Here we see a comparison of a loaded model seen from the top, with the equivalent revolve-generated PNG.
<center>
<img src="../imgs/228_dev_top.jpg" width="600"/>
<img src="../imgs/228_gen.jpg" width="500"/>
</center>

As can be noted from this example, the PNG is lacking essential detail (a hinge) in explaining the shape of the model, exemplifying the need for this program.

---
## Editing YAMLs
Editing existing YAML files is just as easy as combining the previous steps: <br> load a YAML file, make the required changes to a YAML file, and then save it.


Saving it in the same directory with the same name will raise a prompt for overwriting an existing file, which the user can accept or decline.

---

<center>
    Learning Devolve i **done**
</center>