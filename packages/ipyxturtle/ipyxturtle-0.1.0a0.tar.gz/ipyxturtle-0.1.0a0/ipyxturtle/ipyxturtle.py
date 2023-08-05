import ipywidgets as widgets
from traitlets import Unicode, Dict, Integer, Float, observe

@widgets.register
class Turtle(widgets.DOMWidget):
    canvas = Dict({ 'instance': None }).tag(sync=True)

    def __init__(self, id, canvas):
        self._model_id = id
        self.canvas = canvas

    def forward(self, distance):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'forward',
            'args': [distance]
        }

    def backward(self, distance):
        self.forward(distance*-1)

    def right(self, angle):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'right',
            'args': [angle]
        }

    def left(self, angle):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'left',
            'args': [angle]
        }

    def color(self, color):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'setLineColor',
            'args': [color]
        }

    def circle(self, radius):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'circle',
            'args': [radius]
        }

    def rectangle(self, width, height):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'rectangle',
            'args': [width, height]
        }

    def speed(self, value):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'speed',
            'args': [value]
        }

    def set_position(self, x, y):
        self.canvas['instance'].command = {
            'turtle_id': self._model_id,
            'function_name': 'setPosition',
            'args': [x, y]
        }

@widgets.register
class Canvas(widgets.DOMWidget):
    _view_name = Unicode('CanvasView').tag(sync=True)
    _model_name = Unicode('CanvasModel').tag(sync=True)
    _view_module = Unicode('ipyxturtle').tag(sync=True)
    _model_module = Unicode('ipyxturtle').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    _auto_increment_counter = Integer(0).tag(sync=True)

    width = Integer(400).tag(sync=True)
    height = Integer(400).tag(sync=True)
    canvas_style = Unicode('border: solid 1px black; position: absolute !important;').tag(sync=True)
    sprite_scale = Float(1.0).tag(sync=True)

    command = Dict({}).tag(sync=True)
    last_turtle = Dict({}).tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__()
        self.width = kwargs.get('width', self.width)
        self.height = kwargs.get('height', self.height)
        self.canvas_style = kwargs.get('canvas_style', self.canvas_style)
        self.sprite_scale = kwargs.get('sprite_scale', self.sprite_scale)

    def create_turtle(self):
        turtle = Turtle(self._auto_increment_counter, { 'instance': self })
        self.last_turtle = { 'id': turtle._model_id }
        self._auto_increment_counter += 1

        return turtle

    @observe('command')
    def reset_command(self, event):
        self.command = {}

    @observe('last_turtle')
    def build_turtles(self, event):
        self.last_turtle = {}