(self["webpackChunkdemo_widgets"] = self["webpackChunkdemo_widgets"] || []).push([["lib_widgets_example_widget_js-lib_widgets_stock_list_widget_js-lib_widgets_stock_lookup_widget_js"],{

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
const version_1 = __webpack_require__(/*! ../version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../../css/stock_list_widget.css */ "./css/stock_list_widget.css");
class StockListModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: StockListModel.model_name, _model_module: StockListModel.model_module, _model_module_version: StockListModel.model_module_version, _view_name: StockListModel.view_name, _view_module: StockListModel.view_module, _view_module_version: StockListModel.view_module_version, input_label: 'Stock Symbol', button_text: 'Add Stock', stock_symbol: '', stocks: [] });
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
      <button type="button">X</button>
    </li>
  `);
    }
    render() {
        this.el.classList.add('stock-list-widget');
        this.$el.html(this.template(this.model.attributes));
        this.$el.find('ul.stock_symbol_list');
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
        this.model.on('change:stocks', () => {
            const stocks = this.model.get('stocks');
            const stockSymbolList = this.$el.find('ul.stock_symbol_list');
            stockSymbolList.empty();
            stocks.forEach((stock) => {
                stockSymbolList.append(this.stockListItemTemplate(stock));
            });
        });
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

/***/ "./node_modules/css-loader/dist/cjs.js!./css/stock_list_widget.css":
/*!*************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/stock_list_widget.css ***!
  \*************************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".stock-list-widget {\n  margin: 4px;\n  background-color: white;\n  padding: 0px 2px;\n  border: 1px solid black;\n  padding: 4px;\n}\n\n.stock-list-widget .hide-results {\n  display: none;\n}\n\n.stock-list-widget .results_symbol {\n  font-weight: bold;\n}\n\n", ""]);
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

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

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

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"demo_widgets","version":"0.1.0","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/Training 4 Developers LLC/demo_widgets","bugs":{"url":"https://github.com/Training 4 Developers LLC/demo_widgets/issues"},"license":"BSD-3-Clause","author":{"name":"Eric","email":"eric@t4d.io"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/Training 4 Developers LLC/demo_widgets"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf demo_widgets/labextension","clean:nbextension":"rimraf demo_widgets/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","chart.js":"^4.2.0","underscore":"^1.13.6"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"demo_widgets/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widgets_example_widget_js-lib_widgets_stock_list_widget_js-lib_widgets_stock_lookup_widget_js.31a3367985d4eb1c82a8.js.map