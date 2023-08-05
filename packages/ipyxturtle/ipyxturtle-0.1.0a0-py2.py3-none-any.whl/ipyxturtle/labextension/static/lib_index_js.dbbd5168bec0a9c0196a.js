(self["webpackChunkipyxturtle"] = self["webpackChunkipyxturtle"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

// Export widget models and views, and the npm package version number.
module.exports = __webpack_require__(/*! ./ipyxturtle.js */ "./lib/ipyxturtle.js");
module.exports.version = __webpack_require__(/*! ../package.json */ "./package.json").version;


/***/ }),

/***/ "./lib/ipyxturtle.js":
/*!***************************!*\
  !*** ./lib/ipyxturtle.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CanvasModel": () => (/* binding */ CanvasModel),
/* harmony export */   "CanvasView": () => (/* binding */ CanvasView)
/* harmony export */ });
/* harmony import */ var xturtle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! xturtle */ "webpack/sharing/consume/default/xturtle/xturtle");
/* harmony import */ var xturtle__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(xturtle__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__);



class CanvasModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: 'CanvasModel',
            _view_name: 'CanvasView',
            _model_module: 'ipyxturtle',
            _view_module: 'ipyxturtle',
            _model_module_version: '0.1.0',
            _view_module_version: '0.1.0'
        }
    }
}

class CanvasView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetView {
    render() {
        this.turtles = {};
        this.create_canvas();

        this.model.on('change:command', this.execute, this);
        this.model.on('change:last_turtle', this.create_turtle, this);
    }

    create_turtle() {
        const turtle = this.model.get('last_turtle');

        if (Number.isInteger(turtle.id)) {
            this.turtles[turtle.id] = this.canvas.createTurtle();
        }
    }

    create_canvas() {
        const backgroundCanvas = document.createElement('canvas');
        this.canvas = new xturtle__WEBPACK_IMPORTED_MODULE_0__.TurtleComponent();

        this.canvas.width = this.model.get('width');
        this.canvas.height = this.model.get('height');

        backgroundCanvas.id = 'bgCanvas';
        backgroundCanvas.setAttribute('width', this.canvas.width);
        backgroundCanvas.setAttribute('height', this.canvas.height);

        this.canvas.canvasStyle = this.model.get('canvas_style');
        this.canvas.spriteScale = this.model.get('sprite_scale');
        this.canvas.initializeCanvas(this.el);

        this.el.appendChild(backgroundCanvas);

        this.el.style.cssText = `
            width: ${this.canvas.width};
            height: ${this.canvas.height};
            z-index: 999;
            background-color: white;
            position: fixed;
            border-color: grey;
            border-width: 1px;
            border: 1px solid grey;
            right: 0;
            bottom: 0;
        `
        document.body.prepend(this.el);

        this.set_canvas();
    }

    set_canvas() {
        this.model.set('canvas', { 'element': this.canvas });
        this.model.save_changes();
    }

    set_turtle() {
        this.model.set('turtle', { 'element': this.turtle });
        this.model.save_changes();
    }

    get_canvas() {
        let canvas = this.model.get('canvas');

        if (canvas) return canvas.element;
    }

    get_turtle() {
        let turtle = this.model.get('turtle');

        if (turtle) return turtle.element;
    }

    execute() {
        this.command = this.model.get('command');

        if (this.command.function_name) {
            this.run();
            this.command = {};
        }
    }

    run() {
        let turtle_id = this.command.turtle_id;
        let turtle = this.turtles[turtle_id];

        if (turtle) turtle[this.command['function_name']](...this.command['args']);
    }
}


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipyxturtle","version":"0.1.0","description":"A Jupyter Widget Library to simulate Logo language in python environment","author":"Guilherme Silva","main":"lib/index.js","repository":{"type":"git","url":"https://github.com/x-turtle/ipyxturtle.git"},"keywords":["jupyter","widgets","ipython","ipywidgets","jupyterlab-extension"],"files":["lib/**/*.js","dist/*.js"],"scripts":{"clean":"rimraf dist/ && rimraf ../ipyxturtle/labextension/ && rimraf ../ipyxturtle/nbextension","prepublish":"yarn run clean && yarn run build:prod","build":"webpack --mode=development && yarn run build:labextension:dev","build:prod":"webpack --mode=production && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","watch":"webpack --watch --mode=development","test":"echo \\"Error: no test specified\\" && exit 1"},"devDependencies":{"@jupyterlab/builder":"^3.0.0","rimraf":"^2.6.1","webpack":"^5"},"dependencies":{"@jupyter-widgets/base":"^1.1 || ^2 || ^3 || ^4","lodash":"^4.17.4","xturtle":"1.0.0"},"jupyterlab":{"extension":"lib/labplugin","outputDir":"../ipyxturtle/labextension","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.dbbd5168bec0a9c0196a.js.map