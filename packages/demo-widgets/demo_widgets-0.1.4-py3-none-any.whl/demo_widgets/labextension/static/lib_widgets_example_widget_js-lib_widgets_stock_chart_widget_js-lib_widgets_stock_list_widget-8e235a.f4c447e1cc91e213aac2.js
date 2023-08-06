(self["webpackChunkdemo_widgets"] = self["webpackChunkdemo_widgets"] || []).push([["lib_widgets_example_widget_js-lib_widgets_stock_chart_widget_js-lib_widgets_stock_list_widget-8e235a"],{

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widgets/example_widget.js":
/*!***************************************!*\
  !*** ./lib/widgets/example_widget.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ExampleView = exports.ExampleModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ../version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../../css/example_widget.css */ "./css/example_widget.css");
class ExampleModel extends base_1.DOMWidgetModel {
    defaults() {
        console.log('client-side: printing from ExampleModel!!!');
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version, value: 'Hello World' });
    }
}
exports.ExampleModel = ExampleModel;
ExampleModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
ExampleModel.model_name = 'ExampleModel';
ExampleModel.model_module = version_1.MODULE_NAME;
ExampleModel.model_module_version = version_1.MODULE_VERSION;
ExampleModel.view_name = 'ExampleView'; // Set to null if no view
ExampleModel.view_module = version_1.MODULE_NAME; // Set to null if no view
ExampleModel.view_module_version = version_1.MODULE_VERSION;
class ExampleView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('example-widget');
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    }
    value_changed() {
        this.el.textContent = this.model.get('value');
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=example_widget.js.map

/***/ }),

/***/ "./lib/widgets/stock_chart_widget.js":
/*!*******************************************!*\
  !*** ./lib/widgets/stock_chart_widget.js ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.StockChartView = exports.StockChartModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const auto_1 = __importDefault(__webpack_require__(/*! chart.js/auto */ "./node_modules/chart.js/auto/auto.cjs"));
const version_1 = __webpack_require__(/*! ../version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../../css/stock_chart_widget.css */ "./css/stock_chart_widget.css");
class StockChartModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: StockChartModel.model_name, _model_module: StockChartModel.model_module, _model_module_version: StockChartModel.model_module_version, _view_name: StockChartModel.view_name, _view_module: StockChartModel.view_module, _view_module_version: StockChartModel.view_module_version, stock_symbol: 'AAPL', stock_data: [[], []], stock_days: 90 });
    }
}
exports.StockChartModel = StockChartModel;
StockChartModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
StockChartModel.model_name = 'StockChartModel';
StockChartModel.model_module = version_1.MODULE_NAME;
StockChartModel.model_module_version = version_1.MODULE_VERSION;
StockChartModel.view_name = 'StockChartView'; // Set to null if no view
StockChartModel.view_module = version_1.MODULE_NAME; // Set to null if no view
StockChartModel.view_module_version = version_1.MODULE_VERSION;
class StockChartView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('stock-chart-widget');
        this.model.on('change:stock_symbol', this._updateData, this);
        this.model.on('change:stock_days', this._updateData, this);
        this.model.on('change:stock_data', this._updateChart, this);
        this._updateChart();
        return this;
    }
    _updateData() {
        this.send({
            name: 'load-stock-data',
            stock_symbol: this.model.get('stock_symbol'),
            stock_days: this.model.get('stock_days'),
        });
    }
    // _updateData: () => void = () => {
    //   this.send({
    //     name: 'update-data',
    //     stock_symbol: this.model.get('stock_symbol')
    //   });
    // };
    _updateChart() {
        const [labels, prices] = this.model.get('stock_data');
        this.$el.empty();
        const chartCanvas = document.createElement('canvas');
        const context = chartCanvas.getContext('2d');
        if (context) {
            context.clearRect(0, 0, chartCanvas.width, chartCanvas.height);
        }
        if (labels.length === prices.length && labels.length > 0) {
            new auto_1.default(chartCanvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: `${this.model.get('stock_symbol')} Stock Closing Price`,
                            data: prices,
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1,
                        },
                    ],
                },
            });
        }
        this.$el.append(chartCanvas);
    }
}
exports.StockChartView = StockChartView;
//# sourceMappingURL=stock_chart_widget.js.map

/***/ }),

/***/ "./lib/widgets/stock_list_widget.js":
/*!******************************************!*\
  !*** ./lib/widgets/stock_list_widget.js ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.StockListView = exports.StockListModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const underscore_1 = __importDefault(__webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore"));
const jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "webpack/sharing/consume/default/jquery/jquery"));
const version_1 = __webpack_require__(/*! ../version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../../css/stock_list_widget.css */ "./css/stock_list_widget.css");
class StockListModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: StockListModel.model_name, _model_module: StockListModel.model_module, _model_module_version: StockListModel.model_module_version, _view_name: StockListModel.view_name, _view_module: StockListModel.view_module, _view_module_version: StockListModel.view_module_version, input_label: 'Stock Symbol', button_text: 'Add Stock', stock_symbol: '', stocks: [], selected_stock_symbol: '' });
    }
}
exports.StockListModel = StockListModel;
StockListModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
StockListModel.model_name = 'StockListModel';
StockListModel.model_module = version_1.MODULE_NAME;
StockListModel.model_module_version = version_1.MODULE_VERSION;
StockListModel.view_name = 'StockListView'; // Set to null if no view
StockListModel.view_module = version_1.MODULE_NAME; // Set to null if no view
StockListModel.view_module_version = version_1.MODULE_VERSION;
class StockListView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.template = underscore_1.default.template(`
    <header>
      <h1>Stock List</l1>
    </header>
    <form>
      <label>
        <%= input_label %>
        <input type="text" name="stock_symbol" value="<%= stock_symbol %>">
      </label>
      <button type="button" class="add-stock-button"><%= button_text %></button>
    </form>
    <div>
      <header>
        <h2>My Stocks</h2>
      </header>
      <ul class="stock_symbol_list">
      </ul>
    </div>
  `);
        this.stockListItemTemplate = underscore_1.default.template(`
    <li>
      <span><%= stock_symbol %>: <%= stock_price %></span>
      <button type="button" data-op-name="remove-stock" data-stock-symbol="<%= stock_symbol %>">X</button>
      <button type="button" data-op-name="view-stock-chart" data-stock-symbol="<%= stock_symbol %>">View Chart</button>
    </li>
  `);
        this.refreshStocksList = () => {
            const stocks = this.model.get('stocks');
            const stockSymbolList = this.$el.find('ul.stock_symbol_list');
            stockSymbolList.empty();
            stocks.forEach((stock) => {
                stockSymbolList.append(this.stockListItemTemplate(stock));
            });
        };
    }
    render() {
        this.el.classList.add('stock-list-widget');
        this.$el.html(this.template(this.model.attributes));
        this.refreshStocksList();
        this.$el.find('ul.stock_symbol_list')
            .on('click', 'button' /* css selector */, (evt) => {
            const opButton = jquery_1.default(evt.target);
            const opName = opButton.attr('data-op-name');
            const stockSymbol = opButton.attr('data-stock-symbol');
            console.log('opName', opName);
            switch (opName) {
                case 'remove-stock':
                    console.log('ran remove stock');
                    this.send({ name: 'remove-stock', stock_symbol: stockSymbol });
                    break;
                case 'view-stock-chart':
                    this.send({ name: 'select-stock', stock_symbol: stockSymbol });
                    break;
                default:
                    console.log('unknown op name');
                    break;
            }
        });
        // handle the button click
        this.$el.find('button.add-stock-button').on('click', () => {
            // retrieve the value from the input field
            const stockSymbolInput = this.$el.find('input[name=stock_symbol]');
            const stockSymbol = stockSymbolInput.val();
            stockSymbolInput.val('');
            stockSymbolInput.focus();
            // using the comm to send data to the other side
            this.send({ name: 'add-stock', stock_symbol: stockSymbol });
        });
        // populate the results
        this.model.on('change:stocks', this.refreshStocksList);
        setInterval(() => {
            this.send({ name: 'refresh-stocks' });
        }, 60000 /* 1 min, 60 secs */);
        return this;
    }
}
exports.StockListView = StockListView;
//# sourceMappingURL=stock_list_widget.js.map

/***/ }),

/***/ "./lib/widgets/stock_lookup_widget.js":
/*!********************************************!*\
  !*** ./lib/widgets/stock_lookup_widget.js ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.StockLookupView = exports.StockLookupModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const underscore_1 = __importDefault(__webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore"));
const version_1 = __webpack_require__(/*! ../version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../../css/stock_lookup_widget.css */ "./css/stock_lookup_widget.css");
class StockLookupModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: StockLookupModel.model_name, _model_module: StockLookupModel.model_module, _model_module_version: StockLookupModel.model_module_version, _view_name: StockLookupModel.view_name, _view_module: StockLookupModel.view_module, _view_module_version: StockLookupModel.view_module_version, input_label: 'Stock Symbol', button_text: 'Get Price', stock_symbol: '', stock_price: -1 });
    }
}
exports.StockLookupModel = StockLookupModel;
StockLookupModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
StockLookupModel.model_name = 'StockLookupModel';
StockLookupModel.model_module = version_1.MODULE_NAME;
StockLookupModel.model_module_version = version_1.MODULE_VERSION;
StockLookupModel.view_name = 'StockLookupView'; // Set to null if no view
StockLookupModel.view_module = version_1.MODULE_NAME; // Set to null if no view
StockLookupModel.view_module_version = version_1.MODULE_VERSION;
class StockLookupView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.template = underscore_1.default.template(`
    <form>
      <label>
        <%= input_label %>
        <input type="text" name="stock_symbol" value="<%= stock_symbol %>">
      </label>
      <button type="button" class="get-price-button"><%= button_text %></button>
    </form>
    <div class="results hide-results">
      <span class="results_symbol"><%= stock_symbol %></span>
      <span class="results_price"><%= stock_price %></span>
    </div>
  `);
    }
    render() {
        this.el.classList.add('stock-lookup-widget');
        this.$el.html(this.template(this.model.attributes));
        // handle the button click
        this.$el.find('button.get-price-button').on('click', () => {
            // retrieve the value from the input field
            this.model.set('stock_price', -1);
            const stockSymbol = this.$el.find('input[name=stock_symbol]').val();
            // using the comm to send data to the other side
            this.send({ name: 'stock-lookup', stock_symbol: stockSymbol });
        });
        // populate the results
        this.model.on('change:stock_symbol', () => {
            const stockSymbol = this.model.get('stock_symbol');
            this.$el.find('input[name=stock_symbol]').val(stockSymbol);
            this.$el.find('span.results_symbol').text(stockSymbol);
        });
        this.model.on('change:stock_price', () => {
            const stockPrice = Number(this.model.get('stock_price'));
            this.$el.find('span.results_price').text(stockPrice);
        });
        // show/hide the results
        this.model.on('change', () => {
            const stockSymbol = this.model.get('stock_symbol');
            const stockPrice = Number(this.model.get('stock_price'));
            console.log('stock price: ', stockPrice, typeof stockPrice);
            const resultsDiv = this.$el.find('div.results');
            if (stockSymbol.length === 0 || stockPrice < 0) {
                resultsDiv.addClass('hide-results');
            }
            else {
                resultsDiv.removeClass('hide-results');
            }
        });
        return this;
    }
}
exports.StockLookupView = StockLookupView;
//# sourceMappingURL=stock_lookup_widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/example_widget.css":
/*!**********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/example_widget.css ***!
  \**********************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".example-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/stock_chart_widget.css":
/*!**************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/stock_chart_widget.css ***!
  \**************************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".stock-chart-widget {\n  margin: 4px;\n  padding: 4px;\n  overflow: auto;\n}\n\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/stock_list_widget.css":
/*!*************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/stock_list_widget.css ***!
  \*************************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".stock-list-widget {\n  margin: 4px;\n  padding: 4px;\n  color:white;\n\n}\n\n.stock-list-widget .hide-results {\n  display: none;\n}\n\n.stock-list-widget .results_symbol {\n  font-weight: bold;\n}\n\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/stock_lookup_widget.css":
/*!***************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/stock_lookup_widget.css ***!
  \***************************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".stock-lookup-widget {\n  margin: 4px;\n  background-color: white;\n  padding: 0px 2px;\n  border: 1px solid black;\n  padding: 4px;\n}\n\n.stock-lookup-widget .hide-results {\n  display: none;\n}\n\n.stock-lookup-widget .results_symbol {\n  font-weight: bold;\n}\n\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/example_widget.css":
/*!********************************!*\
  !*** ./css/example_widget.css ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./example_widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/example_widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./css/stock_chart_widget.css":
/*!************************************!*\
  !*** ./css/stock_chart_widget.css ***!
  \************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./stock_chart_widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/stock_chart_widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./css/stock_list_widget.css":
/*!***********************************!*\
  !*** ./css/stock_list_widget.css ***!
  \***********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./stock_list_widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/stock_list_widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./css/stock_lookup_widget.css":
/*!*************************************!*\
  !*** ./css/stock_lookup_widget.css ***!
  \*************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./stock_lookup_widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/stock_lookup_widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"demo_widgets","version":"0.1.4","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/Training 4 Developers LLC/demo_widgets","bugs":{"url":"https://github.com/Training 4 Developers LLC/demo_widgets/issues"},"license":"BSD-3-Clause","author":{"name":"Eric","email":"eric@t4d.io"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/Training 4 Developers LLC/demo_widgets"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf demo_widgets/labextension","clean:nbextension":"rimraf demo_widgets/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","chart.js":"^4.2.0","jquery":"^3.6.3","underscore":"^1.13.6"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"demo_widgets/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widgets_example_widget_js-lib_widgets_stock_chart_widget_js-lib_widgets_stock_list_widget-8e235a.f4c447e1cc91e213aac2.js.map