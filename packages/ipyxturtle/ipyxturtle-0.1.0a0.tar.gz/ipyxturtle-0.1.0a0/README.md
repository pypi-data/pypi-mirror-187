# ipyxturtle - Turtle Widget for Jupyter Notebook

Widget adaptation to Jupyter Notebook environment of [turtle graphics](https://docs.python.org/3/library/turtle.html) library, that is inspired by Logo programming language, developed by Wally Feurzeig, Seymour Papert and Cynthia Solomon in 1967.

Simulating robotic commands to draw a figure into a clean surface, you can create Turtles to execute their commands, making them draw by according to the commands sent.

[GIF do exemplo de código em funcionamento]

# Install

```sh
$ pip install ipyxturtle
$ jupyter nbextension install --py ipyxturtle --user
$ jupyter nbextension enable --sys-prefix --py ipyxturtle
```

# Development install

```sh
$ python -m pip install -e .
$ jupyter nbextension install --py ipyxturtle --user
$ jupyter nbextension enable --sys-prefix --py ipyxturtle
```

To watch every change on javascript module, enter on `js/lib` and execute `yarn watch`.

# Commands

## Start

To start a ipyxturtle environment, first do you have to instantiate a Canvas.

```py
from ipyxturtle import Canvas

canvas = Canvas()
canvas
```

Drawing a Canvas inside a notebook cell response.

[GIF mostrando a execução desses comandos]

Then, you can create turtles to help you to create your own figures.

```py
turtle = canvas.create_turtle()
```

[GIF da turtle sendo criada]

You can create more than one turtle, just calling ```create_turtle()``` method again! After all, you can start to draw.

## Command list

### Canvas

| Command | Arguments | Description | Code example |
|:-------:|:-------:|:-----------:|:------------:|
| create_turtle() | | Returns a Turtle instance associated to the canvas | `turtle = canvas.create_turtle()` |

### Turtle

| Command | Arguments | Description | Code example |
|:-------:|:-------:|:-----------:|:------------:|
| forward(distance) | **distance**: Integer | Make the turtle draw the line forward in an amount of pixels relative to the distance parameter | turtle.forward(100) |
| backward(distance) | **distance**: Integer | Make the turtle draw the line backward in an amount of pixels relative to the distance parameter | turtle.backward(100) |
| right(angle) | **angle**: Integer | Adjusts the turtle's angle by moving the set amount to the right | turtle.right(90) |
| left(angle) | **angle**: Integer | Adjusts the turtle's angle by moving the set amount to the left | turtle.left(90) |
| color(color_hex) | **color_hex**: String | Change turtle color line | turtle.color('green') ou turtle.color('#008000') |
| circle(radius) | **radius**: Integer  | Creates a circle stamp with the specified radius | turtle.circle(100) |
| rectangle(width, height) | **width**: Integer, **height**: Integer | Creates a rectangle stamp with the specified width and height | turtle.rectangle(100, 200) |
| speed(value) | **value**: Float | Set Turtle draw speed | turtle.speed(1.5) |
| set_position(x, y) | **x**: Integer, **y**: Integer | Moves the turtle to the desired position | turtle.set_position(100, 100) |
