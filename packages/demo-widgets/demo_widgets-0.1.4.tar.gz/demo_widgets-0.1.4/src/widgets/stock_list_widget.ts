// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import _ from 'underscore';
import $ from 'jquery';

import { MODULE_NAME, MODULE_VERSION } from '../version';

// Import the CSS
import '../../css/stock_list_widget.css';

export type StockListItem = {
  stock_symbol: string;
  stock_price: number;
};

export class StockListModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: StockListModel.model_name,
      _model_module: StockListModel.model_module,
      _model_module_version: StockListModel.model_module_version,
      _view_name: StockListModel.view_name,
      _view_module: StockListModel.view_module,
      _view_module_version: StockListModel.view_module_version,

      input_label: 'Stock Symbol',
      button_text: 'Add Stock',
      stock_symbol: '',
      stocks: [] as StockListItem[],
      selected_stock_symbol: '',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'StockListModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'StockListView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class StockListView extends DOMWidgetView {
  template = _.template(`
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

  stockListItemTemplate = _.template(`
    <li>
      <span><%= stock_symbol %>: <%= stock_price %></span>
      <button type="button" data-op-name="remove-stock" data-stock-symbol="<%= stock_symbol %>">X</button>
      <button type="button" data-op-name="view-stock-chart" data-stock-symbol="<%= stock_symbol %>">View Chart</button>
    </li>
  `);

  render(): StockListView {
    this.el.classList.add('stock-list-widget');

    this.$el.html(this.template(this.model.attributes));
    this.refreshStocksList();

    this.$el.find('ul.stock_symbol_list')
      .on('click', 'button' /* css selector */, (evt: any) => {
        const opButton = $(evt.target);

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
      const stockSymbolInput = this.$el.find('input[name=stock_symbol]')
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

  refreshStocksList = () => {
    const stocks = this.model.get('stocks') as StockListItem[];
    const stockSymbolList = this.$el.find('ul.stock_symbol_list');
    stockSymbolList.empty();
    stocks.forEach((stock) => {
      stockSymbolList.append(this.stockListItemTemplate(stock));
    });
  }
}
