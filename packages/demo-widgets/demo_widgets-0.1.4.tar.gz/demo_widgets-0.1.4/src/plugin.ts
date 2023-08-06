// Copyright (c) Eric
// Distributed under the terms of the Modified BSD License.

import { Application, IPlugin } from '@lumino/application';

import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import * as exampleWidgetExports from './widgets/example_widget';
import * as stockLookupWidgetExports from './widgets/stock_lookup_widget';
import * as stockListWidgetExports from './widgets/stock_list_widget';
import * as stockChartWidgetExports from './widgets/stock_chart_widget';

import { MODULE_NAME, MODULE_VERSION } from './version';

const EXTENSION_ID = 'demo_widgets:plugin';

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true,
} as unknown as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.

export default examplePlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry
): void {
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: {
      ...exampleWidgetExports,
      ...stockLookupWidgetExports,
      ...stockListWidgetExports,
      ...stockChartWidgetExports,
    },
  });
}
