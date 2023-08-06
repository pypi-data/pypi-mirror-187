// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import Chart from 'chart.js/auto';

import { MODULE_NAME, MODULE_VERSION } from '../version';

// Import the CSS
import '../../css/stock_chart_widget.css';

export type StockData = [string[], number[]];

export class StockChartModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: StockChartModel.model_name,
      _model_module: StockChartModel.model_module,
      _model_module_version: StockChartModel.model_module_version,
      _view_name: StockChartModel.view_name,
      _view_module: StockChartModel.view_module,
      _view_module_version: StockChartModel.view_module_version,

      stock_symbol: 'AAPL',
      stock_data: [[], []] as StockData,
      stock_days: 90,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'StockChartModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'StockChartView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class StockChartView extends DOMWidgetView {
  render(): StockChartView {
    this.el.classList.add('stock-chart-widget');

    this.model.on('change:stock_symbol', this._updateData, this);
    this.model.on('change:stock_days', this._updateData, this);
    this.model.on('change:stock_data', this._updateChart, this);

    this._updateChart();

    return this;
  }

  _updateData(): void {
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

  _updateChart(): void {
    const [labels, prices] = this.model.get('stock_data') as StockData;

    this.$el.empty();

    const chartCanvas = document.createElement('canvas');

    const context = chartCanvas.getContext('2d');
    if (context) {
      context.clearRect(0, 0, chartCanvas.width, chartCanvas.height);
    }

    if (labels.length === prices.length && labels.length > 0) {
      new Chart(chartCanvas, {
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
