var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var SmilesDrawer = require('smiles-drawer');
var check = require('check-types');
var Color = require('color');

require('./smiles_drawer.css');

// See *.js.py for the kernel counterpart to this file.


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var SmilesDrawerModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name: 'SmilesDrawerModel',
        _view_name: 'SmilesDrawerView',
        _model_module: 'faerun-notebook',
        _view_module: 'faerun-notebook',
        _model_module_version: '0.1.6',
        _view_module_version: '0.1.6',
        value: '',
        theme: 'light',
        options: {},
        output: 'svg',
        border: true,
        background: "#ffffff",
    })
});


// Custom View. Renders the widget model.
var SmilesDrawerView = widgets.DOMWidgetView.extend({
    // Defines how the widget gets rendered into the DOM
    render: function () {
        this.redraw();
        this.model.on('change:value', this.redraw, this);
    },
    redraw() {
        var value = this.model.get('value');
        var weights = this.model.get('weights');
        var theme = this.model.get('theme');
        var options = this.model.get('options');
        var border = this.model.get('options');
        var background = Color(this.model.get('background'));

        if (!('scale' in options)) {
            options['scale'] = 1.25;
        }

        var append = function (value, weights, parent, output, options, border, title = '') {
            var smiDrawer = new SmilesDrawer.SmiDrawer(options);

            smiDrawer.draw(value, output, theme, svg => {
                var container = document.createElement('div');
                container.setAttribute('class', 'smiles-drawer-container');
                container.setAttribute('style', `background-color: ${background.hex()}`)
                if (border) {
                    container.classList.add('border');
                }

                if (title !== '') {
                    var titleElement = document.createElement('div');
                    titleElement.setAttribute('class', 'smiles-drawer-title');

                    var textColor = '#ffffff';
                    if (background.isLight()) {
                        textColor = '#000000';
                    }

                    titleElement.setAttribute('style', `color: ${textColor}`)
                    titleElement.textContent = title;
                    container.append(titleElement);
                }

                svg.setAttribute('class', 'smiles-drawer-element');
                container.appendChild(svg);
                parent.appendChild(container);
            }, e => {
                console.log(e);
            }, weights);
        }

        this.el.innerHTML = '';
        if (check.string(value)) {
            var w = null;
            if (weights.length > 0) {
                w = weights[0];
            }
            append(value, w, this.el, this.model.get('output'), options, false);
        } else if (check.array.of.array(value)) {
            for (var i = 0; i < value.length; i++) {
                var w = null;
                if (weights.length > i) {
                    w = weights[i];
                }
                if (value[i].length === 2) {
                    append(value[i][1], w, this.el, this.model.get('output'), options, border, value[i][0]);
                }
            }
        } else if (check.array(value)) {
            for (var i = 0; i < value.length; i++) {
                var w = null;
                if (weights.length > i) {
                    w = weights[i];
                }
                append(value[i], w, this.el, this.model.get('output'), options, border);
            }
        }
    }
});


module.exports = {
    SmilesDrawerModel: SmilesDrawerModel,
    SmilesDrawerView: SmilesDrawerView
};
