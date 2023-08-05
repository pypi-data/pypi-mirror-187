# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


# This file was changed by Artem Shumeiko
from flask_babel import gettext as __

# superset-frontend/src/profile/components/Favorites.tsx
slice = __("slice")
creator = __("creator")
favorited = __("favorited")
created = __("created")

# superset-frontend/src/profile/components/RecentActivity.tsx
name = __("name")
type_ = __("type")
time = __("time")

# superset-frontend/src/SqlLab/components/QueryHistory/index.tsx
state = __('state')
started = __('started')
duration = __('duration')
progress = __('progress')
rows = __('rows')
sql = __('sql')
results = __('results')
actions = __('actions')

# superset-frontend/src/dashboard/components/SliceAdder.jsx
chart_names = {
  'line': __('line'),
  'big_number': __('big_number'),
  'big_number_total': __('big_number_total'),
  'table': __('table'),
  'table_xml': __('table_xml'),
  'pivot_table_v2': __('pivot_table_v2'),
  'echarts_timeseries_line': __('echarts_timeseries_line'),
  'echarts_area': __('echarts_area'),
  'echarts_timeseries_bar': __('echarts_timeseries_bar'),
  'echarts_timeseries_scatter': __('echarts_timeseries_scatter'),
  'pie': __('pie'),
  'mixed_timeseries': __('mixed_timeseries'),
  'filter_box': __('filter_box'),
  'dist_bar': __('dist_bar'),
  'area': __('area'),
  'bar': __('bar'),
  'deck_polygon': __('deck_polygon'),
  'time_table': __('time_table'),
  'histogram': __('histogram'),
  'deck_scatter': __('deck_scatter'),
  'deck_hex': __('deck_hex'),
  'time_pivot': __('time_pivot'),
  'deck_arc': __('deck_arc'),
  'heatmap': __('heatmap'),
  'deck_grid': __('deck_grid'),
  'dual_line': __('dual_line'),
  'deck_screengrid': __('deck_screengrid'),
  'line_multi': __('line_multi'),
  'treemap': __('treemap'),
  'box_plot': __('box_plot'),
  'sunburst': __('sunburst'),
  'sankey': __('sankey'),
  'word_cloud': __('word_cloud'),
  'mapbox': __('mapbox'),
  'kepler': __('kepler'),
  'cal_heatmap': __('cal_heatmap'),
  'rose': __('rose'),
  'bubble': __('bubble'),
  'deck_geojson': __('deck_geojson'),
  'horizon': __('horizon'),
  'deck_multi': __('deck_multi'),
  'compare': __('compare'),
  'partition': __('partition'),
  'event_flow': __('event_flow'),
  'deck_path': __('deck_path'),
  'graph_chart': __('graph_chart'),
  'world_map': __('world_map'),
  'paired_ttest': __('paired_ttest'),
  'para': __('para'),
  'country_map': __('country_map'),
  # added manually :/
  'gauge_chart': __('gauge_chart'),
  'treemap_v2': __('treemap_v2'),
  'bullet': __('bullet'),
}

# superset-frontend/src/explore/components/controls/DateFilterControl/DateFilterLabel.tsx
TIME_RANGES_MAP = {
  'Last day': __('Last day'),
  'Last week': __('Last week'),
  'Last month': __('Last month'),
  'Last quarter': __('Last quarter'),
  'Last year': __('Last year'),
}

# alert modal
asdasd = {
  'Alert': __('Alert'),
  'Report': __('Report'),
}

# superset-frontend/src/SqlLab/constants.ts
STATUS_OPTIONS = {
  'success': __('success'),
  'failed': __('failed'),
  'running': __('running'),
  'offline': __('offline'),
  'pending': __('pending'),
}

TIME_OPTIONS = {
  'now': __('now'),
  '1 hour ago': __('1 hour ago'),
  '1 day ago': __('1 day ago'),
  '7 days ago': __('7 days ago'),
  '28 days ago': __('28 days ago'),
  '90 days ago': __('90 days ago'),
  '1 year ago': __('1 year ago'),
}

# superset-frontend/packages/superset-ui-core/src/query/types/Query.ts
QueryState = {
  'stopped': __('stopped'),
  'failed': __('failed'),
  'pending': __('pending'),
  'running': __('running'),
  'scheduled': __('scheduled'),
  'success': __('success'),
  'fetching': __('fetching'),
  'timed_out': __('timed_out'),
}
