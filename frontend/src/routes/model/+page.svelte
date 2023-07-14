<script>
    // import table_of_contents from '$lib/toc2.js';
    // import MathJax from 'mathjax';
    // import {onMount} from 'svelte';
    //
    // MathJax.config({
    //     tex: {
    //         inlineMath: [['$', '$'], ["\\(", "\\)"]],
    //         displayMath: [['$$', '$$'], ["\\[", "\\]"]],
    //         processEscapes: true,
    //         processEnvironments: true
    //     },
    //     displayAlign: 'center',
    //     'HTML-CSS': {
    //         styles: {'.MathJax_Display': {'margin': 0}},
    //         linebreaks: {automatic: true}
    //     }
    // });
    //
    // let cfg = {};
    // onMount(() => {
    //     table_of_contents(cfg);
    //
    //     // Insert the PlotlyConfig and Plotly code here
    //     window.PlotlyConfig = {MathJaxConfig: 'local'};
    //     if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {
    //         window.MathJax.Hub.Config({SVG: {font: "STIX-Web"}});
    //     }
    //     if (typeof require !== 'undefined') {
    //         require.undef("plotly");
    //         requirejs.config({
    //             paths: {
    //                 'plotly': ['https://cdn.plot.ly/plotly-2.20.0.min']
    //             }
    //         });
    //         require(['plotly'], function (Plotly) {
    //             window._Plotly = Plotly;
    //         });
    //     }
    // });
</script>

<html lang="en">
<head>
    <meta charset="utf-8"/>

    <title>Singapore Weather Prediction</title>

</head>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.css">

<link rel="stylesheet" type="text/css"
      href="https://rawgit.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/main.css">

<link rel="stylesheet" type="text/css"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<body>
<div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container" style="margin-left: 308px; width: 1096px;">

        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h1 id="Singapore-Weather-Prediction" data-toc-modified-id="Singapore-Weather-Prediction-1"><a class="toc-mod-link" id="Singapore-Weather-Prediction-1"></a><span class="toc-item-num">1&nbsp;&nbsp;</span>Singapore Weather Prediction<a class="anchor-link" href="#Singapore-Weather-Prediction">¶</a></h1>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[1]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># setup</span>
<span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="k">as</span> <span class="nn">plt</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">plotly.express</span> <span class="k">as</span> <span class="nn">px</span>
<span class="kn">import</span> <span class="nn">plotly.graph_objects</span> <span class="k">as</span> <span class="nn">go</span>
<span class="kn">import</span> <span class="nn">plotly.io</span> <span class="k">as</span> <span class="nn">pio</span>
<span class="kn">import</span> <span class="nn">plotly.offline</span> <span class="k">as</span> <span class="nn">pyo</span>
<span class="kn">import</span> <span class="nn">requests</span>
<span class="kn">import</span> <span class="nn">tensorflow</span> <span class="k">as</span> <span class="nn">tf</span>
<span class="kn">import</span> <span class="nn">os</span>

<span class="kn">from</span> <span class="nn">datetime</span> <span class="kn">import</span> <span class="n">datetime</span><span class="p">,</span> <span class="n">timedelta</span>
<span class="kn">from</span> <span class="nn">keras.layers</span> <span class="kn">import</span> <span class="n">Dense</span>
<span class="kn">from</span> <span class="nn">keras.layers</span> <span class="kn">import</span> <span class="n">Dropout</span>
<span class="kn">from</span> <span class="nn">keras.layers</span> <span class="kn">import</span> <span class="n">LSTM</span>
<span class="kn">from</span> <span class="nn">keras.models</span> <span class="kn">import</span> <span class="n">Sequential</span>
<span class="kn">from</span> <span class="nn">keras.preprocessing.sequence</span> <span class="kn">import</span> <span class="n">TimeseriesGenerator</span>
<span class="kn">from</span> <span class="nn">pmdarima</span> <span class="kn">import</span> <span class="n">auto_arima</span>
<span class="kn">from</span> <span class="nn">sklearn</span> <span class="kn">import</span> <span class="n">preprocessing</span>
<span class="kn">from</span> <span class="nn">sklearn.metrics</span> <span class="kn">import</span> <span class="n">mean_absolute_error</span><span class="p">,</span> <span class="n">mean_squared_error</span>
<span class="kn">from</span> <span class="nn">sklearn.preprocessing</span> <span class="kn">import</span> <span class="n">MinMaxScaler</span>
<span class="kn">from</span> <span class="nn">statsmodels.graphics.tsaplots</span> <span class="kn">import</span> <span class="n">plot_acf</span><span class="p">,</span> <span class="n">plot_pacf</span>
<span class="kn">from</span> <span class="nn">statsmodels.tsa.arima.model</span> <span class="kn">import</span> <span class="n">ARIMA</span>
<span class="kn">from</span> <span class="nn">statsmodels.tsa.seasonal</span> <span class="kn">import</span> <span class="n">seasonal_decompose</span>
<span class="kn">from</span> <span class="nn">statsmodels.tsa.stattools</span> <span class="kn">import</span> <span class="n">adfuller</span>
<span class="kn">from</span> <span class="nn">statsmodels.tsa.statespace.sarimax</span> <span class="kn">import</span> <span class="n">SARIMAX</span>
<span class="kn">from</span> <span class="nn">statsmodels.tsa.statespace.varmax</span> <span class="kn">import</span> <span class="n">VARMAX</span>
<span class="kn">from</span> <span class="nn">time</span> <span class="kn">import</span> <span class="n">time</span>

<span class="n">px</span><span class="o">.</span><span class="n">defaults</span><span class="o">.</span><span class="n">template</span> <span class="o">=</span> <span class="s1">'plotly'</span> <span class="c1"># plotly, plotly_dark</span>
<span class="n">pyo</span><span class="o">.</span><span class="n">init_notebook_mode</span><span class="p">(</span><span class="n">connected</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">pio</span><span class="o">.</span><span class="n">renderers</span><span class="o">.</span><span class="n">default</span> <span class="o">=</span> <span class="s2">"iframe"</span> <span class="c1"># must trust notebook for it to work, use iframe for lab</span>

<span class="c1"># Set the seed for numpy module</span>
<span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">seed</span><span class="p">(</span><span class="mi">123</span><span class="p">)</span>

<span class="c1"># Set the seed for tensorflow module</span>
<span class="n">tf</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">set_seed</span><span class="p">(</span><span class="mi">123</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <script type="text/javascript">
                                window.PlotlyConfig = {MathJaxConfig: 'local'};
                                if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {window.MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}
                                if (typeof require !== 'undefined') {
                                    require.undef("plotly");
                                    requirejs.config({
                                        paths: {
                                            'plotly': ['https://cdn.plot.ly/plotly-2.20.0.min']
                                        }
                                    });
                                    require(['plotly'], function(Plotly) {
                                        window._Plotly = Plotly;
                                    });
                                }
                            </script>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="Data-Acquisition" data-toc-modified-id="Data-Acquisition-1.0.1"><a class="toc-mod-link" id="Data-Acquisition-1.0.1"></a><span class="toc-item-num">1.0.1&nbsp;&nbsp;</span>Data Acquisition<a class="anchor-link" href="#Data-Acquisition">¶</a></h3><p>Data source: <a href="https://data.gov.sg/">data.gov.sg</a> - National Environment Agency</p>
                <p>Data format: CKAN APIs</p>
                <ul>
                    <li>access to static tabular data such as time series or listings</li>
                    <li>alternative to the data.gov.sg web interface</li>
                    <li>provides both RESTful and functional interfaces, all in JSON format, making it suitable for a wide range of clients.</li>
                </ul>
                <p>API used: CKAN Datastore Search</p>
                <ul>
                    <li>GET URL with endpoint: <a href="https://data.gov.sg/api/action/datastore_search">https://data.gov.sg/api/action/datastore_search</a></li>
                </ul>
                <table>
                    <thead><tr>
                        <th style="text-align:left">Name</th>
                        <th style="text-align:left">Description</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td style="text-align:left"><strong>resource_id *</strong></td>
                        <td style="text-align:left">ID or alias of the resource to be searched against</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">limit</td>
                        <td style="text-align:left">Maximum number of rows to return (optional, default: 100)<br><em>Default value</em>: 100</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">offset</td>
                        <td style="text-align:left">Offset this number of rows (optional)</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">fields</td>
                        <td style="text-align:left">Fields to return (optional, default: all fields in original order)</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">filters</td>
                        <td style="text-align:left">Dictionary of matching conditions, e.g., &#123"key1": "a", "key2": "b"} (optional)</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">q</td>
                        <td style="text-align:left">Full text query. If it’s a string, it’ll search on all fields on each row.<br>If it’s a dictionary as &#123"key1": "a", "key2": "b"}, it’ll search on each specific field (optional)</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">sort</td>
                        <td style="text-align:left">Comma-separated field names with ordering, e.g.: "fieldname1, fieldname2 desc" (optional)</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">records_format</td>
                        <td style="text-align:left">The format for the records return value:<br>'objects' (default) list of &#123fieldname1: value1, ...} dicts,<br>'lists' list of [value1, value2, ...] lists,<br>'csv' string containing comma-separated values with no header,<br>'tsv' string containing tab-separated values with no header<br><em>Available values</em>: objects, lists, csv<br><em>Default value</em>: objects</td>
                    </tr>
                    </tbody>
                </table>
                <p><em>Note: wanted to predict on different variables at first but decided to narrow my scope to just <strong>temperature</strong>.</em></p>
                <table>
                    <thead><tr>
                        <th style="text-align:left">Variable</th>
                        <th style="text-align:left">Columns (renamed)</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td style="text-align:left">Surface Air Temperature - Monthly Mean (°C)</td>
                        <td style="text-align:left">month, mean_temp</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Surface Air Temperature - Monthly Absolute Extreme Maximum (°C)</td>
                        <td style="text-align:left">month, max_temp</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Surface Air Temperature - Monthly Absolute Extreme Minimum (°C)</td>
                        <td style="text-align:left">month, min_temp</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Rainfall - Monthly Total (mm)</td>
                        <td style="text-align:left">month, total_rainfall</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Rainfall - Monthly Maximum Daily Total  (mm)</td>
                        <td style="text-align:left">month, max_rainfall_daily</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Rainfall - Monthly Number of Rain Days (d)</td>
                        <td style="text-align:left">month, num_rainy_days</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Relative Humidity - Monthly Mean (%)</td>
                        <td style="text-align:left">month, mean_rh</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Relative Humidity - Monthly Absolute Extreme Minimum (%)</td>
                        <td style="text-align:left">month, min_rh</td>
                    </tr>
                    <tr>
                        <td style="text-align:left">Sunshine Duration - Monthly Mean Daily Duration (h)</td>
                        <td style="text-align:left">month, mean_sunshine_hrs_daily</td>
                    </tr>
                    </tbody>
                </table>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[2]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">api_endpoint</span> <span class="o">=</span> <span class="s2">"https://data.gov.sg/api/action/datastore_search"</span>

<span class="c1"># resource ids</span>
<span class="n">surface_air_temp_monthly_mean_resource_id</span> <span class="o">=</span> <span class="s2">"07654ce7-f97f-49c9-81c6-bd41beba4e96"</span>
<span class="c1"># surface_air_temp_monthly_abs_extreme_max_resource_id = "96e66346-68bb-4ca9-b001-58bbf39e36a7"</span>
<span class="c1"># surface_air_temp_monthly_abs_extreme_min_resource_id = "0c5b9752-2488-46cc-ae1c-42318d0f8865"</span>
<span class="n">rainfall_monthly_total_resource_id</span> <span class="o">=</span> <span class="s2">"778814b8-1b96-404b-9ac9-68d6c00e637b"</span>
<span class="c1"># rainfall_monthly_max_daily_total_resource_id = "df4d391e-6950-4fc6-80cd-c9b9ef6354fe"</span>
<span class="c1"># rainfall_monthly_num_rain_days_resource_id = "8b94f596-91fd-4545-bf9e-7a426493b674"</span>
<span class="c1"># relative_humidity_monthly_mean_resource_id = "4631174f-9858-463d-8a88-f3cb21588c67"</span>
<span class="c1"># relative_humidity_monthly_abs_extreme_min_resource_id = "585c24a5-76cd-4c48-9341-9223de5adc1d"</span>
<span class="c1"># sunshine_duration_monthly_mean_daily_resource_id = "0230819f-1c83-4980-b738-56136d6dc300"</span>

<span class="n">resource_ids</span> <span class="o">=</span> <span class="p">[</span><span class="n">surface_air_temp_monthly_mean_resource_id</span><span class="p">,</span> <span class="n">rainfall_monthly_total_resource_id</span><span class="p">]</span>

<span class="c1"># resource_ids = [surface_air_temp_monthly_mean_resource_id,</span>
<span class="c1"># surface_air_temp_monthly_abs_extreme_max_resource_id,</span>
<span class="c1"># surface_air_temp_monthly_abs_extreme_min_resource_id,</span>
<span class="c1"># rainfall_monthly_total_resource_id,</span>
<span class="c1"># rainfall_monthly_max_daily_total_resource_id,</span>
<span class="c1"># rainfall_monthly_num_rain_days_resource_id,</span>
<span class="c1"># relative_humidity_monthly_mean_resource_id,</span>
<span class="c1"># relative_humidity_monthly_abs_extreme_min_resource_id,</span>
<span class="c1"># sunshine_duration_monthly_mean_daily_resource_id]</span>

<span class="c1"># call APIs</span>
<span class="n">merged_df</span> <span class="o">=</span> <span class="kc">None</span>
<span class="k">for</span> <span class="n">resource_id</span> <span class="ow">in</span> <span class="n">resource_ids</span><span class="p">:</span>
    <span class="n">url</span> <span class="o">=</span> <span class="n">api_endpoint</span> <span class="o">+</span> <span class="s2">"?resource_id="</span> <span class="o">+</span> <span class="n">resource_id</span> <span class="o">+</span> <span class="s2">"&amp;limit=1000"</span>
    <span class="n">response</span> <span class="o">=</span> <span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">url</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()</span>
    <span class="n">data</span> <span class="o">=</span> <span class="n">response</span><span class="p">[</span><span class="s1">'result'</span><span class="p">][</span><span class="s1">'records'</span><span class="p">]</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">data</span><span class="p">)</span><span class="o">.</span><span class="n">set_index</span><span class="p">(</span><span class="s1">'month'</span><span class="p">)</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="s1">'_id'</span><span class="p">,</span> <span class="n">axis</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">merged_df</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
        <span class="nb">print</span><span class="p">(</span><span class="s2">"Acquiring data..."</span><span class="p">)</span>
        <span class="n">merged_df</span> <span class="o">=</span> <span class="n">df</span>
        <span class="k">continue</span>
    <span class="n">merged_df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">merged_df</span><span class="p">,</span> <span class="n">df</span><span class="p">,</span> <span class="n">on</span><span class="o">=</span><span class="s1">'month'</span><span class="p">)</span>

<span class="c1"># data until April 2023 when this was executed</span>
<span class="n">merged_df</span> <span class="o">=</span> <span class="n">merged_df</span><span class="p">[:</span><span class="mi">496</span><span class="p">]</span>
<span class="nb">print</span><span class="p">(</span><span class="n">merged_df</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Acquiring data...
        mean_temp total_rainfall
month
1982-01      25.9          107.1
1982-02      27.1           27.8
1982-03      27.2          160.8
1982-04        27            157
1982-05        28          102.2
...           ...            ...
2022-12      26.8          215.4
2023-01      26.5          302.6
2023-02      26.9          324.4
2023-03      27.1          243.4
2023-04      28.5          222.8

[496 rows x 2 columns]
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="Data-Preprocessing" data-toc-modified-id="Data-Preprocessing-1.0.2"><a class="toc-mod-link" id="Data-Preprocessing-1.0.2"></a><span class="toc-item-num">1.0.2&nbsp;&nbsp;</span>Data Preprocessing<a class="anchor-link" href="#Data-Preprocessing">¶</a></h3><p>Rename columns, convert data types, handle missing values, data cleaning, ensuring data is in suitable format for modeling.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[3]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># rename columns</span>
<span class="n">new_names</span> <span class="o">=</span> <span class="p">&#123</span><span class="s1">'max_temperature'</span><span class="p">:</span> <span class="s1">'max_temp'</span><span class="p">,</span> <span class="s1">'temp_extremes_min'</span><span class="p">:</span> <span class="s1">'min_temp'</span><span class="p">,</span> <span class="s1">'maximum_rainfall_in_a_day'</span><span class="p">:</span> <span class="s1">'max_rainfall_daily'</span><span class="p">,</span> <span class="s1">'no_of_rainy_days'</span><span class="p">:</span> <span class="s1">'num_rainy_days'</span><span class="p">,</span> <span class="s1">'rh_extremes_minimum'</span><span class="p">:</span> <span class="s1">'min_rh'</span><span class="p">,</span> <span class="s1">'mean_sunshine_hrs'</span><span class="p">:</span> <span class="s1">'mean_sunshine_hrs_daily'</span><span class="p">}</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">merged_df</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="n">new_names</span><span class="p">)</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">rename_axis</span><span class="p">(</span><span class="s1">'datetime'</span><span class="p">)</span>
<span class="n">df</span><span class="o">.</span><span class="n">index</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">to_datetime</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">index</span><span class="p">)</span>
<span class="c1"># df['year'] = df.index.year.astype('int64')</span>
<span class="c1"># df['month'] = df.index.month.astype('int64')</span>
<span class="k">for</span> <span class="n">column</span> <span class="ow">in</span> <span class="n">df</span><span class="o">.</span><span class="n">columns</span><span class="p">:</span>
    <span class="n">df</span><span class="p">[</span><span class="n">column</span><span class="p">]</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">to_numeric</span><span class="p">(</span><span class="n">df</span><span class="p">[</span><span class="n">column</span><span class="p">],</span> <span class="n">errors</span><span class="o">=</span><span class="s1">'raise'</span><span class="p">)</span>
<span class="c1"># start_datetime = pd.to_datetime('2010-01-01')</span>
<span class="c1"># df = df[start_datetime:]</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
<span class="c1"># df.head()</span>
<span class="c1"># print(df.dtypes)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>            mean_temp  total_rainfall
datetime
1982-01-01       25.9           107.1
1982-02-01       27.1            27.8
1982-03-01       27.2           160.8
1982-04-01       27.0           157.0
1982-05-01       28.0           102.2
...               ...             ...
2022-12-01       26.8           215.4
2023-01-01       26.5           302.6
2023-02-01       26.9           324.4
2023-03-01       27.1           243.4
2023-04-01       28.5           222.8

[496 rows x 2 columns]
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="Data-Visualisation" data-toc-modified-id="Data-Visualisation-1.0.3"><a class="toc-mod-link" id="Data-Visualisation-1.0.3"></a><span class="toc-item-num">1.0.3&nbsp;&nbsp;</span>Data Visualisation<a class="anchor-link" href="#Data-Visualisation">¶</a></h3>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[4]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">series_monthly_mean_temp</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="s1">'mean_temp'</span><span class="p">]</span><span class="o">.</span><span class="n">resample</span><span class="p">(</span><span class="s1">'M'</span><span class="p">)</span><span class="o">.</span><span class="n">mean</span><span class="p">()</span>  <span class="c1"># resample to monthly mean</span>
<span class="c1"># print(series_monthly_mean_temp)</span>

<span class="c1"># line plot for mean temperature</span>
<span class="n">fig_monthly_mean_temp</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Monthly Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_temperature</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">)</span>
<span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="c1"># series_monthly_total_rainfall = df['total_rainfall'].resample('M').mean()  # resample to monthly mean</span>
<span class="c1"># # series_yearly_total_rainfall = df['total_rainfall'].resample('Y').mean()  # resample to yearly mean</span>

<span class="c1"># # print(monthly_total_rainfall)</span>
<span class="c1"># # print(series_yearly_total_rainfall)</span>

<span class="c1"># # line plot for total rainfall</span>
<span class="c1"># fig_monthly_total_rainfall = px.line(monthly_total_rainfall, labels=&#123series_monthly_total_rainfall.index.name: 'Datetime', 'value': 'Total Rainfall (mm)'},title='Monthly Total Rainfall')</span>
<span class="c1"># fig_monthly_total_rainfall.update_xaxes(dtick='M12', tickangle=45)</span>
<span class="c1"># fig_monthly_total_rainfall.update_yaxes(dtick=100, tickangle=45)</span>
<span class="c1"># fig_monthly_total_rainfall.update_traces(hovertemplate='Datetime: %{x}&lt;br&gt;Total Rainfall: %{y}mm')</span>

<span class="c1"># # add the mean line</span>
<span class="c1"># mean_total_rainfall = np.mean(series_monthly_total_rainfall)</span>
<span class="c1"># fig_monthly_total_rainfall.add_shape(</span>
<span class="c1">#     type="line",</span>
<span class="c1">#     x0=series_monthly_total_rainfall.index[0],</span>
<span class="c1">#     y0=mean_total_rainfall,</span>
<span class="c1">#     x1=series_monthly_total_rainfall.index[-1],</span>
<span class="c1">#     y1=mean_total_rainfall,</span>
<span class="c1">#     line=dict(color="red", dash="dot"),</span>
<span class="c1"># )</span>
<span class="c1"># fig_monthly_total_rainfall.show()</span>

<span class="c1"># # Normalize mean temperature data</span>
<span class="c1"># normalized_mean_temp = preprocessing.scale(series_monthly_mean_temp)</span>
<span class="c1"># # Normalize total rainfall data</span>
<span class="c1"># normalized_total_rainfall = preprocessing.scale(series_monthly_total_rainfall)</span>

<span class="c1"># # Create a DataFrame with normalized data</span>
<span class="c1"># df_normalized = pd.DataFrame(&#123'Datetime': series_monthly_mean_temp.index,</span>
    <span class="c1">#                               'Normalized Mean Temperature': normalized_mean_temp,</span>
    <span class="c1">#                               'Normalized Total Rainfall': normalized_total_rainfall})</span>

<span class="c1"># # Combine the normalized data using plotly.express</span>
<span class="c1"># fig_combined = px.line(df_normalized, x='Datetime', y=['Normalized Mean Temperature', 'Normalized Total Rainfall'],</span>
<span class="c1">#                        labels=&#123'value': 'Normalized Value'},</span>
<span class="c1">#                        title='Combined Normalized Data')</span>
<span class="c1"># fig_combined.update_xaxes(dtick='M12', tickangle=45)</span>
<span class="c1"># fig_combined.update_yaxes(dtick=1, tickangle=45)</span>
<span class="c1"># fig_combined.update_traces(hovertemplate='Datetime: %{x}&lt;br&gt;Total Rainfall: %{y}mm')</span>

<span class="c1"># # Show the combined graph</span>
<span class="c1"># fig_combined.show()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_4.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[5]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">series_yearly_mean_temp</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="s1">'mean_temp'</span><span class="p">]</span><span class="o">.</span><span class="n">resample</span><span class="p">(</span><span class="s1">'Y'</span><span class="p">)</span><span class="o">.</span><span class="n">mean</span><span class="p">()</span>  <span class="c1"># resample to yearly mean</span>
<span class="c1"># print(series_yearly_mean_temp)</span>

<span class="n">fig_yearly_mean_temp</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">series_yearly_mean_temp</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">series_yearly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Yearly Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_yearly_mean_temp</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_yearly_mean_temp</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_yearly_mean_temp</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_temperature</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">series_yearly_mean_temp</span><span class="p">)</span>
<span class="n">fig_yearly_mean_temp</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">series_yearly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">series_yearly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_yearly_mean_temp</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_5.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="ARIMA-Series-Model-Development" data-toc-modified-id="ARIMA-Series-Model-Development-1.0.4"><a class="toc-mod-link" id="ARIMA-Series-Model-Development-1.0.4"></a><span class="toc-item-num">1.0.4&nbsp;&nbsp;</span>ARIMA Series Model Development<a class="anchor-link" href="#ARIMA-Series-Model-Development">¶</a></h3>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="Use-ACF-and-PACF-to-know-where-to-start" data-toc-modified-id="Use-ACF-and-PACF-to-know-where-to-start-1.0.4.1"><a class="toc-mod-link" id="Use-ACF-and-PACF-to-know-where-to-start-1.0.4.1"></a><span class="toc-item-num">1.0.4.1&nbsp;&nbsp;</span>Use ACF and PACF to know where to start<a class="anchor-link" href="#Use-ACF-and-PACF-to-know-where-to-start">¶</a></h4>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[6]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">acf_values</span> <span class="o">=</span> <span class="n">plot_acf</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">,</span> <span class="n">lags</span><span class="o">=</span><span class="mi">100</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_11_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Based on decaying ACF, we are likely dealing with an Auto Regressive process.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[7]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">pacf_values</span> <span class="o">=</span> <span class="n">plot_pacf</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">,</span> <span class="n">method</span><span class="o">=</span><span class="s1">'ywm'</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_13_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Based on decaying PACF, we should start with an Auto Regressive model with lags 1, 3, 9, 10, 11, 12.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="Augmented-Dickey-Fuller-Test" data-toc-modified-id="Augmented-Dickey-Fuller-Test-1.0.4.2"><a class="toc-mod-link" id="Augmented-Dickey-Fuller-Test-1.0.4.2"></a><span class="toc-item-num">1.0.4.2&nbsp;&nbsp;</span>Augmented Dickey-Fuller Test<a class="anchor-link" href="#Augmented-Dickey-Fuller-Test">¶</a></h4>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[8]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="k">def</span> <span class="nf">perform_adf_test</span><span class="p">(</span><span class="n">series</span><span class="p">):</span>
    <span class="n">result</span> <span class="o">=</span> <span class="n">adfuller</span><span class="p">(</span><span class="n">series</span><span class="p">)</span>
    <span class="n">adf_statistic</span> <span class="o">=</span> <span class="n">result</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
    <span class="n">p_value</span> <span class="o">=</span> <span class="n">result</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>
    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'ADF Statistic: </span><span class="si">&#123</span><span class="n">adf_statistic</span><span class="si">:</span><span class="s1">.4f</span><span class="si">}</span><span class="s1">'</span><span class="p">)</span>
    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'p-value: </span><span class="si">&#123</span><span class="n">p_value</span><span class="si">:</span><span class="s1">.4f</span><span class="si">}</span><span class="s1">'</span><span class="p">)</span>

<span class="n">perform_adf_test</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>ADF Statistic: -4.4622
p-value: 0.0002
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Since p-value &lt; 0.5, time series is stationary.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="ARIMA-Series-Model-Validation" data-toc-modified-id="ARIMA-Series-Model-Validation-1.0.5"><a class="toc-mod-link" id="ARIMA-Series-Model-Validation-1.0.5"></a><span class="toc-item-num">1.0.5&nbsp;&nbsp;</span>ARIMA Series Model Validation<a class="anchor-link" href="#ARIMA-Series-Model-Validation">¶</a></h3>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="AR-Model" data-toc-modified-id="AR-Model-1.0.5.1"><a class="toc-mod-link" id="AR-Model-1.0.5.1"></a><span class="toc-item-num">1.0.5.1&nbsp;&nbsp;</span>AR Model<a class="anchor-link" href="#AR-Model">¶</a></h4>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[9]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split 70:30 (28, 12)</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2011</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># create model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">))</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># summary of the model</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 0.32241296768188477
                               SARIMAX Results
==============================================================================
Dep. Variable:              mean_temp   No. Observations:                  348
Model:                ARIMA(12, 0, 0)   Log Likelihood                -236.362
Date:                Thu, 15 Jun 2023   AIC                            500.724
Time:                        02:19:43   BIC                            554.655
Sample:                    01-31-1982   HQIC                           522.195
                         - 12-31-2010
Covariance Type:                  opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
const         27.5814      0.156    176.262      0.000      27.275      27.888
ar.L1          0.5915      0.050     11.899      0.000       0.494       0.689
ar.L2          0.0056      0.065      0.087      0.931      -0.122       0.133
ar.L3         -0.0665      0.067     -0.998      0.318      -0.197       0.064
ar.L4         -0.0253      0.065     -0.391      0.696      -0.152       0.101
ar.L5         -0.0797      0.066     -1.212      0.226      -0.209       0.049
ar.L6          0.0405      0.067      0.607      0.544      -0.090       0.171
ar.L7         -0.0257      0.057     -0.449      0.653      -0.138       0.086
ar.L8          0.1044      0.065      1.610      0.107      -0.023       0.231
ar.L9         -0.1524      0.068     -2.246      0.025      -0.285      -0.019
ar.L10         0.1075      0.066      1.618      0.106      -0.023       0.238
ar.L11         0.1545      0.066      2.351      0.019       0.026       0.283
ar.L12         0.1930      0.056      3.436      0.001       0.083       0.303
sigma2         0.2254      0.018     12.621      0.000       0.190       0.260
===================================================================================
Ljung-Box (L1) (Q):                   0.23   Jarque-Bera (JB):                 0.58
Prob(Q):                              0.63   Prob(JB):                         0.75
Heteroskedasticity (H):               0.74   Skew:                             0.09
Prob(H) (two-sided):                  0.10   Kurtosis:                         2.92
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>We should only keep those lags with p-value &lt; 0.5.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[10]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from AR Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_10.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Clear pattern in residual data - means that there's some dynamic data that is failed to be captured i.e. not good.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[11]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_11.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0215
Root Mean Squared Error: 0.7288853463855004
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>AR(3) Model:</strong>
                    Mean Absolute Percent Error: 0.0242
                    Root Mean Squared Error: 0.8109909048888814</p>
                <p><strong>AR(12) Model:</strong>
                    Mean Absolute Percent Error: 0.0215
                    Root Mean Squared Error: 0.7288853463855004</p>
                <p>AR(12) did better than AR(3) here, as predicted by the lags of the PACF. Also, we can see that the further we predict into the future, the worst the predictions.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="Rolling-Forecast-Origin-(Rolling-Window)" data-toc-modified-id="Rolling-Forecast-Origin-(Rolling-Window)-1.0.5.2"><a class="toc-mod-link" id="Rolling-Forecast-Origin-(Rolling-Window)-1.0.5.2"></a><span class="toc-item-num">1.0.5.2&nbsp;&nbsp;</span>Rolling Forecast Origin (Rolling Window)<a class="anchor-link" href="#Rolling-Forecast-Origin-(Rolling-Window)">¶</a></h4><p>Predict 1 month in advance each time:</p>
                <p>Train on months 1, 2, ..., k - 3 -&gt; predict month k - 2</p>
                <p>Train on months 1, 2, ..., k - 3, k - 2 -&gt; predict month k - 1</p>
                <p>Train on months 1, 2, ..., k - 3, k - 2, k - 1 -&gt; predict month k</p>
                <p>...</p>
                <p>Average all predictions</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[12]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># create the model</span>
<span class="n">predictions_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">Series</span><span class="p">(</span><span class="n">dtype</span><span class="o">=</span><span class="s1">'float64'</span><span class="p">)</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="k">for</span> <span class="n">end_date</span> <span class="ow">in</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">:</span>
    <span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">end_date</span> <span class="o">-</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">)]</span>
    <span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">))</span>
    <span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
    <span class="n">pred</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">end_date</span><span class="p">)</span>
    <span class="n">predictions_rolling</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span> <span class="o">=</span> <span class="n">pred</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">residuals_rolling</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions_rolling</span>

<span class="c1"># print(residuals_rolling)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from AR Model (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error_rolling</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 46.334877014160156
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_12.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Although there is volatility in residual data, there is less pattern compared to just training on the test data in one shot (as shown above), means predictions will be closer and model is better.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[13]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions_rolling</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data_rolling</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_13.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0139
Root Mean Squared Error: 0.4852945337116935
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>AR(3) Model (Rolling Window):</strong>
                    Mean Absolute Percent Error: 0.0158
                    Root Mean Squared Error: 0.5362938714312385</p>
                <p><strong>AR(12) Model (Rolling Window):</strong>
                    Mean Absolute Percent Error: 0.0139
                    Root Mean Squared Error: 0.4852945337116935</p>
                <p>As shown here, the RMSE of rolling window (0.48529) is lower than that of the non-rolling window (0.72889) of AR(12), and it predicts a better shape as it predicts in 1 month intervals of the test data consecutively rather than predicting over the whole test data. The downside is that rolling window takes a much longer time to train.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="MA-Model" data-toc-modified-id="MA-Model-1.0.5.3"><a class="toc-mod-link" id="MA-Model-1.0.5.3"></a><span class="toc-item-num">1.0.5.3&nbsp;&nbsp;</span>MA Model<a class="anchor-link" href="#MA-Model">¶</a></h4><p>Using ACF, we can know which lag/order to use for the MA model.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[14]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">acf_values</span> <span class="o">=</span> <span class="n">plot_acf</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_32_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Based on decaying ACF, we should start with a Moving Average model with lags 1, 2 (for simplicity).</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[15]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split 70:30 (28, 12)</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2011</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># create model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">2</span><span class="p">))</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># summary of the model</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 0.036110877990722656
                               SARIMAX Results
==============================================================================
Dep. Variable:              mean_temp   No. Observations:                  348
Model:                 ARIMA(0, 0, 2)   Log Likelihood                -298.502
Date:                Thu, 15 Jun 2023   AIC                            605.004
Time:                        02:20:45   BIC                            620.413
Sample:                    01-31-1982   HQIC                           611.139
                         - 12-31-2010
Covariance Type:                  opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
const         27.5641      0.065    423.368      0.000      27.437      27.692
ma.L1          0.7289      0.052     14.098      0.000       0.628       0.830
ma.L2          0.4013      0.050      7.985      0.000       0.303       0.500
sigma2         0.3249      0.026     12.594      0.000       0.274       0.375
===================================================================================
Ljung-Box (L1) (Q):                   2.30   Jarque-Bera (JB):                 0.36
Prob(Q):                              0.13   Prob(JB):                         0.83
Heteroskedasticity (H):               0.86   Skew:                            -0.02
Prob(H) (two-sided):                  0.40   Kurtosis:                         2.85
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>From the constants and the lag terms, we should use the predicted model:</p>
                <p>ŷ(t) = 28 + 0.73ε(t-1) + 0.40ε(t-2) (ignore ε(t) as current prediction error is caught on the fly)</p>
                <p>In this equation:</p>
                <p>ŷ(t) represents the predicted value of the dependent variable at time t.
                    ε(t-1) represents the prediction error (residual) at time (t-1).
                    ε(t-2) represents the prediction error (residual) at time (t-2).
                    The coefficients 0.73 and 0.40 represent the weights assigned to the lagged prediction errors (ε).</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[16]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from MA Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_16.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Similar to the AR model above (without rolling window), clear pattern in residual data - means that there's some dynamic data that is failed to be captured i.e. not good.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[17]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_17.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0243
Root Mean Squared Error: 0.813192975445521
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>As we used MA(2) of 2 lag periods, we could only predict the first 2 months of the test data. The MA model will then predict the rest of the test data as the mean value as shown above. This is a characteristic of the MA model.</p>
                <p>For simplicity, we will omit the rolling window version of the MA model.</p>
                <p>AR model uses PACF whereas MA model uses ACF.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="ARMA-Model" data-toc-modified-id="ARMA-Model-1.0.5.4"><a class="toc-mod-link" id="ARMA-Model-1.0.5.4"></a><span class="toc-item-num">1.0.5.4&nbsp;&nbsp;</span>ARMA Model<a class="anchor-link" href="#ARMA-Model">¶</a></h4><p>Although the above Augmented Dickey-Fuller Test showed a low p-value implying that the series might be stationary, we cannot be too sure as it seems as if there is a slight upward trend (possibly due to global warming) by just looking at the graph. To confirm, let's perform the first difference to check for stationarity. We can see the difference easier by comparing both graphs as shown below.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[18]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">show</span><span class="p">()</span> <span class="c1"># for easier comparison</span>

<span class="n">first_diff</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">diff</span><span class="p">()[</span><span class="mi">1</span><span class="p">:]</span>
<span class="nb">print</span><span class="p">(</span><span class="n">first_diff</span><span class="p">)</span>

<span class="c1"># line plot for mean temperature</span>
<span class="n">fig_first_diff</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">first_diff</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'First Difference of Monthly Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_temperature</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">first_diff</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_4.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>datetime
1982-02-28    1.2
1982-03-31    0.1
1982-04-30   -0.2
1982-05-31    1.0
1982-06-30    0.4
             ...
2022-12-31   -0.6
2023-01-31   -0.3
2023-02-28    0.4
2023-03-31    0.2
2023-04-30    1.4
Freq: M, Name: mean_temp, Length: 495, dtype: float64
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_18.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>As the differenced series appears to be more stationary, it suggests that the original series had some form of trend or seasonality that was removed, in so doing, the data is preprocessed.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[19]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">acf_values</span> <span class="o">=</span> <span class="n">plot_acf</span><span class="p">(</span><span class="n">first_diff</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_43_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Based on decaying ACF, we are should start with a MA process of order 12.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[20]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">pacf_values</span> <span class="o">=</span> <span class="n">plot_pacf</span><span class="p">(</span><span class="n">first_diff</span><span class="p">,</span> <span class="n">method</span><span class="o">=</span><span class="s1">'ywm'</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_45_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Based on decaying PACF, we are should start with a AR process of order 9.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>From here on, our test data will only consist of 1 year as it takes very long to fit the model with higher order processes, especially with the Rolling Forecast Origin.</strong></p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[21]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split to test 1 year of data as splitting 70:30 takes very long</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2022</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">first_diff</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">first_diff</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># create model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">9</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">12</span><span class="p">))</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># summary of the model</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 1.7389419078826904
                               SARIMAX Results
==============================================================================
Dep. Variable:              mean_temp   No. Observations:                  479
Model:                ARIMA(9, 0, 12)   Log Likelihood                -287.025
Date:                Thu, 15 Jun 2023   AIC                            620.050
Time:                        02:20:47   BIC                            715.999
Sample:                    02-28-1982   HQIC                           657.768
                         - 12-31-2021
Covariance Type:                  opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
const          0.0022      0.005      0.432      0.666      -0.008       0.012
ar.L1         -0.2740      0.168     -1.633      0.103      -0.603       0.055
ar.L2         -0.2867      0.136     -2.115      0.034      -0.552      -0.021
ar.L3         -0.2837      0.112     -2.529      0.011      -0.504      -0.064
ar.L4         -0.3228      0.130     -2.487      0.013      -0.577      -0.068
ar.L5         -0.4790      0.109     -4.395      0.000      -0.693      -0.265
ar.L6         -0.2459      0.145     -1.701      0.089      -0.529       0.037
ar.L7         -0.4211      0.115     -3.668      0.000      -0.646      -0.196
ar.L8         -0.3796      0.131     -2.900      0.004      -0.636      -0.123
ar.L9         -0.6483      0.140     -4.624      0.000      -0.923      -0.373
ma.L1         -0.2665      0.168     -1.583      0.113      -0.596       0.063
ma.L2          0.0438      0.184      0.238      0.812      -0.317       0.404
ma.L3         -0.0164      0.162     -0.101      0.920      -0.334       0.301
ma.L4          0.0635      0.150      0.422      0.673      -0.231       0.358
ma.L5          0.1606      0.155      1.036      0.300      -0.143       0.465
ma.L6         -0.0423      0.157     -0.269      0.788      -0.351       0.266
ma.L7          0.3150      0.147      2.142      0.032       0.027       0.603
ma.L8          0.1215      0.168      0.724      0.469      -0.208       0.451
ma.L9          0.2605      0.149      1.745      0.081      -0.032       0.553
ma.L10        -0.5671      0.083     -6.830      0.000      -0.730      -0.404
ma.L11        -0.1424      0.062     -2.296      0.022      -0.264      -0.021
ma.L12         0.1362      0.060      2.280      0.023       0.019       0.253
sigma2         0.1866      0.013     13.900      0.000       0.160       0.213
===================================================================================
Ljung-Box (L1) (Q):                   0.04   Jarque-Bera (JB):                 0.01
Prob(Q):                              0.85   Prob(JB):                         0.99
Heteroskedasticity (H):               0.91   Skew:                             0.01
Prob(H) (two-sided):                  0.55   Kurtosis:                         2.99
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[22]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from ARMA Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_22.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[23]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'First Difference of Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;First Difference of Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_23.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: inf
Root Mean Squared Error: 0.5841389478876554
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Not very good, still has room for improvement.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="ARIMA-Model" data-toc-modified-id="ARIMA-Model-1.0.5.5"><a class="toc-mod-link" id="ARIMA-Model-1.0.5.5"></a><span class="toc-item-num">1.0.5.5&nbsp;&nbsp;</span>ARIMA Model<a class="anchor-link" href="#ARIMA-Model">¶</a></h4>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Now, let's use the I component (Integrated) to account for the first difference. Like before, we first analyse the ACF and PACF.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[24]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">first_diff</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">diff</span><span class="p">()[</span><span class="mi">1</span><span class="p">:]</span>
<span class="c1"># print(first_diff)</span>

<span class="c1"># line plot for mean temperature</span>
<span class="n">fig_first_diff</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">first_diff</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'First Difference of Monthly Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_temperature</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">first_diff</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_24.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[25]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">acf_values</span> <span class="o">=</span> <span class="n">plot_acf</span><span class="p">(</span><span class="n">first_diff</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_55_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[26]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">pacf_values</span> <span class="o">=</span> <span class="n">plot_pacf</span><span class="p">(</span><span class="n">first_diff</span><span class="p">,</span> <span class="n">method</span><span class="o">=</span><span class="s1">'ywm'</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_56_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[27]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split to test 1 year of data as splitting 70:30 takes very long</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2022</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># create model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">9</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">12</span><span class="p">))</span> <span class="c1"># (p, d, q) here we use d as 1 as we only performed 1 difference to make the series stationary.</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># summary of the model</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 2.0054309368133545
                               SARIMAX Results
==============================================================================
Dep. Variable:              mean_temp   No. Observations:                  480
Model:                ARIMA(9, 1, 12)   Log Likelihood                -285.269
Date:                Thu, 15 Jun 2023   AIC                            614.538
Time:                        02:20:50   BIC                            706.316
Sample:                    01-31-1982   HQIC                           650.617
                         - 12-31-2021
Covariance Type:                  opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
ar.L1         -0.4575      0.117     -3.923      0.000      -0.686      -0.229
ar.L2         -0.2523      0.091     -2.759      0.006      -0.431      -0.073
ar.L3         -0.2135      0.068     -3.119      0.002      -0.348      -0.079
ar.L4         -0.4251      0.080     -5.314      0.000      -0.582      -0.268
ar.L5         -0.5372      0.058     -9.296      0.000      -0.650      -0.424
ar.L6         -0.2260      0.086     -2.625      0.009      -0.395      -0.057
ar.L7         -0.4289      0.066     -6.520      0.000      -0.558      -0.300
ar.L8         -0.4920      0.082     -5.985      0.000      -0.653      -0.331
ar.L9         -0.6547      0.106     -6.184      0.000      -0.862      -0.447
ma.L1         -0.0913      0.119     -0.765      0.444      -0.325       0.143
ma.L2         -0.0887      0.111     -0.798      0.425      -0.307       0.129
ma.L3         -0.0609      0.100     -0.609      0.542      -0.257       0.135
ma.L4          0.1741      0.090      1.925      0.054      -0.003       0.351
ma.L5          0.1819      0.086      2.122      0.034       0.014       0.350
ma.L6         -0.1087      0.092     -1.176      0.240      -0.290       0.072
ma.L7          0.3366      0.084      4.023      0.000       0.173       0.501
ma.L8          0.2565      0.099      2.600      0.009       0.063       0.450
ma.L9          0.2316      0.102      2.280      0.023       0.033       0.431
ma.L10        -0.6316      0.066     -9.503      0.000      -0.762      -0.501
ma.L11        -0.1682      0.060     -2.818      0.005      -0.285      -0.051
ma.L12         0.1720      0.059      2.939      0.003       0.057       0.287
sigma2         0.1846      0.014     12.851      0.000       0.156       0.213
===================================================================================
Ljung-Box (L1) (Q):                   0.04   Jarque-Bera (JB):                 0.00
Prob(Q):                              0.85   Prob(JB):                         1.00
Heteroskedasticity (H):               0.93   Skew:                            -0.00
Prob(H) (two-sided):                  0.64   Kurtosis:                         3.01
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[28]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from ARIMA Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_28.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[29]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_29.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0109
Root Mean Squared Error: 0.40002647470247793
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Compared to using just the ARMA model with first difference performed, with both AR(9) and MA(12), the ARIMA model performed better, having a RMSE (0.40003), lower than that of the ARMA model (0.58414).</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Let's try to improve it using the rolling forecast origin.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[30]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># create the model</span>
<span class="n">predictions_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">Series</span><span class="p">(</span><span class="n">dtype</span><span class="o">=</span><span class="s1">'float64'</span><span class="p">)</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="k">for</span> <span class="n">end_date</span> <span class="ow">in</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">:</span>
    <span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">end_date</span> <span class="o">-</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">)]</span>
    <span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">9</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">12</span><span class="p">))</span> <span class="c1"># (p, d, q) here we use d as 1 as we are taking into account the first difference to mitigate the slight upward trend.</span>
    <span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
    <span class="n">pred</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">end_date</span><span class="p">)</span>
    <span class="n">predictions_rolling</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span> <span class="o">=</span> <span class="n">pred</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">residuals_rolling</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions_rolling</span>

<span class="c1"># print(residuals_rolling)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from ARIMA Model (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error_rolling</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 18.78998899459839
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_30.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[31]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions_rolling</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data_rolling</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_31.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0113
Root Mean Squared Error: 0.4101693694305862
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Here although it seems like the rolling forecast origin of the ARIMA model predicted values that had a closer shape following that of the test data, it has a slightly higher RMSE (0.41017) compared to the non-rolling version (0.40003). It seems that the rolling forecast origin is less effective when predicting over a short time period. It took quite a while to fit the model, even though we reduced our test data to just 1 year. This is probably due to the higher orders or AR and MA that we used.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="SARIMA-Model" data-toc-modified-id="SARIMA-Model-1.0.5.6"><a class="toc-mod-link" id="SARIMA-Model-1.0.5.6"></a><span class="toc-item-num">1.0.5.6&nbsp;&nbsp;</span>SARIMA Model<a class="anchor-link" href="#SARIMA-Model">¶</a></h4><p>Let's start by performing the first difference to remove the upward trend.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[32]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># fig_monthly_mean_temp.show() # for easier comparison</span>

<span class="n">first_diff</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">diff</span><span class="p">()[</span><span class="mi">1</span><span class="p">:]</span>
<span class="c1"># print(first_diff)</span>

<span class="c1"># line plot for mean temperature</span>
<span class="n">fig_first_diff</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">first_diff</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'First Difference of Monthly Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_temperature</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">first_diff</span><span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">first_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_first_diff</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_32.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>By zooming into the above graph, although we removed the upward trend, seasonality can still be observed, just like the original graph. Hence, lets perform a seasonal difference of 12 months, since we can observe the seasonality within every 12 months.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[33]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># Perform seasonal differencing</span>
<span class="n">seasonal_diff</span> <span class="o">=</span> <span class="n">first_diff</span><span class="o">.</span><span class="n">diff</span><span class="p">(</span><span class="mi">12</span><span class="p">)[</span><span class="mi">12</span><span class="p">:]</span>
<span class="c1"># print(seasonal_diff)</span>

<span class="c1"># Line plot for seasonal difference of mean temperature</span>
<span class="n">fig_seasonal_diff</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">seasonal_diff</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">seasonal_diff</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Seasonal Difference (+ First Difference) of Monthly Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_seasonal_diff</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_seasonal_diff</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_seasonal_diff</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>

<span class="c1"># Add the mean line</span>
<span class="n">mean_temperature</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">seasonal_diff</span><span class="p">)</span>
<span class="n">fig_seasonal_diff</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">seasonal_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">seasonal_diff</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_temperature</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_seasonal_diff</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_33.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Great, now it's hard to observe seasonality. Now we have a time series that is probably stationary.</p>
                <p>Requirements for having a stationary time series:</p>
                <ol>
                    <li><p>Constant mean: The mean of the time series remains constant over time. This means that the average value of the series does not change as time progresses.</p>
                    </li>
                    <li><p>Constant variance: The variance (or standard deviation) of the time series remains constant over time. This implies that the spread or dispersion of the data points does not change.</p>
                    </li>
                    <li><p>No seasonality: There is no systematic pattern or periodic fluctuations observed in the series. Seasonality refers to regular and predictable variations that occur at specific intervals, such as daily, weekly, or yearly patterns.</p>
                    </li>
                    <li><p>No trend: The series does not exhibit a long-term increasing or decreasing pattern. A trend represents a gradual change in the mean or level of the series over an extended period.</p>
                    </li>
                </ol>
                <p>Now we analyse its ACF and PACF.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[34]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">acf_values</span> <span class="o">=</span> <span class="n">plot_acf</span><span class="p">(</span><span class="n">seasonal_diff</span><span class="p">,</span> <span class="n">lags</span><span class="o">=</span><span class="mi">50</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xticks</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">51</span><span class="p">,</span> <span class="mi">5</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_70_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[35]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">pacf_values</span> <span class="o">=</span> <span class="n">plot_pacf</span><span class="p">(</span><span class="n">seasonal_diff</span><span class="p">,</span> <span class="n">lags</span><span class="o">=</span><span class="mi">50</span><span class="p">,</span> <span class="n">method</span><span class="o">=</span><span class="s1">'ywm'</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xticks</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">51</span><span class="p">,</span> <span class="mi">5</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>




                        <div class="output_png output_subarea ">
                            <img src="model_matplotlib_figures/Singapore%20Weather%20Prediction_71_0.png">
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>As shown above, there are significant spikes in the ACF plot at lag 1 and 12. In the PACF plot, there is a significant spike at lag 1 and there are significant spikes at intervals of 12 lags. Since we performed a first difference of the original data, d=1 of the normal order, and since we also performed a seasonal difference, D=1 of the seasonal order. Due to the significant spikes at lag 1 of both the ACF and PACF, these are non-seasonal lags, therefore we can set p=1 and q=1 of the normal order. Due to the spikes at lag 12 of both the ACF and PACF, we can set P=1 and Q=1 (since the seasonal lag is 12 months)of the seasonal order. Last but not least, since the seasonal lag happens every 12 months, m=12 of the seasonal order. These characteristics suggest a potential parameter starting point of SARIMA(1,1,1)x(1,1,1,12).</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[36]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split to test 1 year of data as splitting 70:30 takes very long</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2022</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># create model</span>
<span class="n">normal_order</span> <span class="o">=</span> <span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">seasonal_order</span> <span class="o">=</span> <span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">12</span><span class="p">)</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="n">normal_order</span><span class="p">,</span> <span class="n">seasonal_order</span><span class="o">=</span><span class="n">seasonal_order</span><span class="p">)</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># summary of the model</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 1.1708199977874756
                                    SARIMAX Results
========================================================================================
Dep. Variable:                        mean_temp   No. Observations:                  480
Model:             ARIMA(1, 1, 1)x(1, 1, 1, 12)   Log Likelihood                -277.962
Date:                          Thu, 15 Jun 2023   AIC                            565.924
Time:                                  02:21:10   BIC                            586.655
Sample:                              01-31-1982   HQIC                           574.082
                                   - 12-31-2021
Covariance Type:                            opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
ar.L1          0.1856      0.067      2.752      0.006       0.053       0.318
ma.L1         -0.7552      0.049    -15.360      0.000      -0.852      -0.659
ar.S.L12       0.0151      0.053      0.287      0.774      -0.088       0.118
ma.S.L12      -0.9981      0.754     -1.324      0.185      -2.475       0.479
sigma2         0.1754      0.130      1.348      0.178      -0.080       0.430
===================================================================================
Ljung-Box (L1) (Q):                   0.06   Jarque-Bera (JB):                 5.93
Prob(Q):                              0.81   Prob(JB):                         0.05
Heteroskedasticity (H):               0.89   Skew:                            -0.25
Prob(H) (two-sided):                  0.47   Kurtosis:                         2.76
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>From the model summary, we can see that there is a high p-value (&gt;0.5) for the seasonal AR component, so it seems redundant and that there is some discrepancy that we have not accounted for. Note: I used <code>model = SARIMAX(train_data, order=normal_order, seasonal_order=seasonal_order)</code> and there was no difference in result. Seems like the ARIMA function can apply the SARIMA model as well.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[37]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from SARIMA Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_37.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[38]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_38.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0155
Root Mean Squared Error: 0.5200608882024743
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Seems like our SARIMA model performed worse than our ARIMA model (RMSE=0.40003). Let's try applying the rolling forecast origin.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[39]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">normal_order</span> <span class="o">=</span> <span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">seasonal_order</span> <span class="o">=</span> <span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">12</span><span class="p">)</span>

<span class="c1"># create the model</span>
<span class="n">predictions_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">Series</span><span class="p">(</span><span class="n">dtype</span><span class="o">=</span><span class="s1">'float64'</span><span class="p">)</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="k">for</span> <span class="n">end_date</span> <span class="ow">in</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">:</span>
    <span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">end_date</span> <span class="o">-</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">)]</span>
    <span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="n">normal_order</span><span class="p">,</span> <span class="n">seasonal_order</span><span class="o">=</span><span class="n">seasonal_order</span><span class="p">)</span>
    <span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
    <span class="n">pred</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">end_date</span><span class="p">)</span>
    <span class="n">predictions_rolling</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span> <span class="o">=</span> <span class="n">pred</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">residuals_rolling</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions_rolling</span>

<span class="c1"># print(residuals_rolling)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from SARIMA Model (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error_rolling</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 8.850817203521729
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_39.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[40]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions_rolling</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data_rolling</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_40.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0123
Root Mean Squared Error: 0.43694862169817994
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>We can see that the rolling forecast origin on the SARIMA model did better, but it still fell short to the ARIMA model (rolling window RMSE=0.41017 and non-rolling RMSE=0.40003). Perhaps, the orders chosen were not the best or the SARIMA overfitted to a greater extent.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="ARIMA-Series-Model-Refinement:-Automated-Parameter-Selection-with-auto_arima" data-toc-modified-id="ARIMA-Series-Model-Refinement:-Automated-Parameter-Selection-with-auto_arima-1.0.6"><a class="toc-mod-link" id="ARIMA-Series-Model-Refinement:-Automated-Parameter-Selection-with-auto_arima-1.0.6"></a><span class="toc-item-num">1.0.6&nbsp;&nbsp;</span>ARIMA Series Model Refinement: Automated Parameter Selection with <code>auto_arima</code><a class="anchor-link" href="#ARIMA-Series-Model-Refinement:-Automated-Parameter-Selection-with-auto_arima">¶</a></h3><p>To automate the process of parameter selection in time series modeling, we can use the <code>auto_arima</code> function provided by the <code>pmdarima</code> library. These functions use a combination of algorithms and heuristics to find the best set of parameters for the ARIMA and SARIMA models, respectively.</p>
                <h4 id="Auto-ARIMA" data-toc-modified-id="Auto-ARIMA-1.0.6.1"><a class="toc-mod-link" id="Auto-ARIMA-1.0.6.1"></a><span class="toc-item-num">1.0.6.1&nbsp;&nbsp;</span>Auto ARIMA<a class="anchor-link" href="#Auto-ARIMA">¶</a></h4><p>The <code>auto_arima</code> function can be used to automatically determine the optimal parameters for an ARIMA model. It considers various combinations of p, d, and q values and evaluates the models based on the AIC (Akaike Information Criterion) or BIC (Bayesian Information Criterion).</p>
                <p>The AIC and BIC are based on the principle of trade-off between goodness of fit and model complexity. The goal is to find a model that fits the data well but is not overly complex, as overly complex models can lead to overfitting.</p>
                <p>The AIC is defined as:</p>
                <p>AIC = -2 <em> log-likelihood + 2 </em> k,</p>
                <p>where log-likelihood is a measure of how well the model fits the data, and k is the number of parameters in the model. The AIC penalizes models with a larger number of parameters, meaning that models with a higher AIC value are considered less favorable.</p>
                <p>The BIC is similar to the AIC but includes a stronger penalty for model complexity. It is defined as:</p>
                <p>BIC = -2 <em> log-likelihood + k </em> log(n),</p>
                <p>where n is the number of observations in the data. The BIC penalizes models with a larger number of parameters more severely than the AIC, leading to a more conservative model selection.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[41]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split to test 1 year of data as splitting 70:30 takes very long</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2022</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># Find optimal ARIMA order using auto_arima</span>
<span class="n">model_arima</span> <span class="o">=</span> <span class="n">auto_arima</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">,</span> <span class="n">d</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">max_d</span><span class="o">=</span><span class="mi">3</span><span class="p">,</span> <span class="n">max_p</span><span class="o">=</span><span class="mi">12</span><span class="p">,</span> <span class="n">max_q</span><span class="o">=</span><span class="mi">12</span><span class="p">,</span> <span class="n">max_order</span><span class="o">=</span><span class="mi">24</span><span class="p">,</span> <span class="n">parallel</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">num_cores</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">seasonal</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">information_criterion</span><span class="o">=</span><span class="s1">'aic'</span><span class="p">,</span> <span class="n">trace</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">stepwise</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>

<span class="c1"># Get the best ARIMA order</span>
<span class="n">order_arima</span> <span class="o">=</span> <span class="n">model_arima</span><span class="o">.</span><span class="n">order</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Optimal ARIMA order:"</span><span class="p">,</span> <span class="n">order_arima</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre> ARIMA(0,0,0)(0,0,0)[0]             : AIC=4703.909, Time=0.01 sec
 ARIMA(0,0,1)(0,0,0)[0]             : AIC=4044.152, Time=0.05 sec
 ARIMA(0,0,2)(0,0,0)[0]             : AIC=3447.842, Time=0.10 sec
 ARIMA(0,0,3)(0,0,0)[0]             : AIC=3012.063, Time=0.25 sec
 ARIMA(0,0,4)(0,0,0)[0]             : AIC=2644.616, Time=0.36 sec
 ARIMA(0,0,5)(0,0,0)[0]             : AIC=2373.222, Time=0.19 sec
 ARIMA(0,0,6)(0,0,0)[0]             : AIC=2168.781, Time=0.38 sec
 ARIMA(0,0,7)(0,0,0)[0]             : AIC=inf, Time=0.50 sec
 ARIMA(0,0,8)(0,0,0)[0]             : AIC=inf, Time=0.66 sec
 ARIMA(0,0,9)(0,0,0)[0]             : AIC=inf, Time=0.64 sec
 ARIMA(0,0,10)(0,0,0)[0]             : AIC=inf, Time=1.06 sec
 ARIMA(0,0,11)(0,0,0)[0]             : AIC=1578.521, Time=0.58 sec
 ARIMA(0,0,12)(0,0,0)[0]             : AIC=inf, Time=1.12 sec
 ARIMA(1,0,0)(0,0,0)[0]             : AIC=inf, Time=0.01 sec
 ARIMA(1,0,1)(0,0,0)[0]             : AIC=923.908, Time=0.04 sec
 ARIMA(1,0,2)(0,0,0)[0]             : AIC=923.974, Time=0.03 sec
 ARIMA(1,0,3)(0,0,0)[0]             : AIC=855.327, Time=0.14 sec
 ARIMA(1,0,4)(0,0,0)[0]             : AIC=836.260, Time=0.19 sec
 ARIMA(1,0,5)(0,0,0)[0]             : AIC=821.881, Time=0.40 sec
 ARIMA(1,0,6)(0,0,0)[0]             : AIC=823.465, Time=0.29 sec
 ARIMA(1,0,7)(0,0,0)[0]             : AIC=811.098, Time=0.31 sec
 ARIMA(1,0,8)(0,0,0)[0]             : AIC=806.365, Time=0.41 sec
 ARIMA(1,0,9)(0,0,0)[0]             : AIC=830.695, Time=0.56 sec
 ARIMA(1,0,10)(0,0,0)[0]             : AIC=810.304, Time=0.74 sec
 ARIMA(1,0,11)(0,0,0)[0]             : AIC=842.901, Time=0.87 sec
 ARIMA(1,0,12)(0,0,0)[0]             : AIC=791.315, Time=1.05 sec
 ARIMA(2,0,0)(0,0,0)[0]             : AIC=inf, Time=0.02 sec
 ARIMA(2,0,1)(0,0,0)[0]             : AIC=920.574, Time=0.10 sec
 ARIMA(2,0,2)(0,0,0)[0]             : AIC=849.830, Time=0.15 sec
 ARIMA(2,0,3)(0,0,0)[0]             : AIC=923.979, Time=0.13 sec
 ARIMA(2,0,4)(0,0,0)[0]             : AIC=inf, Time=0.28 sec
 ARIMA(2,0,5)(0,0,0)[0]             : AIC=825.991, Time=0.28 sec
 ARIMA(2,0,6)(0,0,0)[0]             : AIC=826.869, Time=0.34 sec
 ARIMA(2,0,7)(0,0,0)[0]             : AIC=825.486, Time=0.40 sec
 ARIMA(2,0,8)(0,0,0)[0]             : AIC=inf, Time=0.55 sec
 ARIMA(2,0,9)(0,0,0)[0]             : AIC=inf, Time=0.70 sec
 ARIMA(2,0,10)(0,0,0)[0]             : AIC=inf, Time=0.81 sec
 ARIMA(2,0,11)(0,0,0)[0]             : AIC=inf, Time=0.79 sec
 ARIMA(2,0,12)(0,0,0)[0]             : AIC=inf, Time=1.02 sec
 ARIMA(3,0,0)(0,0,0)[0]             : AIC=inf, Time=0.05 sec
 ARIMA(3,0,1)(0,0,0)[0]             : AIC=923.853, Time=0.05 sec
 ARIMA(3,0,2)(0,0,0)[0]             : AIC=924.562, Time=0.15 sec
 ARIMA(3,0,3)(0,0,0)[0]             : AIC=926.715, Time=0.18 sec
 ARIMA(3,0,4)(0,0,0)[0]             : AIC=inf, Time=0.26 sec
 ARIMA(3,0,5)(0,0,0)[0]             : AIC=877.535, Time=0.24 sec
 ARIMA(3,0,6)(0,0,0)[0]             : AIC=inf, Time=0.43 sec
 ARIMA(3,0,7)(0,0,0)[0]             : AIC=821.491, Time=0.37 sec
 ARIMA(3,0,8)(0,0,0)[0]             : AIC=inf, Time=0.68 sec
 ARIMA(3,0,9)(0,0,0)[0]             : AIC=inf, Time=0.89 sec
 ARIMA(3,0,10)(0,0,0)[0]             : AIC=inf, Time=0.90 sec
 ARIMA(3,0,11)(0,0,0)[0]             : AIC=inf, Time=1.03 sec
 ARIMA(3,0,12)(0,0,0)[0]             : AIC=inf, Time=1.12 sec
 ARIMA(4,0,0)(0,0,0)[0]             : AIC=inf, Time=0.03 sec
 ARIMA(4,0,1)(0,0,0)[0]             : AIC=808.797, Time=0.18 sec
 ARIMA(4,0,2)(0,0,0)[0]             : AIC=926.005, Time=0.21 sec
 ARIMA(4,0,3)(0,0,0)[0]             : AIC=925.608, Time=0.25 sec
 ARIMA(4,0,4)(0,0,0)[0]             : AIC=930.438, Time=0.30 sec
 ARIMA(4,0,5)(0,0,0)[0]             : AIC=inf, Time=0.63 sec
 ARIMA(4,0,6)(0,0,0)[0]             : AIC=inf, Time=0.57 sec
 ARIMA(4,0,7)(0,0,0)[0]             : AIC=825.358, Time=0.41 sec
 ARIMA(4,0,8)(0,0,0)[0]             : AIC=inf, Time=0.76 sec
 ARIMA(4,0,9)(0,0,0)[0]             : AIC=inf, Time=0.88 sec
 ARIMA(4,0,10)(0,0,0)[0]             : AIC=inf, Time=1.07 sec
 ARIMA(4,0,11)(0,0,0)[0]             : AIC=inf, Time=1.11 sec
 ARIMA(4,0,12)(0,0,0)[0]             : AIC=inf, Time=1.31 sec
 ARIMA(5,0,0)(0,0,0)[0]             : AIC=inf, Time=0.04 sec
 ARIMA(5,0,1)(0,0,0)[0]             : AIC=800.915, Time=0.23 sec
 ARIMA(5,0,2)(0,0,0)[0]             : AIC=inf, Time=0.26 sec
 ARIMA(5,0,3)(0,0,0)[0]             : AIC=930.156, Time=0.25 sec
 ARIMA(5,0,4)(0,0,0)[0]             : AIC=inf, Time=0.35 sec
 ARIMA(5,0,5)(0,0,0)[0]             : AIC=inf, Time=0.47 sec
 ARIMA(5,0,6)(0,0,0)[0]             : AIC=inf, Time=0.51 sec
 ARIMA(5,0,7)(0,0,0)[0]             : AIC=inf, Time=0.55 sec
 ARIMA(5,0,8)(0,0,0)[0]             : AIC=inf, Time=0.86 sec
 ARIMA(5,0,9)(0,0,0)[0]             : AIC=inf, Time=0.97 sec
 ARIMA(5,0,10)(0,0,0)[0]             : AIC=inf, Time=1.02 sec
 ARIMA(5,0,11)(0,0,0)[0]             : AIC=inf, Time=1.11 sec
 ARIMA(5,0,12)(0,0,0)[0]             : AIC=inf, Time=1.48 sec
 ARIMA(6,0,0)(0,0,0)[0]             : AIC=inf, Time=0.05 sec
 ARIMA(6,0,1)(0,0,0)[0]             : AIC=793.180, Time=0.25 sec
 ARIMA(6,0,2)(0,0,0)[0]             : AIC=inf, Time=0.35 sec
 ARIMA(6,0,3)(0,0,0)[0]             : AIC=932.158, Time=0.31 sec
 ARIMA(6,0,4)(0,0,0)[0]             : AIC=inf, Time=0.41 sec
 ARIMA(6,0,5)(0,0,0)[0]             : AIC=inf, Time=0.50 sec
 ARIMA(6,0,6)(0,0,0)[0]             : AIC=inf, Time=0.58 sec
 ARIMA(6,0,7)(0,0,0)[0]             : AIC=inf, Time=0.66 sec
 ARIMA(6,0,8)(0,0,0)[0]             : AIC=inf, Time=1.04 sec
 ARIMA(6,0,9)(0,0,0)[0]             : AIC=inf, Time=0.98 sec
 ARIMA(6,0,10)(0,0,0)[0]             : AIC=inf, Time=1.19 sec
 ARIMA(6,0,11)(0,0,0)[0]             : AIC=inf, Time=1.16 sec
 ARIMA(6,0,12)(0,0,0)[0]             : AIC=inf, Time=1.31 sec
 ARIMA(7,0,0)(0,0,0)[0]             : AIC=inf, Time=0.06 sec
 ARIMA(7,0,1)(0,0,0)[0]             : AIC=793.117, Time=0.29 sec
 ARIMA(7,0,2)(0,0,0)[0]             : AIC=inf, Time=0.44 sec
 ARIMA(7,0,3)(0,0,0)[0]             : AIC=924.186, Time=0.39 sec
 ARIMA(7,0,4)(0,0,0)[0]             : AIC=927.444, Time=0.51 sec
 ARIMA(7,0,5)(0,0,0)[0]             : AIC=inf, Time=0.65 sec
 ARIMA(7,0,6)(0,0,0)[0]             : AIC=inf, Time=0.72 sec
 ARIMA(7,0,7)(0,0,0)[0]             : AIC=inf, Time=0.64 sec
 ARIMA(7,0,8)(0,0,0)[0]             : AIC=inf, Time=0.85 sec
 ARIMA(7,0,9)(0,0,0)[0]             : AIC=inf, Time=0.87 sec
 ARIMA(7,0,10)(0,0,0)[0]             : AIC=inf, Time=1.10 sec
 ARIMA(7,0,11)(0,0,0)[0]             : AIC=inf, Time=1.26 sec
 ARIMA(7,0,12)(0,0,0)[0]             : AIC=inf, Time=1.32 sec
 ARIMA(8,0,0)(0,0,0)[0]             : AIC=inf, Time=0.06 sec
 ARIMA(8,0,1)(0,0,0)[0]             : AIC=786.944, Time=0.32 sec
 ARIMA(8,0,2)(0,0,0)[0]             : AIC=794.122, Time=0.37 sec
 ARIMA(8,0,3)(0,0,0)[0]             : AIC=inf, Time=0.48 sec
 ARIMA(8,0,4)(0,0,0)[0]             : AIC=891.707, Time=0.52 sec
 ARIMA(8,0,5)(0,0,0)[0]             : AIC=694.237, Time=0.58 sec
 ARIMA(8,0,6)(0,0,0)[0]             : AIC=inf, Time=0.62 sec
 ARIMA(8,0,7)(0,0,0)[0]             : AIC=inf, Time=0.83 sec
 ARIMA(8,0,8)(0,0,0)[0]             : AIC=inf, Time=0.92 sec
 ARIMA(8,0,9)(0,0,0)[0]             : AIC=inf, Time=0.95 sec
 ARIMA(8,0,10)(0,0,0)[0]             : AIC=inf, Time=1.48 sec
 ARIMA(8,0,11)(0,0,0)[0]             : AIC=inf, Time=1.29 sec
 ARIMA(8,0,12)(0,0,0)[0]             : AIC=inf, Time=1.58 sec
 ARIMA(9,0,0)(0,0,0)[0]             : AIC=inf, Time=0.09 sec
 ARIMA(9,0,1)(0,0,0)[0]             : AIC=770.020, Time=0.34 sec
 ARIMA(9,0,2)(0,0,0)[0]             : AIC=693.097, Time=0.43 sec
 ARIMA(9,0,3)(0,0,0)[0]             : AIC=inf, Time=0.60 sec
 ARIMA(9,0,4)(0,0,0)[0]             : AIC=897.204, Time=0.48 sec
 ARIMA(9,0,5)(0,0,0)[0]             : AIC=inf, Time=0.65 sec
 ARIMA(9,0,6)(0,0,0)[0]             : AIC=inf, Time=0.75 sec
 ARIMA(9,0,7)(0,0,0)[0]             : AIC=692.589, Time=0.71 sec
 ARIMA(9,0,8)(0,0,0)[0]             : AIC=inf, Time=0.97 sec
 ARIMA(9,0,9)(0,0,0)[0]             : AIC=inf, Time=1.09 sec
 ARIMA(9,0,10)(0,0,0)[0]             : AIC=inf, Time=1.24 sec
 ARIMA(9,0,11)(0,0,0)[0]             : AIC=inf, Time=1.21 sec
 ARIMA(9,0,12)(0,0,0)[0]             : AIC=803.892, Time=1.54 sec
 ARIMA(10,0,0)(0,0,0)[0]             : AIC=inf, Time=0.38 sec
 ARIMA(10,0,1)(0,0,0)[0]             : AIC=831.568, Time=0.46 sec
 ARIMA(10,0,2)(0,0,0)[0]             : AIC=699.899, Time=0.47 sec
 ARIMA(10,0,3)(0,0,0)[0]             : AIC=688.404, Time=0.58 sec
 ARIMA(10,0,4)(0,0,0)[0]             : AIC=inf, Time=0.71 sec
 ARIMA(10,0,5)(0,0,0)[0]             : AIC=889.241, Time=0.66 sec
 ARIMA(10,0,6)(0,0,0)[0]             : AIC=inf, Time=0.85 sec
 ARIMA(10,0,7)(0,0,0)[0]             : AIC=652.507, Time=0.83 sec
 ARIMA(10,0,8)(0,0,0)[0]             : AIC=inf, Time=1.17 sec
 ARIMA(10,0,9)(0,0,0)[0]             : AIC=inf, Time=1.16 sec
 ARIMA(10,0,10)(0,0,0)[0]             : AIC=inf, Time=1.56 sec
 ARIMA(10,0,11)(0,0,0)[0]             : AIC=inf, Time=1.52 sec
 ARIMA(10,0,12)(0,0,0)[0]             : AIC=inf, Time=1.56 sec
 ARIMA(11,0,0)(0,0,0)[0]             : AIC=inf, Time=0.44 sec
 ARIMA(11,0,1)(0,0,0)[0]             : AIC=786.896, Time=0.49 sec
 ARIMA(11,0,2)(0,0,0)[0]             : AIC=inf, Time=0.77 sec
 ARIMA(11,0,3)(0,0,0)[0]             : AIC=687.914, Time=0.65 sec
 ARIMA(11,0,4)(0,0,0)[0]             : AIC=877.454, Time=0.80 sec
 ARIMA(11,0,5)(0,0,0)[0]             : AIC=824.132, Time=0.97 sec
 ARIMA(11,0,6)(0,0,0)[0]             : AIC=inf, Time=1.20 sec
 ARIMA(11,0,7)(0,0,0)[0]             : AIC=650.993, Time=1.10 sec
 ARIMA(11,0,8)(0,0,0)[0]             : AIC=inf, Time=1.27 sec
 ARIMA(11,0,9)(0,0,0)[0]             : AIC=879.540, Time=1.28 sec
 ARIMA(11,0,10)(0,0,0)[0]             : AIC=inf, Time=1.47 sec
 ARIMA(11,0,11)(0,0,0)[0]             : AIC=inf, Time=1.74 sec
 ARIMA(11,0,12)(0,0,0)[0]             : AIC=808.423, Time=1.61 sec
 ARIMA(12,0,0)(0,0,0)[0]             : AIC=inf, Time=0.50 sec
 ARIMA(12,0,1)(0,0,0)[0]             : AIC=728.603, Time=0.57 sec
 ARIMA(12,0,2)(0,0,0)[0]             : AIC=725.668, Time=0.66 sec
 ARIMA(12,0,3)(0,0,0)[0]             : AIC=706.672, Time=0.64 sec
 ARIMA(12,0,4)(0,0,0)[0]             : AIC=704.142, Time=0.70 sec
 ARIMA(12,0,5)(0,0,0)[0]             : AIC=703.286, Time=0.66 sec
 ARIMA(12,0,6)(0,0,0)[0]             : AIC=656.813, Time=0.93 sec
 ARIMA(12,0,7)(0,0,0)[0]             : AIC=650.940, Time=1.04 sec
 ARIMA(12,0,8)(0,0,0)[0]             : AIC=647.599, Time=1.11 sec
 ARIMA(12,0,9)(0,0,0)[0]             : AIC=inf, Time=1.51 sec
 ARIMA(12,0,10)(0,0,0)[0]             : AIC=inf, Time=1.45 sec
 ARIMA(12,0,11)(0,0,0)[0]             : AIC=680.574, Time=1.48 sec
 ARIMA(12,0,12)(0,0,0)[0]             : AIC=inf, Time=1.79 sec

Best model:  ARIMA(12,0,8)(0,0,0)[0]
Total fit time: 115.457 seconds
Optimal ARIMA order: (12, 0, 8)
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[42]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># create model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="n">order_arima</span><span class="p">)</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># Print model summary</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/sarimax.py:966: UserWarning:

Non-stationary starting autoregressive parameters found. Using zeros as starting parameters.

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 1.4268977642059326
                               SARIMAX Results
==============================================================================
Dep. Variable:              mean_temp   No. Observations:                  480
Model:                ARIMA(12, 0, 8)   Log Likelihood                -284.550
Date:                Thu, 15 Jun 2023   AIC                            613.099
Time:                        02:23:16   BIC                            704.923
Sample:                    01-31-1982   HQIC                           649.193
                         - 12-31-2021
Covariance Type:                  opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
const         27.6671      0.151    183.394      0.000      27.371      27.963
ar.L1          0.2012      0.200      1.005      0.315      -0.191       0.594
ar.L2          0.3249      0.195      1.666      0.096      -0.057       0.707
ar.L3         -0.2085      0.103     -2.026      0.043      -0.410      -0.007
ar.L4         -0.1540      0.082     -1.885      0.059      -0.314       0.006
ar.L5         -0.1563      0.087     -1.795      0.073      -0.327       0.014
ar.L6          0.4679      0.094      4.981      0.000       0.284       0.652
ar.L7         -0.3473      0.168     -2.071      0.038      -0.676      -0.019
ar.L8         -0.2929      0.206     -1.420      0.156      -0.697       0.111
ar.L9          0.2748      0.093      2.952      0.003       0.092       0.457
ar.L10         0.0352      0.054      0.655      0.513      -0.070       0.141
ar.L11         0.1625      0.056      2.895      0.004       0.052       0.272
ar.L12         0.3095      0.064      4.828      0.000       0.184       0.435
ma.L1          0.2800      0.203      1.379      0.168      -0.118       0.678
ma.L2         -0.0541      0.107     -0.504      0.614      -0.264       0.156
ma.L3          0.1846      0.074      2.478      0.013       0.039       0.331
ma.L4          0.3169      0.062      5.119      0.000       0.196       0.438
ma.L5          0.3882      0.072      5.379      0.000       0.247       0.530
ma.L6         -0.1597      0.086     -1.854      0.064      -0.328       0.009
ma.L7          0.5272      0.102      5.175      0.000       0.328       0.727
ma.L8          0.5830      0.177      3.296      0.001       0.236       0.930
sigma2         0.1869      0.013     14.919      0.000       0.162       0.211
===================================================================================
Ljung-Box (L1) (Q):                   1.00   Jarque-Bera (JB):                 0.27
Prob(Q):                              0.32   Prob(JB):                         0.87
Heteroskedasticity (H):               0.85   Skew:                             0.04
Prob(H) (two-sided):                  0.30   Kurtosis:                         3.09
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[43]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from auto ARIMA Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_43.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[44]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_44.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0116
Root Mean Squared Error: 0.37387541794493334
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>ARIMA(12,0,8)(0,0,0)[0]:</strong>
                    Mean Absolute Percent Error: 0.0116
                    Root Mean Squared Error: 0.37387541794493334</p>
                <p><strong>ARIMA(9,1,9)(0,0,0)[0]:</strong>
                    Mean Absolute Percent Error: 0.0136
                    Root Mean Squared Error: 0.45632291182559315</p>
                <p>The auto ARIMA chose the above 2 orders as the optimal orders, as I tried with different orders of <em>d</em>. Weirdly enough, the ARIMA without first differencing performed better than with first differencing. This shows that differencing is not always necessary or beneficial, or maybe the chosen <em>p</em> and <em>q</em> were not optimal.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Since ARIMA(12,0,8)(0,0,0)[0] did better here, let's try using RFO on ARIMA(12,0,8)(0,0,0)[0] to see if it improves the predictions.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[45]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># create the model</span>
<span class="n">predictions_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">Series</span><span class="p">(</span><span class="n">dtype</span><span class="o">=</span><span class="s1">'float64'</span><span class="p">)</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="k">for</span> <span class="n">end_date</span> <span class="ow">in</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">:</span>
    <span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">end_date</span> <span class="o">-</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">)]</span>
    <span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">8</span><span class="p">))</span>
    <span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
    <span class="n">pred</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">end_date</span><span class="p">)</span>
    <span class="n">predictions_rolling</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span> <span class="o">=</span> <span class="n">pred</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">residuals_rolling</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions_rolling</span>

<span class="c1"># print(residuals_rolling)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from auto ARIMA Model (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error_rolling</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/sarimax.py:966: UserWarning:

Non-stationary starting autoregressive parameters found. Using zeros as starting parameters.

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/sarimax.py:966: UserWarning:

Non-stationary starting autoregressive parameters found. Using zeros as starting parameters.

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/sarimax.py:966: UserWarning:

Non-stationary starting autoregressive parameters found. Using zeros as starting parameters.

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/sarimax.py:966: UserWarning:

Non-stationary starting autoregressive parameters found. Using zeros as starting parameters.

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 15.89620304107666
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_45.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[46]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions_rolling</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data_rolling</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_46.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0114
Root Mean Squared Error: 0.40277785698754665
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>Seems like with RFO, the predictions are worse than without RFO (RMSE=0.37388). Initially I thought that RFO would always perform better but I noticed that this is not always the case, especially in this scenario, when the test data is limited to 1 year, as compared to the initial 70:30 split with test data consisting of 12 years. Perhaps there is a correlation between the sample size and the variability of the data. With a smaller test set (with the 39:1 split), the evaluation of the model's performance becomes more sensitive to individual data points, which can lead to more variability in the results. On the other hand, despite its RMSE being higher, the RFO version's graph has a shape closer to the test data, compared to the non-RFO version.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h4 id="Auto-SARIMA" data-toc-modified-id="Auto-SARIMA-1.0.6.2"><a class="toc-mod-link" id="Auto-SARIMA-1.0.6.2"></a><span class="toc-item-num">1.0.6.2&nbsp;&nbsp;</span>Auto SARIMA<a class="anchor-link" href="#Auto-SARIMA">¶</a></h4>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[47]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split to test 1 year of data as splitting 70:30 takes very long</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2022</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>

<span class="c1"># Find optimal SARIMA order using auto_arima</span>
<span class="n">model_sarima</span> <span class="o">=</span> <span class="n">auto_arima</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">,</span> <span class="n">d</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">max_d</span><span class="o">=</span><span class="mi">3</span><span class="p">,</span> <span class="n">max_D</span><span class="o">=</span><span class="mi">3</span><span class="p">,</span> <span class="n">max_p</span><span class="o">=</span><span class="mi">12</span><span class="p">,</span> <span class="n">max_q</span><span class="o">=</span><span class="mi">12</span><span class="p">,</span> <span class="n">max_P</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">max_Q</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">max_order</span><span class="o">=</span><span class="mi">26</span><span class="p">,</span> <span class="n">parallel</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">num_cores</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">seasonal</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">m</span><span class="o">=</span><span class="mi">12</span><span class="p">,</span> <span class="n">information_criterion</span><span class="o">=</span><span class="s1">'aic'</span><span class="p">,</span> <span class="n">trace</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">stepwise</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>

<span class="c1"># Get the best SARIMA order</span>
<span class="n">normal_order</span> <span class="o">=</span> <span class="n">model_sarima</span><span class="o">.</span><span class="n">order</span>
<span class="n">seasonal_order</span> <span class="o">=</span> <span class="n">model_sarima</span><span class="o">.</span><span class="n">seasonal_order</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Optimal SARIMA order:"</span><span class="p">,</span> <span class="n">normal_order</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Optimal SARIMA seasonal order:"</span><span class="p">,</span> <span class="n">seasonal_order</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre> ARIMA(0,1,0)(0,0,0)[12] intercept   : AIC=913.330, Time=0.02 sec
 ARIMA(0,1,0)(0,0,1)[12] intercept   : AIC=851.187, Time=0.08 sec
 ARIMA(0,1,0)(1,0,0)[12] intercept   : AIC=827.111, Time=0.06 sec
 ARIMA(0,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=0.40 sec
 ARIMA(0,1,1)(0,0,0)[12] intercept   : AIC=914.480, Time=0.03 sec
 ARIMA(0,1,1)(0,0,1)[12] intercept   : AIC=840.119, Time=0.10 sec
 ARIMA(0,1,1)(1,0,0)[12] intercept   : AIC=787.031, Time=0.09 sec
 ARIMA(0,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=0.50 sec
 ARIMA(0,1,2)(0,0,0)[12] intercept   : AIC=914.540, Time=0.04 sec
 ARIMA(0,1,2)(0,0,1)[12] intercept   : AIC=842.027, Time=0.12 sec
 ARIMA(0,1,2)(1,0,0)[12] intercept   : AIC=783.875, Time=0.14 sec
 ARIMA(0,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=0.68 sec
 ARIMA(0,1,3)(0,0,0)[12] intercept   : AIC=inf, Time=0.32 sec
 ARIMA(0,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=0.77 sec
 ARIMA(0,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=0.45 sec
 ARIMA(0,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=0.90 sec
 ARIMA(0,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.30 sec
 ARIMA(0,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=0.74 sec
 ARIMA(0,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=0.52 sec
 ARIMA(0,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=1.47 sec
 ARIMA(0,1,5)(0,0,0)[12] intercept   : AIC=inf, Time=0.22 sec
 ARIMA(0,1,5)(0,0,1)[12] intercept   : AIC=745.118, Time=0.93 sec
 ARIMA(0,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=0.65 sec
 ARIMA(0,1,5)(1,0,1)[12] intercept   : AIC=621.531, Time=1.06 sec
 ARIMA(0,1,6)(0,0,0)[12] intercept   : AIC=inf, Time=0.38 sec
 ARIMA(0,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.01 sec
 ARIMA(0,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=0.63 sec
 ARIMA(0,1,6)(1,0,1)[12] intercept   : AIC=620.483, Time=1.26 sec
 ARIMA(0,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=0.49 sec
 ARIMA(0,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=1.30 sec
 ARIMA(0,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=0.70 sec
 ARIMA(0,1,7)(1,0,1)[12] intercept   : AIC=637.966, Time=1.54 sec
 ARIMA(0,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.56 sec
 ARIMA(0,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=1.57 sec
 ARIMA(0,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=0.75 sec
 ARIMA(0,1,8)(1,0,1)[12] intercept   : AIC=641.732, Time=1.65 sec
 ARIMA(0,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=0.66 sec
 ARIMA(0,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=1.86 sec
 ARIMA(0,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=0.85 sec
 ARIMA(0,1,9)(1,0,1)[12] intercept   : AIC=621.069, Time=2.11 sec
 ARIMA(0,1,10)(0,0,0)[12] intercept   : AIC=790.067, Time=0.72 sec
 ARIMA(0,1,10)(0,0,1)[12] intercept   : AIC=745.570, Time=1.93 sec
 ARIMA(0,1,10)(1,0,0)[12] intercept   : AIC=722.375, Time=0.91 sec
 ARIMA(0,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=2.08 sec
 ARIMA(0,1,11)(0,0,0)[12] intercept   : AIC=791.484, Time=0.87 sec
 ARIMA(0,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=2.39 sec
 ARIMA(0,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=0.99 sec
 ARIMA(0,1,11)(1,0,1)[12] intercept   : AIC=645.897, Time=2.55 sec
 ARIMA(1,1,0)(0,0,0)[12] intercept   : AIC=914.383, Time=0.02 sec
 ARIMA(1,1,0)(0,0,1)[12] intercept   : AIC=839.475, Time=0.08 sec
 ARIMA(1,1,0)(1,0,0)[12] intercept   : AIC=792.132, Time=0.10 sec
 ARIMA(1,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=0.47 sec
 ARIMA(1,1,1)(0,0,0)[12] intercept   : AIC=911.145, Time=0.09 sec
 ARIMA(1,1,1)(0,0,1)[12] intercept   : AIC=840.203, Time=0.19 sec
 ARIMA(1,1,1)(1,0,0)[12] intercept   : AIC=inf, Time=0.40 sec
 ARIMA(1,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=0.76 sec
 ARIMA(1,1,2)(0,0,0)[12] intercept   : AIC=inf, Time=0.21 sec
 ARIMA(1,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=0.56 sec
 ARIMA(1,1,2)(1,0,0)[12] intercept   : AIC=729.216, Time=0.48 sec
 ARIMA(1,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=0.81 sec
 ARIMA(1,1,3)(0,0,0)[12] intercept   : AIC=inf, Time=0.27 sec
 ARIMA(1,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=0.78 sec
 ARIMA(1,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=0.64 sec
 ARIMA(1,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=0.83 sec
 ARIMA(1,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.35 sec
 ARIMA(1,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=0.87 sec
 ARIMA(1,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=0.68 sec
 ARIMA(1,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=1.03 sec
 ARIMA(1,1,5)(0,0,0)[12] intercept   : AIC=inf, Time=0.43 sec
 ARIMA(1,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=1.09 sec
 ARIMA(1,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=0.75 sec
 ARIMA(1,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=1.24 sec
 ARIMA(1,1,6)(0,0,0)[12] intercept   : AIC=809.432, Time=0.45 sec
 ARIMA(1,1,6)(0,0,1)[12] intercept   : AIC=746.983, Time=1.23 sec
 ARIMA(1,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=0.79 sec
 ARIMA(1,1,6)(1,0,1)[12] intercept   : AIC=655.406, Time=1.26 sec
 ARIMA(1,1,7)(0,0,0)[12] intercept   : AIC=794.442, Time=0.55 sec
 ARIMA(1,1,7)(0,0,1)[12] intercept   : AIC=741.578, Time=1.49 sec
 ARIMA(1,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=0.84 sec
 ARIMA(1,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=1.74 sec
 ARIMA(1,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.34 sec
 ARIMA(1,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=0.95 sec
 ARIMA(1,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=0.54 sec
 ARIMA(1,1,8)(1,0,1)[12] intercept   : AIC=inf, Time=1.75 sec
 ARIMA(1,1,9)(0,0,0)[12] intercept   : AIC=792.204, Time=0.75 sec
 ARIMA(1,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.04 sec
 ARIMA(1,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=1.03 sec
 ARIMA(1,1,9)(1,0,1)[12] intercept   : AIC=662.790, Time=2.10 sec
 ARIMA(1,1,10)(0,0,0)[12] intercept   : AIC=792.736, Time=0.86 sec
 ARIMA(1,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=2.11 sec
 ARIMA(1,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=1.07 sec
 ARIMA(1,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=2.46 sec
 ARIMA(1,1,11)(0,0,0)[12] intercept   : AIC=797.779, Time=0.95 sec
 ARIMA(1,1,11)(0,0,1)[12] intercept   : AIC=750.148, Time=2.50 sec
 ARIMA(1,1,11)(1,0,0)[12] intercept   : AIC=725.236, Time=1.15 sec
 ARIMA(1,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=2.77 sec
 ARIMA(2,1,0)(0,0,0)[12] intercept   : AIC=914.550, Time=0.03 sec
 ARIMA(2,1,0)(0,0,1)[12] intercept   : AIC=841.032, Time=0.10 sec
 ARIMA(2,1,0)(1,0,0)[12] intercept   : AIC=792.866, Time=0.14 sec
 ARIMA(2,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=0.53 sec
 ARIMA(2,1,1)(0,0,0)[12] intercept   : AIC=913.915, Time=0.08 sec
 ARIMA(2,1,1)(0,0,1)[12] intercept   : AIC=841.986, Time=0.22 sec
 ARIMA(2,1,1)(1,0,0)[12] intercept   : AIC=inf, Time=0.62 sec
 ARIMA(2,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=0.65 sec
 ARIMA(2,1,2)(0,0,0)[12] intercept   : AIC=915.619, Time=0.14 sec
 ARIMA(2,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=0.72 sec
 ARIMA(2,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=0.75 sec
 ARIMA(2,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=1.45 sec
 ARIMA(2,1,3)(0,0,0)[12] intercept   : AIC=inf, Time=0.32 sec
 ARIMA(2,1,3)(0,0,1)[12] intercept   : AIC=765.741, Time=0.81 sec
 ARIMA(2,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=0.77 sec
 ARIMA(2,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=0.85 sec
 ARIMA(2,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.36 sec
 ARIMA(2,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=0.98 sec
 ARIMA(2,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=0.83 sec
 ARIMA(2,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=1.09 sec
 ARIMA(2,1,5)(0,0,0)[12] intercept   : AIC=inf, Time=0.44 sec
 ARIMA(2,1,5)(0,0,1)[12] intercept   : AIC=745.141, Time=1.14 sec
 ARIMA(2,1,5)(1,0,0)[12] intercept   : AIC=723.429, Time=0.83 sec
 ARIMA(2,1,5)(1,0,1)[12] intercept   : AIC=655.886, Time=1.33 sec
 ARIMA(2,1,6)(0,0,0)[12] intercept   : AIC=796.767, Time=0.47 sec
 ARIMA(2,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.30 sec
 ARIMA(2,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=1.08 sec
 ARIMA(2,1,6)(1,0,1)[12] intercept   : AIC=inf, Time=1.59 sec
 ARIMA(2,1,7)(0,0,0)[12] intercept   : AIC=791.479, Time=0.56 sec
 ARIMA(2,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=1.59 sec
 ARIMA(2,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=1.02 sec
 ARIMA(2,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=1.97 sec
 ARIMA(2,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.70 sec
 ARIMA(2,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=1.73 sec
 ARIMA(2,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=1.14 sec
 ARIMA(2,1,8)(1,0,1)[12] intercept   : AIC=inf, Time=1.81 sec
 ARIMA(2,1,9)(0,0,0)[12] intercept   : AIC=801.402, Time=0.75 sec
 ARIMA(2,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.12 sec
 ARIMA(2,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=1.16 sec
 ARIMA(2,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=2.24 sec
 ARIMA(2,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=0.95 sec
 ARIMA(2,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=2.50 sec
 ARIMA(2,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=1.39 sec
 ARIMA(2,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=2.55 sec
 ARIMA(2,1,11)(0,0,0)[12] intercept   : AIC=762.627, Time=1.03 sec
 ARIMA(2,1,11)(0,0,1)[12] intercept   : AIC=739.456, Time=2.72 sec
 ARIMA(2,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=1.32 sec
 ARIMA(2,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=2.78 sec
 ARIMA(3,1,0)(0,0,0)[12] intercept   : AIC=908.391, Time=0.05 sec
 ARIMA(3,1,0)(0,0,1)[12] intercept   : AIC=838.115, Time=0.12 sec
 ARIMA(3,1,0)(1,0,0)[12] intercept   : AIC=791.124, Time=0.16 sec
 ARIMA(3,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=0.66 sec
 ARIMA(3,1,1)(0,0,0)[12] intercept   : AIC=inf, Time=0.25 sec
 ARIMA(3,1,1)(0,0,1)[12] intercept   : AIC=inf, Time=0.72 sec
 ARIMA(3,1,1)(1,0,0)[12] intercept   : AIC=inf, Time=0.66 sec
 ARIMA(3,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=0.71 sec
 ARIMA(3,1,2)(0,0,0)[12] intercept   : AIC=805.415, Time=0.29 sec
 ARIMA(3,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=0.70 sec
 ARIMA(3,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=0.80 sec
 ARIMA(3,1,2)(1,0,1)[12] intercept   : AIC=620.834, Time=0.79 sec
 ARIMA(3,1,3)(0,0,0)[12] intercept   : AIC=inf, Time=0.35 sec
 ARIMA(3,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=0.83 sec
 ARIMA(3,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=0.76 sec
 ARIMA(3,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=1.28 sec
 ARIMA(3,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.34 sec
 ARIMA(3,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=1.22 sec
 ARIMA(3,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=0.95 sec
 ARIMA(3,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=1.11 sec
 ARIMA(3,1,5)(0,0,0)[12] intercept   : AIC=684.351, Time=0.45 sec
 ARIMA(3,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=1.37 sec
 ARIMA(3,1,5)(1,0,0)[12] intercept   : AIC=683.616, Time=0.98 sec
 ARIMA(3,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=1.41 sec
 ARIMA(3,1,6)(0,0,0)[12] intercept   : AIC=inf, Time=0.57 sec
 ARIMA(3,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.32 sec
 ARIMA(3,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=1.11 sec
 ARIMA(3,1,6)(1,0,1)[12] intercept   : AIC=648.558, Time=1.60 sec
 ARIMA(3,1,7)(0,0,0)[12] intercept   : AIC=792.975, Time=0.60 sec
 ARIMA(3,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=1.73 sec
 ARIMA(3,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=1.01 sec
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/pmdarima/arima/_auto_solvers.py:524: ModelFitWarning:

Error fitting  ARIMA(3,1,7)(1,0,1)[12] intercept (if you do not want to see these warnings, run with error_action="ignore").
Traceback:
Traceback (most recent call last):
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/pmdarima/arima/_auto_solvers.py", line 508, in _fit_candidate_model
    fit.fit(y, X=X, **fit_params)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/pmdarima/arima/arima.py", line 603, in fit
    self._fit(y, X, **fit_args)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/pmdarima/arima/arima.py", line 524, in _fit
    fit, self.arima_res_ = _fit_wrapper()
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/pmdarima/arima/arima.py", line 510, in _fit_wrapper
    fitted = arima.fit(
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/mlemodel.py", line 704, in fit
    mlefit = super(MLEModel, self).fit(start_params, method=method,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py", line 566, in fit
    xopt, retvals, optim_settings = optimizer._fit(f, score, start_params,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/optimizer.py", line 242, in _fit
    xopt, retvals = func(objective, gradient, start_params, fargs, kwargs,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/optimizer.py", line 659, in _fit_lbfgs
    retvals = optimize.fmin_l_bfgs_b(func, start_params, maxiter=maxiter,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_lbfgsb_py.py", line 197, in fmin_l_bfgs_b
    res = _minimize_lbfgsb(fun, x0, args=args, jac=jac, bounds=bounds,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_lbfgsb_py.py", line 359, in _minimize_lbfgsb
    f, g = func_and_grad(x)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_differentiable_functions.py", line 286, in fun_and_grad
    self._update_grad()
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_differentiable_functions.py", line 256, in _update_grad
    self._update_grad_impl()
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_differentiable_functions.py", line 173, in update_grad
    self.g = approx_derivative(fun_wrapped, self.x, f0=self.f,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_numdiff.py", line 505, in approx_derivative
    return _dense_difference(fun_wrapped, x0, f0, h,
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_numdiff.py", line 576, in _dense_difference
    df = fun(x) - f0
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_numdiff.py", line 456, in fun_wrapped
    f = np.atleast_1d(fun(x, *args, **kwargs))
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/scipy/optimize/_differentiable_functions.py", line 137, in fun_wrapped
    fx = fun(np.copy(x), *args)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py", line 534, in f
    return -self.loglike(params, *args) / nobs
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/mlemodel.py", line 939, in loglike
    loglike = self.ssm.loglike(complex_step=complex_step, **kwargs)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/kalman_filter.py", line 1001, in loglike
    kfilter = self._filter(**kwargs)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/kalman_filter.py", line 921, in _filter
    self._initialize_state(prefix=prefix, complex_step=complex_step)
  File "/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/tsa/statespace/representation.py", line 1058, in _initialize_state
    self._statespaces[prefix].initialize(self.initialization,
  File "statsmodels/tsa/statespace/_representation.pyx", line 1373, in statsmodels.tsa.statespace._representation.dStatespace.initialize
  File "statsmodels/tsa/statespace/_representation.pyx", line 1362, in statsmodels.tsa.statespace._representation.dStatespace.initialize
  File "statsmodels/tsa/statespace/_initialization.pyx", line 288, in statsmodels.tsa.statespace._initialization.dInitialization.initialize
  File "statsmodels/tsa/statespace/_initialization.pyx", line 406, in statsmodels.tsa.statespace._initialization.dInitialization.initialize_stationary_stationary_cov
  File "statsmodels/tsa/statespace/_tools.pyx", line 1525, in statsmodels.tsa.statespace._tools._dsolve_discrete_lyapunov
numpy.linalg.LinAlgError: LU decomposition error.


</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre> ARIMA(3,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=nan sec
 ARIMA(3,1,8)(0,0,0)[12] intercept   : AIC=794.679, Time=0.68 sec
 ARIMA(3,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=1.92 sec
 ARIMA(3,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=1.18 sec
 ARIMA(3,1,8)(1,0,1)[12] intercept   : AIC=inf, Time=2.21 sec
 ARIMA(3,1,9)(0,0,0)[12] intercept   : AIC=748.471, Time=0.92 sec
 ARIMA(3,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.53 sec
 ARIMA(3,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=1.65 sec
 ARIMA(3,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=2.61 sec
 ARIMA(3,1,10)(0,0,0)[12] intercept   : AIC=763.290, Time=0.94 sec
 ARIMA(3,1,10)(0,0,1)[12] intercept   : AIC=749.514, Time=2.50 sec
 ARIMA(3,1,10)(1,0,0)[12] intercept   : AIC=732.901, Time=1.28 sec
 ARIMA(3,1,10)(1,0,1)[12] intercept   : AIC=692.967, Time=2.58 sec
 ARIMA(3,1,11)(0,0,0)[12] intercept   : AIC=760.981, Time=1.06 sec
 ARIMA(3,1,11)(0,0,1)[12] intercept   : AIC=725.232, Time=2.86 sec
 ARIMA(3,1,11)(1,0,0)[12] intercept   : AIC=716.822, Time=1.36 sec
 ARIMA(3,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=3.21 sec
 ARIMA(4,1,0)(0,0,0)[12] intercept   : AIC=901.225, Time=0.05 sec
 ARIMA(4,1,0)(0,0,1)[12] intercept   : AIC=831.554, Time=0.14 sec
 ARIMA(4,1,0)(1,0,0)[12] intercept   : AIC=786.667, Time=0.21 sec
 ARIMA(4,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=0.84 sec
 ARIMA(4,1,1)(0,0,0)[12] intercept   : AIC=inf, Time=0.29 sec
 ARIMA(4,1,1)(0,0,1)[12] intercept   : AIC=inf, Time=0.75 sec
 ARIMA(4,1,1)(1,0,0)[12] intercept   : AIC=718.175, Time=0.85 sec
 ARIMA(4,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=1.02 sec
 ARIMA(4,1,2)(0,0,0)[12] intercept   : AIC=inf, Time=0.37 sec
 ARIMA(4,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=0.76 sec
 ARIMA(4,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=0.90 sec
 ARIMA(4,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=1.04 sec
 ARIMA(4,1,3)(0,0,0)[12] intercept   : AIC=inf, Time=0.37 sec
 ARIMA(4,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=0.94 sec
 ARIMA(4,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=1.04 sec
 ARIMA(4,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=1.12 sec
 ARIMA(4,1,4)(0,0,0)[12] intercept   : AIC=781.377, Time=0.52 sec
 ARIMA(4,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=1.21 sec
 ARIMA(4,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=1.11 sec
 ARIMA(4,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=1.34 sec
 ARIMA(4,1,5)(0,0,0)[12] intercept   : AIC=inf, Time=0.61 sec
 ARIMA(4,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=1.47 sec
 ARIMA(4,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=1.31 sec
 ARIMA(4,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=1.82 sec
 ARIMA(4,1,6)(0,0,0)[12] intercept   : AIC=704.823, Time=0.60 sec
 ARIMA(4,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.49 sec
 ARIMA(4,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=1.33 sec
 ARIMA(4,1,6)(1,0,1)[12] intercept   : AIC=672.323, Time=1.60 sec
 ARIMA(4,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=0.76 sec
 ARIMA(4,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=1.98 sec
 ARIMA(4,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=1.31 sec
 ARIMA(4,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=2.04 sec
 ARIMA(4,1,8)(0,0,0)[12] intercept   : AIC=724.929, Time=0.76 sec
 ARIMA(4,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=2.04 sec
 ARIMA(4,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=1.37 sec
 ARIMA(4,1,8)(1,0,1)[12] intercept   : AIC=inf, Time=2.21 sec
 ARIMA(4,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=1.04 sec
 ARIMA(4,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.75 sec
 ARIMA(4,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=1.55 sec
 ARIMA(4,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=2.52 sec
 ARIMA(4,1,10)(0,0,0)[12] intercept   : AIC=752.403, Time=0.96 sec
 ARIMA(4,1,10)(0,0,1)[12] intercept   : AIC=720.470, Time=2.45 sec
 ARIMA(4,1,10)(1,0,0)[12] intercept   : AIC=722.118, Time=1.60 sec
 ARIMA(4,1,10)(1,0,1)[12] intercept   : AIC=715.654, Time=2.59 sec
 ARIMA(4,1,11)(0,0,0)[12] intercept   : AIC=750.029, Time=1.15 sec
 ARIMA(4,1,11)(0,0,1)[12] intercept   : AIC=719.624, Time=2.92 sec
 ARIMA(4,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=1.74 sec
 ARIMA(4,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=3.16 sec
 ARIMA(5,1,0)(0,0,0)[12] intercept   : AIC=882.132, Time=0.08 sec
 ARIMA(5,1,0)(0,0,1)[12] intercept   : AIC=812.431, Time=0.17 sec
 ARIMA(5,1,0)(1,0,0)[12] intercept   : AIC=770.046, Time=0.26 sec
 ARIMA(5,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=0.88 sec
 ARIMA(5,1,1)(0,0,0)[12] intercept   : AIC=inf, Time=0.35 sec
 ARIMA(5,1,1)(0,0,1)[12] intercept   : AIC=inf, Time=0.79 sec
 ARIMA(5,1,1)(1,0,0)[12] intercept   : AIC=inf, Time=0.96 sec
 ARIMA(5,1,1)(1,0,1)[12] intercept   : AIC=617.039, Time=1.14 sec
 ARIMA(5,1,2)(0,0,0)[12] intercept   : AIC=inf, Time=0.38 sec
 ARIMA(5,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=0.92 sec
 ARIMA(5,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=1.05 sec
 ARIMA(5,1,2)(1,0,1)[12] intercept   : AIC=630.996, Time=1.16 sec
 ARIMA(5,1,3)(0,0,0)[12] intercept   : AIC=798.044, Time=0.46 sec
 ARIMA(5,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=1.02 sec
 ARIMA(5,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=1.14 sec
 ARIMA(5,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=1.33 sec
 ARIMA(5,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.49 sec
 ARIMA(5,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=1.22 sec
 ARIMA(5,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=1.22 sec
 ARIMA(5,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=1.38 sec
 ARIMA(5,1,5)(0,0,0)[12] intercept   : AIC=inf, Time=0.62 sec
 ARIMA(5,1,5)(0,0,1)[12] intercept   : AIC=671.550, Time=1.53 sec
 ARIMA(5,1,5)(1,0,0)[12] intercept   : AIC=673.467, Time=1.43 sec
 ARIMA(5,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=1.84 sec
 ARIMA(5,1,6)(0,0,0)[12] intercept   : AIC=715.714, Time=0.62 sec
 ARIMA(5,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.71 sec
 ARIMA(5,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=1.42 sec
 ARIMA(5,1,6)(1,0,1)[12] intercept   : AIC=652.848, Time=1.76 sec
 ARIMA(5,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=0.74 sec
 ARIMA(5,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=1.91 sec
 ARIMA(5,1,7)(1,0,0)[12] intercept   : AIC=662.685, Time=1.62 sec
 ARIMA(5,1,7)(1,0,1)[12] intercept   : AIC=654.640, Time=2.10 sec
 ARIMA(5,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.87 sec
 ARIMA(5,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=2.22 sec
 ARIMA(5,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=1.66 sec
 ARIMA(5,1,8)(1,0,1)[12] intercept   : AIC=673.328, Time=2.15 sec
 ARIMA(5,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=1.00 sec
 ARIMA(5,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.67 sec
 ARIMA(5,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=1.79 sec
 ARIMA(5,1,9)(1,0,1)[12] intercept   : AIC=654.459, Time=2.52 sec
 ARIMA(5,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=0.93 sec
 ARIMA(5,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=2.72 sec
 ARIMA(5,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=1.71 sec
 ARIMA(5,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=3.23 sec
 ARIMA(5,1,11)(0,0,0)[12] intercept   : AIC=684.697, Time=1.41 sec
 ARIMA(5,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=3.52 sec
 ARIMA(5,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=2.13 sec
 ARIMA(5,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=3.61 sec
 ARIMA(6,1,0)(0,0,0)[12] intercept   : AIC=866.307, Time=0.10 sec
 ARIMA(6,1,0)(0,0,1)[12] intercept   : AIC=797.232, Time=0.19 sec
 ARIMA(6,1,0)(1,0,0)[12] intercept   : AIC=755.122, Time=0.34 sec
 ARIMA(6,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=1.17 sec
 ARIMA(6,1,1)(0,0,0)[12] intercept   : AIC=782.550, Time=0.47 sec
 ARIMA(6,1,1)(0,0,1)[12] intercept   : AIC=inf, Time=0.87 sec
 ARIMA(6,1,1)(1,0,0)[12] intercept   : AIC=719.431, Time=1.30 sec
 ARIMA(6,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=1.29 sec
 ARIMA(6,1,2)(0,0,0)[12] intercept   : AIC=inf, Time=0.60 sec
 ARIMA(6,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=0.98 sec
 ARIMA(6,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=1.39 sec
 ARIMA(6,1,2)(1,0,1)[12] intercept   : AIC=629.185, Time=1.41 sec
 ARIMA(6,1,3)(0,0,0)[12] intercept   : AIC=790.495, Time=0.54 sec
 ARIMA(6,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=1.10 sec
 ARIMA(6,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=1.42 sec
 ARIMA(6,1,3)(1,0,1)[12] intercept   : AIC=630.265, Time=1.55 sec
 ARIMA(6,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.56 sec
 ARIMA(6,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=1.33 sec
 ARIMA(6,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=1.49 sec
 ARIMA(6,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=2.06 sec
 ARIMA(6,1,5)(0,0,0)[12] intercept   : AIC=683.715, Time=0.68 sec
 ARIMA(6,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=1.58 sec
 ARIMA(6,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=1.74 sec
 ARIMA(6,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=1.87 sec
 ARIMA(6,1,6)(0,0,0)[12] intercept   : AIC=inf, Time=0.77 sec
 ARIMA(6,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.95 sec
 ARIMA(6,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=1.94 sec
 ARIMA(6,1,6)(1,0,1)[12] intercept   : AIC=inf, Time=1.99 sec
 ARIMA(6,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=0.79 sec
 ARIMA(6,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=2.12 sec
 ARIMA(6,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=2.25 sec
 ARIMA(6,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=2.55 sec
 ARIMA(6,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.90 sec
 ARIMA(6,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=2.30 sec
 ARIMA(6,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=1.95 sec
 ARIMA(6,1,8)(1,0,1)[12] intercept   : AIC=654.284, Time=2.36 sec
 ARIMA(6,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=1.11 sec
 ARIMA(6,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.69 sec
 ARIMA(6,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=2.08 sec
 ARIMA(6,1,9)(1,0,1)[12] intercept   : AIC=646.897, Time=2.84 sec
 ARIMA(6,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=1.05 sec
 ARIMA(6,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=2.82 sec
 ARIMA(6,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=2.10 sec
 ARIMA(6,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=2.93 sec
 ARIMA(6,1,11)(0,0,0)[12] intercept   : AIC=685.835, Time=1.25 sec
 ARIMA(6,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=3.39 sec
 ARIMA(6,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=2.30 sec
 ARIMA(6,1,11)(1,0,1)[12] intercept   : AIC=671.236, Time=3.79 sec
 ARIMA(7,1,0)(0,0,0)[12] intercept   : AIC=851.615, Time=0.09 sec
 ARIMA(7,1,0)(0,0,1)[12] intercept   : AIC=792.018, Time=0.23 sec
 ARIMA(7,1,0)(1,0,0)[12] intercept   : AIC=755.568, Time=0.47 sec
 ARIMA(7,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=1.41 sec
 ARIMA(7,1,1)(0,0,0)[12] intercept   : AIC=777.421, Time=0.28 sec
 ARIMA(7,1,1)(0,0,1)[12] intercept   : AIC=inf, Time=0.99 sec
 ARIMA(7,1,1)(1,0,0)[12] intercept   : AIC=inf, Time=1.38 sec
 ARIMA(7,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=1.54 sec
 ARIMA(7,1,2)(0,0,0)[12] intercept   : AIC=728.293, Time=0.49 sec
 ARIMA(7,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=1.06 sec
 ARIMA(7,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=1.46 sec
 ARIMA(7,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=1.70 sec
 ARIMA(7,1,3)(0,0,0)[12] intercept   : AIC=inf, Time=0.53 sec
 ARIMA(7,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=1.25 sec
 ARIMA(7,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=1.47 sec
 ARIMA(7,1,3)(1,0,1)[12] intercept   : AIC=633.839, Time=1.72 sec
 ARIMA(7,1,4)(0,0,0)[12] intercept   : AIC=790.843, Time=0.62 sec
 ARIMA(7,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=1.40 sec
 ARIMA(7,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=1.56 sec
 ARIMA(7,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=2.15 sec
 ARIMA(7,1,5)(0,0,0)[12] intercept   : AIC=685.926, Time=0.69 sec
 ARIMA(7,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=1.85 sec
 ARIMA(7,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=1.84 sec
 ARIMA(7,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=2.11 sec
 ARIMA(7,1,6)(0,0,0)[12] intercept   : AIC=inf, Time=0.80 sec
 ARIMA(7,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.87 sec
 ARIMA(7,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=2.06 sec
 ARIMA(7,1,6)(1,0,1)[12] intercept   : AIC=inf, Time=2.10 sec
 ARIMA(7,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=1.05 sec
 ARIMA(7,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=2.48 sec
 ARIMA(7,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=2.21 sec
 ARIMA(7,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=2.73 sec
 ARIMA(7,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.98 sec
 ARIMA(7,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=2.36 sec
 ARIMA(7,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=2.08 sec
 ARIMA(7,1,8)(1,0,1)[12] intercept   : AIC=inf, Time=2.73 sec
 ARIMA(7,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=1.12 sec
 ARIMA(7,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=2.83 sec
 ARIMA(7,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=2.05 sec
 ARIMA(7,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=2.95 sec
 ARIMA(7,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=1.09 sec
 ARIMA(7,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=2.96 sec
 ARIMA(7,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=2.12 sec
 ARIMA(7,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=3.18 sec
 ARIMA(7,1,11)(0,0,0)[12] intercept   : AIC=inf, Time=1.38 sec
 ARIMA(7,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=3.86 sec
 ARIMA(7,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=2.33 sec
 ARIMA(7,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=3.90 sec
 ARIMA(8,1,0)(0,0,0)[12] intercept   : AIC=827.102, Time=0.14 sec
 ARIMA(8,1,0)(0,0,1)[12] intercept   : AIC=782.311, Time=0.23 sec
 ARIMA(8,1,0)(1,0,0)[12] intercept   : AIC=756.116, Time=0.52 sec
 ARIMA(8,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=1.63 sec
 ARIMA(8,1,1)(0,0,0)[12] intercept   : AIC=760.506, Time=0.29 sec
 ARIMA(8,1,1)(0,0,1)[12] intercept   : AIC=744.676, Time=0.60 sec
 ARIMA(8,1,1)(1,0,0)[12] intercept   : AIC=738.374, Time=1.05 sec
 ARIMA(8,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=1.88 sec
 ARIMA(8,1,2)(0,0,0)[12] intercept   : AIC=673.124, Time=0.62 sec
 ARIMA(8,1,2)(0,0,1)[12] intercept   : AIC=672.572, Time=1.12 sec
 ARIMA(8,1,2)(1,0,0)[12] intercept   : AIC=inf, Time=1.89 sec
 ARIMA(8,1,2)(1,0,1)[12] intercept   : AIC=646.525, Time=1.38 sec
 ARIMA(8,1,3)(0,0,0)[12] intercept   : AIC=679.062, Time=0.82 sec
 ARIMA(8,1,3)(0,0,1)[12] intercept   : AIC=inf, Time=1.35 sec
 ARIMA(8,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=1.74 sec
 ARIMA(8,1,3)(1,0,1)[12] intercept   : AIC=645.372, Time=2.42 sec
 ARIMA(8,1,4)(0,0,0)[12] intercept   : AIC=inf, Time=0.78 sec
 ARIMA(8,1,4)(0,0,1)[12] intercept   : AIC=inf, Time=1.46 sec
 ARIMA(8,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=1.90 sec
 ARIMA(8,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=2.15 sec
 ARIMA(8,1,5)(0,0,0)[12] intercept   : AIC=683.853, Time=0.88 sec
 ARIMA(8,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=2.02 sec
 ARIMA(8,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=2.39 sec
 ARIMA(8,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=2.85 sec
 ARIMA(8,1,6)(0,0,0)[12] intercept   : AIC=inf, Time=0.84 sec
 ARIMA(8,1,6)(0,0,1)[12] intercept   : AIC=inf, Time=1.80 sec
 ARIMA(8,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=2.25 sec
 ARIMA(8,1,6)(1,0,1)[12] intercept   : AIC=inf, Time=2.30 sec
 ARIMA(8,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=0.98 sec
 ARIMA(8,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=2.68 sec
 ARIMA(8,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=2.64 sec
 ARIMA(8,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=2.79 sec
 ARIMA(8,1,8)(0,0,0)[12] intercept   : AIC=inf, Time=0.99 sec
 ARIMA(8,1,8)(0,0,1)[12] intercept   : AIC=inf, Time=2.89 sec
 ARIMA(8,1,8)(1,0,0)[12] intercept   : AIC=inf, Time=2.62 sec
 ARIMA(8,1,8)(1,0,1)[12] intercept   : AIC=inf, Time=2.71 sec
 ARIMA(8,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=1.09 sec
 ARIMA(8,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=3.03 sec
 ARIMA(8,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=2.46 sec
 ARIMA(8,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=3.41 sec
 ARIMA(8,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=1.25 sec
 ARIMA(8,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=2.81 sec
 ARIMA(8,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=2.60 sec
 ARIMA(8,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=3.12 sec
 ARIMA(8,1,11)(0,0,0)[12] intercept   : AIC=inf, Time=1.51 sec
 ARIMA(8,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=3.84 sec
 ARIMA(8,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=2.79 sec
 ARIMA(8,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=3.75 sec
 ARIMA(9,1,0)(0,0,0)[12] intercept   : AIC=773.541, Time=0.16 sec
 ARIMA(9,1,0)(0,0,1)[12] intercept   : AIC=754.485, Time=0.27 sec
 ARIMA(9,1,0)(1,0,0)[12] intercept   : AIC=746.149, Time=0.62 sec
 ARIMA(9,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=1.80 sec
 ARIMA(9,1,1)(0,0,0)[12] intercept   : AIC=734.048, Time=0.33 sec
 ARIMA(9,1,1)(0,0,1)[12] intercept   : AIC=728.608, Time=0.58 sec
 ARIMA(9,1,1)(1,0,0)[12] intercept   : AIC=726.702, Time=0.96 sec
 ARIMA(9,1,1)(1,0,1)[12] intercept   : AIC=634.863, Time=1.97 sec
 ARIMA(9,1,2)(0,0,0)[12] intercept   : AIC=690.819, Time=0.75 sec
 ARIMA(9,1,2)(0,0,1)[12] intercept   : AIC=677.889, Time=1.30 sec
 ARIMA(9,1,2)(1,0,0)[12] intercept   : AIC=682.616, Time=1.87 sec
 ARIMA(9,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=2.10 sec
 ARIMA(9,1,3)(0,0,0)[12] intercept   : AIC=672.399, Time=0.81 sec
 ARIMA(9,1,3)(0,0,1)[12] intercept   : AIC=662.409, Time=1.44 sec
 ARIMA(9,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=2.16 sec
 ARIMA(9,1,3)(1,0,1)[12] intercept   : AIC=inf, Time=2.16 sec
 ARIMA(9,1,4)(0,0,0)[12] intercept   : AIC=676.470, Time=0.85 sec
 ARIMA(9,1,4)(0,0,1)[12] intercept   : AIC=671.627, Time=1.65 sec
 ARIMA(9,1,4)(1,0,0)[12] intercept   : AIC=inf, Time=2.58 sec
 ARIMA(9,1,4)(1,0,1)[12] intercept   : AIC=615.979, Time=2.44 sec
 ARIMA(9,1,5)(0,0,0)[12] intercept   : AIC=inf, Time=0.95 sec
 ARIMA(9,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=1.88 sec
 ARIMA(9,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=2.42 sec
 ARIMA(9,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=2.67 sec
 ARIMA(9,1,6)(0,0,0)[12] intercept   : AIC=636.299, Time=0.90 sec
 ARIMA(9,1,6)(0,0,1)[12] intercept   : AIC=640.345, Time=1.94 sec
 ARIMA(9,1,6)(1,0,0)[12] intercept   : AIC=inf, Time=2.48 sec
 ARIMA(9,1,6)(1,0,1)[12] intercept   : AIC=inf, Time=2.50 sec
 ARIMA(9,1,7)(0,0,0)[12] intercept   : AIC=644.864, Time=1.07 sec
 ARIMA(9,1,7)(0,0,1)[12] intercept   : AIC=646.739, Time=2.28 sec
 ARIMA(9,1,7)(1,0,0)[12] intercept   : AIC=649.890, Time=2.50 sec
 ARIMA(9,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=2.77 sec
 ARIMA(9,1,8)(0,0,0)[12] intercept   : AIC=641.624, Time=1.12 sec
 ARIMA(9,1,8)(0,0,1)[12] intercept   : AIC=646.325, Time=2.55 sec
 ARIMA(9,1,8)(1,0,0)[12] intercept   : AIC=646.987, Time=2.79 sec
 ARIMA(9,1,8)(1,0,1)[12] intercept   : AIC=644.189, Time=2.80 sec
 ARIMA(9,1,9)(0,0,0)[12] intercept   : AIC=635.532, Time=1.20 sec
 ARIMA(9,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=3.13 sec
 ARIMA(9,1,9)(1,0,0)[12] intercept   : AIC=639.962, Time=2.70 sec
 ARIMA(9,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=3.64 sec
 ARIMA(9,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=1.25 sec
 ARIMA(9,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=3.03 sec
 ARIMA(9,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=2.73 sec
 ARIMA(9,1,10)(1,0,1)[12] intercept   : AIC=inf, Time=3.26 sec
 ARIMA(9,1,11)(0,0,0)[12] intercept   : AIC=636.706, Time=1.56 sec
 ARIMA(9,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=3.94 sec
 ARIMA(9,1,11)(1,0,0)[12] intercept   : AIC=640.643, Time=2.96 sec
 ARIMA(9,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=4.12 sec
 ARIMA(10,1,0)(0,0,0)[12] intercept   : AIC=724.817, Time=0.28 sec
 ARIMA(10,1,0)(0,0,1)[12] intercept   : AIC=718.423, Time=0.38 sec
 ARIMA(10,1,0)(1,0,0)[12] intercept   : AIC=716.834, Time=0.92 sec
 ARIMA(10,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=2.20 sec
 ARIMA(10,1,1)(0,0,0)[12] intercept   : AIC=717.917, Time=0.53 sec
 ARIMA(10,1,1)(0,0,1)[12] intercept   : AIC=716.172, Time=0.77 sec
 ARIMA(10,1,1)(1,0,0)[12] intercept   : AIC=715.496, Time=1.45 sec
 ARIMA(10,1,1)(1,0,1)[12] intercept   : AIC=inf, Time=2.27 sec
 ARIMA(10,1,2)(0,0,0)[12] intercept   : AIC=693.842, Time=0.77 sec
 ARIMA(10,1,2)(0,0,1)[12] intercept   : AIC=694.048, Time=1.19 sec
 ARIMA(10,1,2)(1,0,0)[12] intercept   : AIC=694.129, Time=2.35 sec
 ARIMA(10,1,2)(1,0,1)[12] intercept   : AIC=inf, Time=2.61 sec
 ARIMA(10,1,3)(0,0,0)[12] intercept   : AIC=700.632, Time=1.03 sec
 ARIMA(10,1,3)(0,0,1)[12] intercept   : AIC=689.727, Time=1.56 sec
 ARIMA(10,1,3)(1,0,0)[12] intercept   : AIC=inf, Time=2.52 sec
 ARIMA(10,1,3)(1,0,1)[12] intercept   : AIC=623.250, Time=3.12 sec
 ARIMA(10,1,4)(0,0,0)[12] intercept   : AIC=697.430, Time=1.04 sec
 ARIMA(10,1,4)(0,0,1)[12] intercept   : AIC=667.073, Time=1.75 sec
 ARIMA(10,1,4)(1,0,0)[12] intercept   : AIC=669.327, Time=2.62 sec
 ARIMA(10,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=2.85 sec
 ARIMA(10,1,5)(0,0,0)[12] intercept   : AIC=658.846, Time=1.03 sec
 ARIMA(10,1,5)(0,0,1)[12] intercept   : AIC=705.870, Time=1.93 sec
 ARIMA(10,1,5)(1,0,0)[12] intercept   : AIC=709.255, Time=2.67 sec
 ARIMA(10,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=2.63 sec
 ARIMA(10,1,6)(0,0,0)[12] intercept   : AIC=643.057, Time=1.12 sec
 ARIMA(10,1,6)(0,0,1)[12] intercept   : AIC=645.033, Time=2.12 sec
 ARIMA(10,1,6)(1,0,0)[12] intercept   : AIC=644.305, Time=2.81 sec
 ARIMA(10,1,6)(1,0,1)[12] intercept   : AIC=inf, Time=3.05 sec
 ARIMA(10,1,7)(0,0,0)[12] intercept   : AIC=638.134, Time=1.21 sec
 ARIMA(10,1,7)(0,0,1)[12] intercept   : AIC=639.956, Time=2.52 sec
 ARIMA(10,1,7)(1,0,0)[12] intercept   : AIC=640.243, Time=2.97 sec
 ARIMA(10,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=3.26 sec
 ARIMA(10,1,8)(0,0,0)[12] intercept   : AIC=642.525, Time=1.22 sec
 ARIMA(10,1,8)(0,0,1)[12] intercept   : AIC=644.641, Time=2.65 sec
 ARIMA(10,1,8)(1,0,0)[12] intercept   : AIC=643.751, Time=3.21 sec
 ARIMA(10,1,8)(1,0,1)[12] intercept   : AIC=645.525, Time=3.40 sec
 ARIMA(10,1,9)(0,0,0)[12] intercept   : AIC=inf, Time=1.33 sec
 ARIMA(10,1,9)(0,0,1)[12] intercept   : AIC=inf, Time=3.35 sec
 ARIMA(10,1,9)(1,0,0)[12] intercept   : AIC=inf, Time=3.25 sec
 ARIMA(10,1,9)(1,0,1)[12] intercept   : AIC=inf, Time=3.42 sec
 ARIMA(10,1,10)(0,0,0)[12] intercept   : AIC=inf, Time=1.33 sec
 ARIMA(10,1,10)(0,0,1)[12] intercept   : AIC=inf, Time=3.29 sec
 ARIMA(10,1,10)(1,0,0)[12] intercept   : AIC=inf, Time=3.45 sec
 ARIMA(10,1,10)(1,0,1)[12] intercept   : AIC=631.020, Time=3.46 sec
 ARIMA(10,1,11)(0,0,0)[12] intercept   : AIC=inf, Time=1.62 sec
 ARIMA(10,1,11)(0,0,1)[12] intercept   : AIC=inf, Time=4.05 sec
 ARIMA(10,1,11)(1,0,0)[12] intercept   : AIC=inf, Time=3.61 sec
 ARIMA(10,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=4.28 sec
 ARIMA(11,1,0)(0,0,0)[12] intercept   : AIC=706.342, Time=0.35 sec
 ARIMA(11,1,0)(0,0,1)[12] intercept   : AIC=707.943, Time=0.59 sec
 ARIMA(11,1,0)(1,0,0)[12] intercept   : AIC=707.924, Time=1.21 sec
 ARIMA(11,1,0)(1,0,1)[12] intercept   : AIC=inf, Time=2.25 sec
 ARIMA(11,1,1)(0,0,0)[12] intercept   : AIC=704.056, Time=0.84 sec
 ARIMA(11,1,1)(0,0,1)[12] intercept   : AIC=665.182, Time=1.28 sec
 ARIMA(11,1,1)(1,0,0)[12] intercept   : AIC=701.604, Time=2.21 sec
 ARIMA(11,1,1)(1,0,1)[12] intercept   : AIC=651.247, Time=2.45 sec
 ARIMA(11,1,2)(0,0,0)[12] intercept   : AIC=688.261, Time=0.91 sec
 ARIMA(11,1,2)(0,0,1)[12] intercept   : AIC=inf, Time=1.45 sec
 ARIMA(11,1,2)(1,0,0)[12] intercept   : AIC=680.567, Time=2.47 sec
 ARIMA(11,1,2)(1,0,1)[12] intercept   : AIC=625.879, Time=2.45 sec
 ARIMA(11,1,3)(0,0,0)[12] intercept   : AIC=703.699, Time=1.02 sec
 ARIMA(11,1,3)(0,0,1)[12] intercept   : AIC=728.984, Time=1.51 sec
 ARIMA(11,1,3)(1,0,0)[12] intercept   : AIC=717.311, Time=2.48 sec
 ARIMA(11,1,3)(1,0,1)[12] intercept   : AIC=671.666, Time=2.63 sec
 ARIMA(11,1,4)(0,0,0)[12] intercept   : AIC=679.250, Time=1.01 sec
 ARIMA(11,1,4)(0,0,1)[12] intercept   : AIC=676.720, Time=1.85 sec
 ARIMA(11,1,4)(1,0,0)[12] intercept   : AIC=673.489, Time=2.95 sec
 ARIMA(11,1,4)(1,0,1)[12] intercept   : AIC=inf, Time=2.98 sec
 ARIMA(11,1,5)(0,0,0)[12] intercept   : AIC=653.144, Time=1.10 sec
 ARIMA(11,1,5)(0,0,1)[12] intercept   : AIC=inf, Time=2.04 sec
 ARIMA(11,1,5)(1,0,0)[12] intercept   : AIC=inf, Time=2.99 sec
 ARIMA(11,1,5)(1,0,1)[12] intercept   : AIC=inf, Time=2.81 sec
 ARIMA(11,1,6)(0,0,0)[12] intercept   : AIC=662.314, Time=1.16 sec
 ARIMA(11,1,6)(0,0,1)[12] intercept   : AIC=615.641, Time=2.15 sec
 ARIMA(11,1,6)(1,0,0)[12] intercept   : AIC=676.141, Time=2.85 sec
 ARIMA(11,1,6)(1,0,1)[12] intercept   : AIC=632.613, Time=2.95 sec
 ARIMA(11,1,7)(0,0,0)[12] intercept   : AIC=inf, Time=1.20 sec
 ARIMA(11,1,7)(0,0,1)[12] intercept   : AIC=inf, Time=2.53 sec
 ARIMA(11,1,7)(1,0,0)[12] intercept   : AIC=inf, Time=3.19 sec
 ARIMA(11,1,7)(1,0,1)[12] intercept   : AIC=inf, Time=3.11 sec
 ARIMA(11,1,8)(0,0,0)[12] intercept   : AIC=638.670, Time=1.25 sec
 ARIMA(11,1,8)(0,0,1)[12] intercept   : AIC=639.408, Time=2.82 sec
 ARIMA(11,1,8)(1,0,0)[12] intercept   : AIC=639.808, Time=3.02 sec
 ARIMA(11,1,8)(1,0,1)[12] intercept   : AIC=642.485, Time=3.45 sec
 ARIMA(11,1,9)(0,0,0)[12] intercept   : AIC=640.553, Time=1.36 sec
 ARIMA(11,1,9)(0,0,1)[12] intercept   : AIC=640.596, Time=3.27 sec
 ARIMA(11,1,9)(1,0,0)[12] intercept   : AIC=642.323, Time=3.29 sec
 ARIMA(11,1,9)(1,0,1)[12] intercept   : AIC=647.488, Time=3.36 sec
 ARIMA(11,1,10)(0,0,0)[12] intercept   : AIC=645.775, Time=1.47 sec
 ARIMA(11,1,10)(0,0,1)[12] intercept   : AIC=648.463, Time=3.51 sec
 ARIMA(11,1,10)(1,0,0)[12] intercept   : AIC=648.303, Time=3.44 sec
 ARIMA(11,1,10)(1,0,1)[12] intercept   : AIC=647.325, Time=3.61 sec
 ARIMA(11,1,11)(0,0,0)[12] intercept   : AIC=639.048, Time=1.69 sec
 ARIMA(11,1,11)(0,0,1)[12] intercept   : AIC=638.104, Time=4.35 sec
 ARIMA(11,1,11)(1,0,0)[12] intercept   : AIC=639.554, Time=3.68 sec
 ARIMA(11,1,11)(1,0,1)[12] intercept   : AIC=inf, Time=4.51 sec

Best model:  ARIMA(11,1,6)(0,0,1)[12] intercept
Total fit time: 881.592 seconds
Optimal SARIMA order: (11, 1, 6)
Optimal SARIMA seasonal order: (0, 0, 1, 12)
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[48]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># create model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="n">normal_order</span><span class="p">,</span> <span class="n">seasonal_order</span><span class="o">=</span><span class="n">seasonal_order</span><span class="p">)</span>

<span class="c1"># fit model</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># Print model summary</span>
<span class="nb">print</span><span class="p">(</span><span class="n">model_fit</span><span class="o">.</span><span class="n">summary</span><span class="p">())</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 1.6968908309936523
                                      SARIMAX Results
===========================================================================================
Dep. Variable:                           mean_temp   No. Observations:                  480
Model:             ARIMA(11, 1, 6)x(0, 0, [1], 12)   Log Likelihood                -281.080
Date:                             Thu, 15 Jun 2023   AIC                            600.160
Time:                                     02:38:16   BIC                            679.422
Sample:                                 01-31-1982   HQIC                           631.319
                                      - 12-31-2021
Covariance Type:                               opg
==============================================================================
                 coef    std err          z      P&gt;|z|      [0.025      0.975]
------------------------------------------------------------------------------
ar.L1         -0.9615      0.025    -38.784      0.000      -1.010      -0.913
ar.L2         -0.9342      0.024    -38.845      0.000      -0.981      -0.887
ar.L3         -0.9928      0.013    -74.501      0.000      -1.019      -0.967
ar.L4         -0.9503      0.026    -36.349      0.000      -1.002      -0.899
ar.L5         -0.9486      0.022    -43.946      0.000      -0.991      -0.906
ar.L6         -0.9804      0.018    -54.010      0.000      -1.016      -0.945
ar.L7         -0.9648      0.020    -48.606      0.000      -1.004      -0.926
ar.L8         -0.9426      0.023    -40.407      0.000      -0.988      -0.897
ar.L9         -0.9748      0.017    -58.682      0.000      -1.007      -0.942
ar.L10        -0.9742      0.019    -49.989      0.000      -1.012      -0.936
ar.L11        -0.9219      0.028    -32.418      0.000      -0.978      -0.866
ma.L1          0.3865      0.050      7.791      0.000       0.289       0.484
ma.L2          0.3537      0.057      6.174      0.000       0.241       0.466
ma.L3          0.2886      0.056      5.150      0.000       0.179       0.398
ma.L4          0.0944      0.063      1.511      0.131      -0.028       0.217
ma.L5          0.0199      0.060      0.333      0.739      -0.097       0.137
ma.L6          0.0221      0.053      0.417      0.677      -0.082       0.126
ma.S.L12      -0.8598      0.040    -21.544      0.000      -0.938      -0.782
sigma2         0.1881      0.014     13.683      0.000       0.161       0.215
===================================================================================
Ljung-Box (L1) (Q):                   0.01   Jarque-Bera (JB):                 0.06
Prob(Q):                              0.94   Prob(JB):                         0.97
Heteroskedasticity (H):               0.88   Skew:                             0.02
Prob(H) (two-sided):                  0.41   Kurtosis:                         3.03
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[49]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># get prediction start and end dates</span>
<span class="n">pred_start_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">pred_end_date</span> <span class="o">=</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>

<span class="c1"># get predictions and residuals</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">start</span><span class="o">=</span><span class="n">pred_start_date</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">pred_end_date</span><span class="p">)</span>
<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(residuals)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from auto SARIMA Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_49.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[50]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_50.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0104
Root Mean Squared Error: 0.34995830445205695
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>SARIMA(11,0,8)(0,0,0)[12]:</strong>
                    Mean Absolute Percent Error: 0.0165
                    Root Mean Squared Error: 0.6175906151774886</p>
                <p><strong>SARIMA(11,1,6)(0,0,1)[12]:</strong>
                    Mean Absolute Percent Error: 0.0104
                    Root Mean Squared Error: 0.34995830445205695</p>
                <p>The auto SARIMA model chose these 2 optimal models with different orders of <em>d</em>. Here, SARIMA(11,1,6)(0,0,1)[12] was better, even better that that of ARIMA(12,0,8)(0,0,0)[0] (RMSE=0.37388).</p>
                <p>Let's complete this with the RFO of SARIMA(11,1,6)(0,0,1)[12].</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[51]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># create the model</span>
<span class="n">predictions_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">Series</span><span class="p">(</span><span class="n">dtype</span><span class="o">=</span><span class="s1">'float64'</span><span class="p">)</span>
<span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="k">for</span> <span class="n">end_date</span> <span class="ow">in</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">:</span>
    <span class="n">train_data</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="p">[:</span><span class="n">end_date</span> <span class="o">-</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">)]</span>
    <span class="n">model</span> <span class="o">=</span> <span class="n">ARIMA</span><span class="p">(</span><span class="n">train_data</span><span class="p">,</span> <span class="n">order</span><span class="o">=</span><span class="p">(</span><span class="mi">11</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">6</span><span class="p">),</span> <span class="n">seasonal_order</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">12</span><span class="p">),</span> <span class="n">enforce_stationarity</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
    <span class="n">model_fit</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">()</span>
    <span class="n">pred</span> <span class="o">=</span> <span class="n">model_fit</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">end_date</span><span class="p">)</span>
    <span class="n">predictions_rolling</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span> <span class="o">=</span> <span class="n">pred</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="n">end_date</span><span class="p">]</span>
<span class="n">end</span> <span class="o">=</span> <span class="n">time</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Model Fitting Time: </span><span class="si">&#123</span><span class="n">end</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">start</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">residuals_rolling</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions_rolling</span>

<span class="c1"># print(residuals_rolling)</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from auto SARIMA Model (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error_rolling</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals_rolling</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error_rolling</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model Fitting Time: 17.422630071640015
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>/Users/linustws/opt/anaconda3/envs/singapore-weather-prediction/lib/python3.9/site-packages/statsmodels/base/model.py:607: ConvergenceWarning:

Maximum Likelihood optimization failed to converge. Check mle_retvals

</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_51.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>Note: I had to use enforce_stationarity=False here if not I would get a LinAlgError: LU decomposition error.</strong></p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[52]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">plot_data_rolling</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions_rolling</span><span class="p">})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test_rolling</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data_rolling</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions (Rolling Window)'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test_rolling</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">/</span><span class="n">test_data</span><span class="p">)),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals_rolling</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_52.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0116
Root Mean Squared Error: 0.40789190822712473
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>The RFO of SARIMA(11,1,6)(0,0,1)[12] did worse than its non RFO (RMSE=0.34996), similar to the RFO of ARIMA with the non-RFO ARIMA. Overall, looking at the above results, it seems that auto SARIMA and auto ARIMA performed about the same.</p>
                <p><strong>SARIMA(11,1,6)(0,0,1)[12]:</strong> 0.34996<br><strong>SARIMA(11,1,6)(0,0,1)[12] RFO:</strong> 0.40789<br><strong>ARIMA(12,0,8)(0,0,0)[0]:</strong> 0.37388<br><strong>ARIMA(12,0,8)(0,0,0)[0] RFO:</strong> 0.40278</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="LSTM-Model-Approach" data-toc-modified-id="LSTM-Model-Approach-1.0.7"><a class="toc-mod-link" id="LSTM-Model-Approach-1.0.7"></a><span class="toc-item-num">1.0.7&nbsp;&nbsp;</span>LSTM Model Approach<a class="anchor-link" href="#LSTM-Model-Approach">¶</a></h3>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[53]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">fig_monthly_mean_temp</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_53.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[54]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># Perform seasonal decomposition (this can help analyse the individual components in greater detail)</span>
<span class="n">results</span> <span class="o">=</span> <span class="n">seasonal_decompose</span><span class="p">(</span><span class="n">series_monthly_mean_temp</span><span class="p">)</span>

<span class="c1"># Plot the seasonal decomposition </span>
<span class="n">fig_decomposition</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">results</span><span class="o">.</span><span class="n">observed</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Seasonal Decomposition - Observed'</span><span class="p">)</span>
<span class="n">fig_decomposition</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Datetime'</span><span class="p">)</span>
<span class="n">fig_decomposition</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Observed'</span><span class="p">)</span>
<span class="n">fig_decomposition</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_54.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[55]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">fig_trend</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">results</span><span class="o">.</span><span class="n">trend</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Seasonal Decomposition - Trend'</span><span class="p">)</span>
<span class="n">fig_trend</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Datetime'</span><span class="p">)</span>
<span class="n">fig_trend</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Trend'</span><span class="p">)</span>
<span class="n">fig_trend</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_55.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[56]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">fig_seasonal</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">results</span><span class="o">.</span><span class="n">seasonal</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Seasonal Decomposition - Seasonal'</span><span class="p">)</span>
<span class="n">fig_seasonal</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Datetime'</span><span class="p">)</span>
<span class="n">fig_seasonal</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Seasonal'</span><span class="p">)</span>
<span class="n">fig_seasonal</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_56.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[57]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">fig_residual</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">results</span><span class="o">.</span><span class="n">resid</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Seasonal Decomposition - Residual'</span><span class="p">)</span>
<span class="n">fig_residual</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Datetime'</span><span class="p">)</span>
<span class="n">fig_residual</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'Residual'</span><span class="p">)</span>
<span class="n">fig_residual</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_57.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>There is no need to make the data stationary here as RNN can work on more complex and non-stationary data compared to the ARIMA models.</strong></p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[58]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># set seed to ensure determinism and reproduceability (always retest from here)</span>
<span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'TF_DETERMINISTIC_OPS'</span><span class="p">]</span> <span class="o">=</span> <span class="s1">'1'</span>
<span class="n">tf</span><span class="o">.</span><span class="n">keras</span><span class="o">.</span><span class="n">utils</span><span class="o">.</span><span class="n">set_random_seed</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
<span class="n">tf</span><span class="o">.</span><span class="n">config</span><span class="o">.</span><span class="n">experimental</span><span class="o">.</span><span class="n">enable_op_determinism</span><span class="p">()</span>

<span class="c1"># print(series_monthly_mean_temp)</span>
<span class="n">df_monthly_mean_temp</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">to_frame</span><span class="p">()</span>  <span class="c1"># Convert Series to DataFrame</span>
<span class="c1"># print(df_monthly_mean_temp)</span>
<span class="n">scaler</span> <span class="o">=</span> <span class="n">MinMaxScaler</span><span class="p">()</span>
<span class="n">scaler</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">df_monthly_mean_temp</span><span class="p">)</span>
<span class="n">df_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">scaler</span><span class="o">.</span><span class="n">transform</span><span class="p">(</span><span class="n">df_monthly_mean_temp</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">shape</span><span class="p">)</span>

<span class="c1"># Create a new DataFrame with the normalized values</span>
<span class="n">df_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="p">,</span> <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">'normalised'</span><span class="p">],</span> <span class="n">index</span><span class="o">=</span><span class="n">df_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">)</span>
<span class="c1"># print(df_normalised)</span>
<span class="n">mean_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">df_normalised_monthly_mean_temp</span><span class="p">[</span><span class="s1">'normalised'</span><span class="p">]</span><span class="o">.</span><span class="n">mean</span><span class="p">()</span>

<span class="c1"># Plot the normalized data</span>
<span class="n">fig_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Normalised'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Normalised Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.2</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Normalised Value: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_normalised_monthly_mean_temp</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_normalised_monthly_mean_temp</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>(496, 1)
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_58.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[59]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># split train:test to 80:20</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="p">)</span> <span class="o">*</span> <span class="mf">0.8</span><span class="p">)</span>
<span class="n">train_data</span> <span class="o">=</span> <span class="n">df_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">df_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span><span class="p">:]</span>
<span class="n">train_data_norm</span> <span class="o">=</span> <span class="n">df_normalised_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span><span class="o">.</span><span class="n">values</span>
<span class="n">test_data_norm</span> <span class="o">=</span> <span class="n">df_normalised_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span><span class="p">:]</span><span class="o">.</span><span class="n">values</span>

<span class="c1"># print(train_data)</span>
<span class="c1"># print(test_data)</span>
<span class="c1"># print(train_data_norm.shape)</span>
<span class="c1"># print(test_data_norm.shape)</span>
</pre></div>

                    </div>
                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[60]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># define generator</span>
<span class="n">n_input</span> <span class="o">=</span> <span class="mi">12</span>
<span class="n">n_features</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">generator</span> <span class="o">=</span> <span class="n">TimeseriesGenerator</span><span class="p">(</span><span class="n">train_data_norm</span><span class="p">,</span> <span class="n">train_data_norm</span><span class="p">,</span> <span class="n">length</span><span class="o">=</span><span class="n">n_input</span><span class="p">,</span> <span class="n">batch_size</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>

<span class="c1"># Create the validation generator</span>
<span class="n">validation_generator</span> <span class="o">=</span> <span class="n">TimeseriesGenerator</span><span class="p">(</span><span class="n">test_data_norm</span><span class="p">,</span> <span class="n">test_data_norm</span><span class="p">,</span> <span class="n">length</span><span class="o">=</span><span class="n">n_input</span><span class="p">,</span> <span class="n">batch_size</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[61]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">X</span><span class="p">,</span><span class="n">y</span> <span class="o">=</span> <span class="n">generator</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Given the Array: </span><span class="se">\n</span><span class="si">&#123</span><span class="n">X</span><span class="o">.</span><span class="n">flatten</span><span class="p">()</span><span class="si">}</span><span class="s1">'</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Predict this y: </span><span class="se">\n</span><span class="s1"> </span><span class="si">&#123</span><span class="n">y</span><span class="o">.</span><span class="n">flatten</span><span class="p">()</span><span class="si">}</span><span class="s1">'</span><span class="p">)</span>
<span class="n">X</span><span class="o">.</span><span class="n">shape</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Given the Array:
[0.12195122 0.41463415 0.43902439 0.3902439  0.63414634 0.73170732
 0.68292683 0.56097561 0.6097561  0.48780488 0.46341463 0.19512195]
Predict this y:
 [0.26829268]
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt output_prompt">Out[61]:</div>




                        <div class="output_text output_subarea output_execute_result">
                            <pre>(1, 12, 1)</pre>
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[62]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># define model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Sequential</span><span class="p">()</span>
<span class="n">model</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">LSTM</span><span class="p">(</span><span class="mi">100</span><span class="p">,</span> <span class="n">activation</span><span class="o">=</span><span class="s1">'tanh'</span><span class="p">,</span> <span class="n">input_shape</span><span class="o">=</span><span class="p">(</span><span class="n">n_input</span><span class="p">,</span> <span class="n">n_features</span><span class="p">)))</span> <span class="c1"># here i used tanh instead of relu to take advantage of cuDNN to speed up training</span>
<span class="c1"># model.add(Dropout(0.2)) </span>
<span class="n">model</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">Dense</span><span class="p">(</span><span class="mi">1</span><span class="p">))</span>
<span class="c1"># optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)</span>
<span class="n">model</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="n">optimizer</span><span class="o">=</span><span class="n">tf</span><span class="o">.</span><span class="n">keras</span><span class="o">.</span><span class="n">optimizers</span><span class="o">.</span><span class="n">Adam</span><span class="p">(</span><span class="n">learning_rate</span><span class="o">=</span><span class="mf">0.001</span><span class="p">),</span> <span class="n">loss</span><span class="o">=</span><span class="s1">'mse'</span><span class="p">)</span>
<span class="n">model</span><span class="o">.</span><span class="n">summary</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 lstm (LSTM)                 (None, 100)               40800

 dense (Dense)               (None, 1)                 101

=================================================================
Total params: 40,901
Trainable params: 40,901
Non-trainable params: 0
_________________________________________________________________
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[63]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># fit model and save history</span>
<span class="n">history</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">generator</span><span class="p">,</span><span class="n">epochs</span><span class="o">=</span><span class="mi">100</span><span class="p">,</span> <span class="n">validation_data</span><span class="o">=</span><span class="n">validation_generator</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Epoch 1/100
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stderr output_text">
<pre>2023-06-15 02:38:34.606859: W tensorflow/tsl/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>384/384 [==============================] - 2s 3ms/step - loss: 0.0386 - val_loss: 0.0362
Epoch 2/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0220 - val_loss: 0.0176
Epoch 3/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0180 - val_loss: 0.0163
Epoch 4/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0162 - val_loss: 0.0187
Epoch 5/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0169 - val_loss: 0.0153
Epoch 6/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0162 - val_loss: 0.0156
Epoch 7/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0160 - val_loss: 0.0159
Epoch 8/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0151 - val_loss: 0.0148
Epoch 9/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0153 - val_loss: 0.0155
Epoch 10/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0151 - val_loss: 0.0149
Epoch 11/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0150 - val_loss: 0.0148
Epoch 12/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0150 - val_loss: 0.0174
Epoch 13/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0146 - val_loss: 0.0166
Epoch 14/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0151 - val_loss: 0.0158
Epoch 15/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0143 - val_loss: 0.0158
Epoch 16/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0148 - val_loss: 0.0166
Epoch 17/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0140 - val_loss: 0.0165
Epoch 18/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0145 - val_loss: 0.0158
Epoch 19/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0150 - val_loss: 0.0160
Epoch 20/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0142 - val_loss: 0.0170
Epoch 21/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0144 - val_loss: 0.0150
Epoch 22/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0143 - val_loss: 0.0152
Epoch 23/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0139 - val_loss: 0.0153
Epoch 24/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0139 - val_loss: 0.0163
Epoch 25/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0136 - val_loss: 0.0210
Epoch 26/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0138 - val_loss: 0.0153
Epoch 27/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0136 - val_loss: 0.0149
Epoch 28/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0137 - val_loss: 0.0156
Epoch 29/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0138 - val_loss: 0.0186
Epoch 30/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0137 - val_loss: 0.0155
Epoch 31/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0135 - val_loss: 0.0167
Epoch 32/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0128 - val_loss: 0.0204
Epoch 33/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0138 - val_loss: 0.0163
Epoch 34/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0127 - val_loss: 0.0173
Epoch 35/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0129 - val_loss: 0.0163
Epoch 36/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0126 - val_loss: 0.0146
Epoch 37/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0129 - val_loss: 0.0153
Epoch 38/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0126 - val_loss: 0.0161
Epoch 39/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0127 - val_loss: 0.0162
Epoch 40/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0126 - val_loss: 0.0173
Epoch 41/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0125 - val_loss: 0.0150
Epoch 42/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0124 - val_loss: 0.0153
Epoch 43/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0122 - val_loss: 0.0178
Epoch 44/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0129 - val_loss: 0.0144
Epoch 45/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0126 - val_loss: 0.0142
Epoch 46/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0123 - val_loss: 0.0146
Epoch 47/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0122 - val_loss: 0.0152
Epoch 48/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0128 - val_loss: 0.0150
Epoch 49/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0126 - val_loss: 0.0165
Epoch 50/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0121 - val_loss: 0.0150
Epoch 51/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0121 - val_loss: 0.0154
Epoch 52/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0119 - val_loss: 0.0155
Epoch 53/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0117 - val_loss: 0.0145
Epoch 54/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0115 - val_loss: 0.0160
Epoch 55/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0115 - val_loss: 0.0158
Epoch 56/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0114 - val_loss: 0.0147
Epoch 57/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0118 - val_loss: 0.0154
Epoch 58/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0118 - val_loss: 0.0143
Epoch 59/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0112 - val_loss: 0.0156
Epoch 60/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0113 - val_loss: 0.0157
Epoch 61/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0117 - val_loss: 0.0159
Epoch 62/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0112 - val_loss: 0.0146
Epoch 63/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0113 - val_loss: 0.0155
Epoch 64/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0106 - val_loss: 0.0171
Epoch 65/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0109 - val_loss: 0.0161
Epoch 66/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0116 - val_loss: 0.0151
Epoch 67/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0112 - val_loss: 0.0152
Epoch 68/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0109 - val_loss: 0.0167
Epoch 69/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0107 - val_loss: 0.0146
Epoch 70/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0106 - val_loss: 0.0147
Epoch 71/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0105 - val_loss: 0.0158
Epoch 72/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0103 - val_loss: 0.0141
Epoch 73/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0102 - val_loss: 0.0174
Epoch 74/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0100 - val_loss: 0.0173
Epoch 75/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0103 - val_loss: 0.0154
Epoch 76/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0097 - val_loss: 0.0153
Epoch 77/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0097 - val_loss: 0.0174
Epoch 78/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0101 - val_loss: 0.0157
Epoch 79/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0100 - val_loss: 0.0149
Epoch 80/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0096 - val_loss: 0.0156
Epoch 81/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0097 - val_loss: 0.0153
Epoch 82/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0099 - val_loss: 0.0167
Epoch 83/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0102 - val_loss: 0.0156
Epoch 84/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0097 - val_loss: 0.0142
Epoch 85/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0096 - val_loss: 0.0160
Epoch 86/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0093 - val_loss: 0.0165
Epoch 87/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0095 - val_loss: 0.0162
Epoch 88/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0091 - val_loss: 0.0171
Epoch 89/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0093 - val_loss: 0.0163
Epoch 90/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0090 - val_loss: 0.0143
Epoch 91/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0091 - val_loss: 0.0143
Epoch 92/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0094 - val_loss: 0.0153
Epoch 93/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0089 - val_loss: 0.0151
Epoch 94/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0089 - val_loss: 0.0150
Epoch 95/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0088 - val_loss: 0.0143
Epoch 96/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0089 - val_loss: 0.0139
Epoch 97/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0086 - val_loss: 0.0170
Epoch 98/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0088 - val_loss: 0.0199
Epoch 99/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0093 - val_loss: 0.0172
Epoch 100/100
384/384 [==============================] - 1s 2ms/step - loss: 0.0108 - val_loss: 0.0141
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[64]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># Get loss history</span>
<span class="n">loss</span> <span class="o">=</span> <span class="n">history</span><span class="o">.</span><span class="n">history</span><span class="p">[</span><span class="s1">'loss'</span><span class="p">]</span>
<span class="n">val_loss</span> <span class="o">=</span> <span class="n">history</span><span class="o">.</span><span class="n">history</span><span class="p">[</span><span class="s1">'val_loss'</span><span class="p">]</span>

<span class="c1"># print(f"training loss: {loss}")</span>
<span class="c1"># print(f"validation loss: {val_loss}")</span>

<span class="c1"># Find the epoch with the minimum validation loss</span>
<span class="n">min_val_loss_epoch</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">argmin</span><span class="p">(</span><span class="n">val_loss</span><span class="p">)</span> <span class="o">+</span> <span class="mi">1</span>
<span class="n">min_val_loss</span> <span class="o">=</span> <span class="n">val_loss</span><span class="p">[</span><span class="n">min_val_loss_epoch</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Minimum validation loss: </span><span class="si">&#123</span><span class="n">min_val_loss</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Epoch with minimum validation loss: </span><span class="si">&#123</span><span class="n">min_val_loss_epoch</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># Create DataFrame</span>
<span class="n">epochs</span> <span class="o">=</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">len</span><span class="p">(</span><span class="n">loss</span><span class="p">)</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">loss_df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'epoch'</span><span class="p">:</span> <span class="n">epochs</span><span class="p">,</span> <span class="s1">'training_loss'</span><span class="p">:</span> <span class="n">loss</span><span class="p">,</span> <span class="s1">'validation_loss'</span><span class="p">:</span> <span class="n">val_loss</span><span class="p">})</span>

<span class="c1"># Plot loss</span>
<span class="n">fig_loss</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">loss_df</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'epoch'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'training_loss'</span><span class="p">,</span> <span class="s1">'validation_loss'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Loss'</span><span class="p">,</span> <span class="s1">'epoch'</span><span class="p">:</span> <span class="s1">'Epoch'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Training and Validation Loss'</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Epoch: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Loss: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Minimum validation loss: 0.01386861503124237
Epoch with minimum validation loss: 96
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_64.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[65]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">last_train_batch</span> <span class="o">=</span> <span class="n">train_data_norm</span><span class="p">[</span><span class="o">-</span><span class="mi">12</span><span class="p">:]</span>
<span class="n">last_train_batch</span> <span class="o">=</span> <span class="n">last_train_batch</span><span class="o">.</span><span class="n">reshape</span><span class="p">((</span><span class="mi">1</span><span class="p">,</span> <span class="n">n_input</span><span class="p">,</span> <span class="n">n_features</span><span class="p">))</span>
<span class="n">model</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">last_train_batch</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>1/1 [==============================] - 0s 161ms/step
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt output_prompt">Out[65]:</div>




                        <div class="output_text output_subarea output_execute_result">
                            <pre>array([[0.3631621]], dtype=float32)</pre>
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[66]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">test_data_norm</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt output_prompt">Out[66]:</div>




                        <div class="output_text output_subarea output_execute_result">
                            <pre>array([0.36585366])</pre>
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[67]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">predictions_norm</span> <span class="o">=</span> <span class="p">[]</span>

<span class="n">first_eval_batch</span> <span class="o">=</span> <span class="n">train_data_norm</span><span class="p">[</span><span class="o">-</span><span class="n">n_input</span><span class="p">:]</span>
<span class="n">current_batch</span> <span class="o">=</span> <span class="n">first_eval_batch</span><span class="o">.</span><span class="n">reshape</span><span class="p">((</span><span class="mi">1</span><span class="p">,</span> <span class="n">n_input</span><span class="p">,</span> <span class="n">n_features</span><span class="p">))</span>

<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">test_data</span><span class="p">)):</span>

    <span class="c1"># get the prediction value for the first batch</span>
    <span class="n">current_pred</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">current_batch</span><span class="p">)[</span><span class="mi">0</span><span class="p">]</span>

    <span class="c1"># append the prediction into the array</span>
    <span class="n">predictions_norm</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">current_pred</span><span class="p">)</span>

    <span class="c1"># use the prediction to update the batch and remove the first value</span>
    <span class="n">current_batch</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">current_batch</span><span class="p">[:,</span><span class="mi">1</span><span class="p">:,:],[[</span><span class="n">current_pred</span><span class="p">]],</span><span class="n">axis</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 12ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 12ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 12ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 99ms/step
1/1 [==============================] - 0s 34ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 19ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 16ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 16ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 16ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 15ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 13ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 14ms/step
1/1 [==============================] - 0s 13ms/step
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[68]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">predictions_norm</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt output_prompt">Out[68]:</div>




                        <div class="output_text output_subarea output_execute_result">
<pre>[array([0.3631621], dtype=float32),
 array([0.42597657], dtype=float32),
 array([0.55605394], dtype=float32),
 array([0.6863072], dtype=float32),
 array([0.76753056], dtype=float32),
 array([0.78265554], dtype=float32),
 array([0.7166672], dtype=float32),
 array([0.62514055], dtype=float32),
 array([0.58941144], dtype=float32),
 array([0.5960854], dtype=float32),
 array([0.46640316], dtype=float32),
 array([0.34995174], dtype=float32),
 array([0.3467129], dtype=float32),
 array([0.40914553], dtype=float32),
 array([0.5226751], dtype=float32),
 array([0.6477614], dtype=float32),
 array([0.7378394], dtype=float32),
 array([0.74744046], dtype=float32),
 array([0.6793829], dtype=float32),
 array([0.6173713], dtype=float32),
 array([0.60769844], dtype=float32),
 array([0.5679723], dtype=float32),
 array([0.43790647], dtype=float32),
 array([0.33309907], dtype=float32),
 array([0.34270018], dtype=float32),
 array([0.41882026], dtype=float32),
 array([0.53937066], dtype=float32),
 array([0.66088694], dtype=float32),
 array([0.7408333], dtype=float32),
 array([0.73563373], dtype=float32),
 array([0.66083074], dtype=float32),
 array([0.61003214], dtype=float32),
 array([0.6057599], dtype=float32),
 array([0.54501873], dtype=float32),
 array([0.4108227], dtype=float32),
 array([0.32216114], dtype=float32),
 array([0.3482728], dtype=float32),
 array([0.43499267], dtype=float32),
 array([0.55982333], dtype=float32),
 array([0.67721254], dtype=float32),
 array([0.74539554], dtype=float32),
 array([0.7247614], dtype=float32),
 array([0.6457316], dtype=float32),
 array([0.6073772], dtype=float32),
 array([0.60195565], dtype=float32),
 array([0.5225945], dtype=float32),
 array([0.38721737], dtype=float32),
 array([0.3183669], dtype=float32),
 array([0.35786504], dtype=float32),
 array([0.4535848], dtype=float32),
 array([0.58080214], dtype=float32),
 array([0.6929304], dtype=float32),
 array([0.74772024], dtype=float32),
 array([0.71295345], dtype=float32),
 array([0.63422865], dtype=float32),
 array([0.6070014], dtype=float32),
 array([0.5953922], dtype=float32),
 array([0.49953616], dtype=float32),
 array([0.36705866], dtype=float32),
 array([0.3198491], dtype=float32),
 array([0.37054187], dtype=float32),
 array([0.4743411], dtype=float32),
 array([0.6020762], dtype=float32),
 array([0.70769], dtype=float32),
 array([0.7474501], dtype=float32),
 array([0.69963735], dtype=float32),
 array([0.62513304], dtype=float32),
 array([0.60743546], dtype=float32),
 array([0.58538324], dtype=float32),
 array([0.47501862], dtype=float32),
 array([0.3494174], dtype=float32),
 array([0.32500607], dtype=float32),
 array([0.38637668], dtype=float32),
 array([0.49778688], dtype=float32),
 array([0.6243601], dtype=float32),
 array([0.721662], dtype=float32),
 array([0.7444175], dtype=float32),
 array([0.68424314], dtype=float32),
 array([0.6174462], dtype=float32),
 array([0.607631], dtype=float32),
 array([0.57131624], dtype=float32),
 array([0.4487637], dtype=float32),
 array([0.33432245], dtype=float32),
 array([0.3327189], dtype=float32),
 array([0.40491027], dtype=float32),
 array([0.5231489], dtype=float32),
 array([0.6469705], dtype=float32),
 array([0.73380065], dtype=float32),
 array([0.73823464], dtype=float32),
 array([0.6673877], dtype=float32),
 array([0.6113859], dtype=float32),
 array([0.6067541], dtype=float32),
 array([0.5532779], dtype=float32),
 array([0.4219971], dtype=float32),
 array([0.3234139], dtype=float32),
 array([0.34187883], dtype=float32),
 array([0.42448664], dtype=float32),
 array([0.5479106], dtype=float32),
 array([0.6676974], dtype=float32),
 array([0.7423276], dtype=float32)]</pre>
                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[69]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># print(type(df_normalised_monthly_mean_temp))</span>
<span class="c1"># print(type(test_data))</span>
<span class="c1"># print(test_data.shape)</span>
<span class="c1"># print(test_data[:5])</span>
<span class="nb">print</span><span class="p">(</span><span class="n">test_data</span><span class="o">.</span><span class="n">head</span><span class="p">())</span>
<span class="n">predictions</span> <span class="o">=</span> <span class="n">scaler</span><span class="o">.</span><span class="n">inverse_transform</span><span class="p">(</span><span class="n">predictions_norm</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>            mean_temp
datetime
2015-01-31       26.9
2015-02-28       27.0
2015-03-31       28.2
2015-04-30       28.6
2015-05-31       28.7
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[70]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(type(residuals))</span>
<span class="c1"># print(type(residuals))</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from LSTM Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">axis</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>
<span class="c1"># print(mean_error)</span>
<span class="c1"># print(type(mean_error))</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="o">.</span><span class="n">values</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="o">.</span><span class="n">values</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_70.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[71]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># print(test_data_no_norm.index)</span>

<span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">flatten</span><span class="p">(),</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="o">.</span><span class="n">flatten</span><span class="p">()})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">),</span><span class="w"> </span><span class="n">axis</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span><span class="o">.</span><span class="n">item</span><span class="p">(),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span class="n">axis</span><span class="o">=</span><span class="mi">0</span><span class="p">))</span><span class="o">.</span><span class="n">item</span><span class="p">()</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_71.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0177
Root Mean Squared Error: 0.6206300301271244
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>lr=0.001<br>No Dropout<br>90:10<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0198
                    Root Mean Squared Error: 0.6755985619320392</p>
                <p><strong>LSTM(103 epochs, loss: 0.0085 - val_loss: 0.0119, beyond this point training loss decreases while validation loss fluctuates i.e. overfitting)</strong>
                    Mean Absolute Percent Error: 0.0215
                    Root Mean Squared Error: 0.7549385723557431</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0213
                    Root Mean Squared Error: 0.7878989971160217</p>
                <p><strong>80:20<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0177
                    Root Mean Squared Error: 0.6206300301271244</p>
                <p><strong>LSTM(113 epochs, loss: 0.0077 - val_loss: 0.0134, beyond this point training loss decreases while validation loss fluctuates i.e. overfitting)</strong>
                    Mean Absolute Percent Error: 0.0191
                    Root Mean Squared Error: 0.6949460889739134</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0173
                    Root Mean Squared Error: 0.6148360571951464</p>
                <p><strong>70:30<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0171
                    Root Mean Squared Error: 0.5935231394134313</p>
                <p><strong>LSTM(82 epochs, loss: 0.0101 - val_loss: 0.0121, beyond this point training loss decreases while validation loss fluctuates i.e. overfitting)</strong>
                    Mean Absolute Percent Error: 0.0194
                    Root Mean Squared Error: 0.7037250795707977</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0177
                    Root Mean Squared Error: 0.6491459898664801</p>
                <p><strong>lr=0.001<br>Dropout=0.2<br>80:20<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0249
                    Root Mean Squared Error: 0.8411129392339437</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0294
                    Root Mean Squared Error: 1.0054840656823747</p>
                <p><strong>lr=0.01 (val_loss not decreasing aft a short while, overfitting)<br>No Dropout<br>80:20<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0273
                    Root Mean Squared Error: 0.9110724662539238</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0179
                    Root Mean Squared Error: 0.6357450427997889</p>
                <p><strong>lr=0.0001 (converges too slowly, underfittng)<br>No Dropout<br>80:20<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0173
                    Root Mean Squared Error: 0.6130719319221452</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.027
                    Root Mean Squared Error: 0.9599652594001916</p>
                <p>It seems that lr=0.001 is the best here, and having dropout regularisation of 0.2 worsened the model's performance, although I only tested it on 80:20 split with 100 and 200 epochs to save time.Also, I learnt that although using the minimum validation loss to find the best fit model (least under/overfitting) is viable, it does not necessarily imply it will have the lowest RMSE. Additionally, it seems that we should not overlook the proportion of the validation dataset. If it's too small, there may not be enough diverse samples to effectively evaluate the model's generalization performance. As a result, the model may become overly tuned to the training data and perform poorly on unseen data. This can lead to overfitting, where the model memorizes the training examples instead of learning the underlying patterns. Here I required more than a year of validation/test data due to the n_input = 12, thus I split that data into ratios instead of a static limit of 1 year as I did with the ARIMA models. I would have did this ratio splitting on the ARIMA models if it did not take so long to train on multiple years of test data but due to this limitation I restricted its test data to a year.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>It was at this point when I realised actually I don't need to split into training and validation sets. The validation set can be used during the training phase to monitor the model's performance on data that is closer to the present time. This can help in detecting overfitting or other issues that may arise during training. By evaluating the model's performance on the validation set, I can make adjustments to the model's architecture, hyperparameters, or training process to improve its generalization ability and overall performance. However, I felt that the entire data is relevant for training, as there is a slight upward trend for the mean temperature right from the start, thus splitting into training and validation might not fully capture this trend, thus I have decided to train uptil end of 2021 and predict on test data of 2022, just like the ARIMA models. I'll then assess the performance by comparing the RMSE values of the predictions. This way, I can make a fair judgement comparing LSTM and ARIMA as the train:test split ratio would be the same.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[72]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># set seed to ensure determinism and reproduceability (always retest from here)</span>
<span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'TF_DETERMINISTIC_OPS'</span><span class="p">]</span> <span class="o">=</span> <span class="s1">'1'</span>
<span class="n">tf</span><span class="o">.</span><span class="n">keras</span><span class="o">.</span><span class="n">utils</span><span class="o">.</span><span class="n">set_random_seed</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
<span class="n">tf</span><span class="o">.</span><span class="n">config</span><span class="o">.</span><span class="n">experimental</span><span class="o">.</span><span class="n">enable_op_determinism</span><span class="p">()</span>

<span class="c1"># print(series_monthly_mean_temp)</span>
<span class="n">df_monthly_mean_temp</span> <span class="o">=</span> <span class="n">series_monthly_mean_temp</span><span class="o">.</span><span class="n">to_frame</span><span class="p">()</span>  <span class="c1"># Convert Series to DataFrame</span>
<span class="c1"># print(df_monthly_mean_temp)</span>
<span class="n">scaler</span> <span class="o">=</span> <span class="n">MinMaxScaler</span><span class="p">()</span>
<span class="n">scaler</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">df_monthly_mean_temp</span><span class="p">)</span>
<span class="n">df_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">scaler</span><span class="o">.</span><span class="n">transform</span><span class="p">(</span><span class="n">df_monthly_mean_temp</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">shape</span><span class="p">)</span>

<span class="c1"># Create a new DataFrame with the normalized values</span>
<span class="n">df_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="p">,</span> <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">'normalised'</span><span class="p">],</span> <span class="n">index</span><span class="o">=</span><span class="n">df_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">)</span>
<span class="c1"># print(df_normalised)</span>
<span class="n">mean_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">df_normalised_monthly_mean_temp</span><span class="p">[</span><span class="s1">'normalised'</span><span class="p">]</span><span class="o">.</span><span class="n">mean</span><span class="p">()</span>

<span class="c1"># Plot the normalized data</span>
<span class="n">fig_normalised_monthly_mean_temp</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">df_normalised_monthly_mean_temp</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Normalised'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Normalised Mean Temperature'</span><span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M12'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.2</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Normalised Value: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">fig_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_normalised_monthly_mean_temp</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">df_normalised_monthly_mean_temp</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_normalised_monthly_mean_temp</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="c1"># fig_normalised_monthly_mean_temp.show()</span>

<span class="c1"># split to test 1 year of data</span>
<span class="n">train_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2022</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">test_end</span> <span class="o">=</span> <span class="n">datetime</span><span class="p">(</span><span class="mi">2023</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">train_data</span> <span class="o">=</span> <span class="n">df_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span>
<span class="n">test_data</span> <span class="o">=</span> <span class="n">df_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span>
<span class="n">train_data_norm</span> <span class="o">=</span> <span class="n">df_normalised_monthly_mean_temp</span><span class="p">[:</span><span class="n">train_end</span><span class="p">]</span><span class="o">.</span><span class="n">values</span>
<span class="n">test_data_norm</span> <span class="o">=</span> <span class="n">df_normalised_monthly_mean_temp</span><span class="p">[</span><span class="n">train_end</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">days</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span><span class="n">test_end</span><span class="p">]</span><span class="o">.</span><span class="n">values</span>

<span class="c1"># print(train_data)</span>
<span class="c1"># print(test_data)</span>
<span class="c1"># print(train_data_norm.shape)</span>
<span class="c1"># print(test_data_norm.shape)</span>

<span class="c1"># define generator</span>
<span class="n">n_input</span> <span class="o">=</span> <span class="mi">12</span>
<span class="n">n_features</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">generator</span> <span class="o">=</span> <span class="n">TimeseriesGenerator</span><span class="p">(</span><span class="n">train_data_norm</span><span class="p">,</span> <span class="n">train_data_norm</span><span class="p">,</span> <span class="n">length</span><span class="o">=</span><span class="n">n_input</span><span class="p">,</span> <span class="n">batch_size</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>

<span class="c1"># define model</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Sequential</span><span class="p">()</span>
<span class="n">model</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">LSTM</span><span class="p">(</span><span class="mi">100</span><span class="p">,</span> <span class="n">activation</span><span class="o">=</span><span class="s1">'tanh'</span><span class="p">,</span> <span class="n">input_shape</span><span class="o">=</span><span class="p">(</span><span class="n">n_input</span><span class="p">,</span> <span class="n">n_features</span><span class="p">)))</span> <span class="c1"># here i used tanh instead of relu to take advantage of cuDNN to speed up training</span>
<span class="n">model</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">Dropout</span><span class="p">(</span><span class="mf">0.5</span><span class="p">))</span>
<span class="n">model</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">Dense</span><span class="p">(</span><span class="mi">1</span><span class="p">))</span>
<span class="c1"># optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)</span>
<span class="n">model</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="n">optimizer</span><span class="o">=</span><span class="n">tf</span><span class="o">.</span><span class="n">keras</span><span class="o">.</span><span class="n">optimizers</span><span class="o">.</span><span class="n">Adam</span><span class="p">(</span><span class="n">learning_rate</span><span class="o">=</span><span class="mf">0.001</span><span class="p">),</span> <span class="n">loss</span><span class="o">=</span><span class="s1">'mse'</span><span class="p">)</span>
<span class="n">model</span><span class="o">.</span><span class="n">summary</span><span class="p">()</span>

<span class="c1"># fit model and save history</span>
<span class="n">history</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">generator</span><span class="p">,</span><span class="n">epochs</span><span class="o">=</span><span class="mi">300</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>(496, 1)
Model: "sequential_1"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 lstm_1 (LSTM)               (None, 100)               40800

 dropout (Dropout)           (None, 100)               0

 dense_1 (Dense)             (None, 1)                 101

=================================================================
Total params: 40,901
Trainable params: 40,901
Non-trainable params: 0
_________________________________________________________________
Epoch 1/300
468/468 [==============================] - 2s 2ms/step - loss: 0.0501
Epoch 2/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0395
Epoch 3/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0369
Epoch 4/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0287
Epoch 5/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0234
Epoch 6/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0223
Epoch 7/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0225
Epoch 8/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0212
Epoch 9/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0211
Epoch 10/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0201
Epoch 11/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0203
Epoch 12/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0193
Epoch 13/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0183
Epoch 14/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0185
Epoch 15/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0180
Epoch 16/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0175
Epoch 17/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0169
Epoch 18/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0176
Epoch 19/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0180
Epoch 20/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0169
Epoch 21/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0174
Epoch 22/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0176
Epoch 23/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0168
Epoch 24/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0165
Epoch 25/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0167
Epoch 26/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0176
Epoch 27/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0157
Epoch 28/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0174
Epoch 29/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0152
Epoch 30/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0163
Epoch 31/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0155
Epoch 32/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0151
Epoch 33/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0154
Epoch 34/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0157
Epoch 35/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0151
Epoch 36/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0153
Epoch 37/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0156
Epoch 38/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0151
Epoch 39/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0145
Epoch 40/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0158
Epoch 41/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0161
Epoch 42/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0149
Epoch 43/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0149
Epoch 44/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0142
Epoch 45/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0143
Epoch 46/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0141
Epoch 47/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0138
Epoch 48/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0140
Epoch 49/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0146
Epoch 50/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0145
Epoch 51/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0144
Epoch 52/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0140
Epoch 53/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0142
Epoch 54/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0142
Epoch 55/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0140
Epoch 56/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0143
Epoch 57/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0134
Epoch 58/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0139
Epoch 59/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0136
Epoch 60/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0137
Epoch 61/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0129
Epoch 62/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0133
Epoch 63/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0136
Epoch 64/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0129
Epoch 65/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0132
Epoch 66/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0134
Epoch 67/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0130
Epoch 68/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0137
Epoch 69/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0140
Epoch 70/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0133
Epoch 71/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0133
Epoch 72/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0130
Epoch 73/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0129
Epoch 74/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0136
Epoch 75/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0125
Epoch 76/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0122
Epoch 77/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0128
Epoch 78/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0128
Epoch 79/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0130
Epoch 80/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0119
Epoch 81/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0131
Epoch 82/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0125
Epoch 83/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0129
Epoch 84/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0131
Epoch 85/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0127
Epoch 86/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0123
Epoch 87/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0124
Epoch 88/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0120
Epoch 89/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0121
Epoch 90/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0122
Epoch 91/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0131
Epoch 92/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0123
Epoch 93/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0127
Epoch 94/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0126
Epoch 95/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0121
Epoch 96/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0122
Epoch 97/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0116
Epoch 98/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0120
Epoch 99/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0118
Epoch 100/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0128
Epoch 101/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0118
Epoch 102/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0118
Epoch 103/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0117
Epoch 104/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0125
Epoch 105/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0120
Epoch 106/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0118
Epoch 107/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0116
Epoch 108/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0113
Epoch 109/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0116
Epoch 110/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0117
Epoch 111/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0116
Epoch 112/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0120
Epoch 113/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0113
Epoch 114/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0114
Epoch 115/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0120
Epoch 116/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0112
Epoch 117/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0117
Epoch 118/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0116
Epoch 119/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0111
Epoch 120/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0115
Epoch 121/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0110
Epoch 122/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0106
Epoch 123/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0110
Epoch 124/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0111
Epoch 125/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0112
Epoch 126/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0110
Epoch 127/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0111
Epoch 128/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0107
Epoch 129/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0112
Epoch 130/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0111
Epoch 131/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0105
Epoch 132/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0106
Epoch 133/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0104
Epoch 134/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0112
Epoch 135/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0105
Epoch 136/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0098
Epoch 137/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0105
Epoch 138/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0106
Epoch 139/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0106
Epoch 140/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0107
Epoch 141/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0105
Epoch 142/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0096
Epoch 143/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0103
Epoch 144/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0102
Epoch 145/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0101
Epoch 146/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0096
Epoch 147/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0095
Epoch 148/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0096
Epoch 149/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0102
Epoch 150/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0092
Epoch 151/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0095
Epoch 152/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0099
Epoch 153/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0092
Epoch 154/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0094
Epoch 155/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0093
Epoch 156/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0091
Epoch 157/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0083
Epoch 158/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0089
Epoch 159/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0093
Epoch 160/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0085
Epoch 161/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0096
Epoch 162/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0091
Epoch 163/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0086
Epoch 164/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0091
Epoch 165/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0089
Epoch 166/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0089
Epoch 167/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0084
Epoch 168/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0085
Epoch 169/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0083
Epoch 170/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0085
Epoch 171/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0085
Epoch 172/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0080
Epoch 173/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0080
Epoch 174/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0081
Epoch 175/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0085
Epoch 176/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0084
Epoch 177/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0083
Epoch 178/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0082
Epoch 179/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0080
Epoch 180/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0077
Epoch 181/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0076
Epoch 182/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0075
Epoch 183/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0077
Epoch 184/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0073
Epoch 185/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0073
Epoch 186/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0072
Epoch 187/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0077
Epoch 188/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0081
Epoch 189/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0073
Epoch 190/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0072
Epoch 191/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0075
Epoch 192/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0072
Epoch 193/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0077
Epoch 194/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0071
Epoch 195/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0074
Epoch 196/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0069
Epoch 197/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0074
Epoch 198/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0069
Epoch 199/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0070
Epoch 200/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0067
Epoch 201/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0071
Epoch 202/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0071
Epoch 203/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0072
Epoch 204/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0071
Epoch 205/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0066
Epoch 206/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0065
Epoch 207/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0070
Epoch 208/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0074
Epoch 209/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0065
Epoch 210/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0063
Epoch 211/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0068
Epoch 212/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0067
Epoch 213/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0059
Epoch 214/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0067
Epoch 215/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0059
Epoch 216/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0059
Epoch 217/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0060
Epoch 218/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0058
Epoch 219/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0058
Epoch 220/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0064
Epoch 221/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0060
Epoch 222/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0055
Epoch 223/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0053
Epoch 224/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0056
Epoch 225/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0056
Epoch 226/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0052
Epoch 227/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0049
Epoch 228/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0054
Epoch 229/300
468/468 [==============================] - 2s 3ms/step - loss: 0.0055
Epoch 230/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0053
Epoch 231/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0054
Epoch 232/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0052
Epoch 233/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0052
Epoch 234/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0052
Epoch 235/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0055
Epoch 236/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0049
Epoch 237/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0052
Epoch 238/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0051
Epoch 239/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0052
Epoch 240/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0050
Epoch 241/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0042
Epoch 242/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0051
Epoch 243/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0047
Epoch 244/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0044
Epoch 245/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0043
Epoch 246/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0051
Epoch 247/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0045
Epoch 248/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0048
Epoch 249/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0047
Epoch 250/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0041
Epoch 251/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0050
Epoch 252/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0041
Epoch 253/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0043
Epoch 254/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0042
Epoch 255/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0047
Epoch 256/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0040
Epoch 257/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0041
Epoch 258/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 259/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0039
Epoch 260/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0038
Epoch 261/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0040
Epoch 262/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0037
Epoch 263/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0039
Epoch 264/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0035
Epoch 265/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0031
Epoch 266/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0041
Epoch 267/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 268/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0037
Epoch 269/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0039
Epoch 270/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0034
Epoch 271/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0034
Epoch 272/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 273/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0035
Epoch 274/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0036
Epoch 275/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 276/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 277/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0030
Epoch 278/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0031
Epoch 279/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0031
Epoch 280/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0031
Epoch 281/300
468/468 [==============================] - 1s 3ms/step - loss: 0.0032
Epoch 282/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0029
Epoch 283/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0026
Epoch 284/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0029
Epoch 285/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0031
Epoch 286/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0032
Epoch 287/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 288/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0027
Epoch 289/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0025
Epoch 290/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0028
Epoch 291/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0033
Epoch 292/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0027
Epoch 293/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0027
Epoch 294/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0029
Epoch 295/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0027
Epoch 296/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0029
Epoch 297/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0031
Epoch 298/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0024
Epoch 299/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0026
Epoch 300/300
468/468 [==============================] - 1s 2ms/step - loss: 0.0027
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[73]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># Get loss history</span>
<span class="n">loss</span> <span class="o">=</span> <span class="n">history</span><span class="o">.</span><span class="n">history</span><span class="p">[</span><span class="s1">'loss'</span><span class="p">]</span>

<span class="c1"># print(f"training loss: {loss}")</span>

<span class="c1"># Find the epoch with the minimum loss </span>
<span class="n">min_loss_epoch</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">argmin</span><span class="p">(</span><span class="n">loss</span><span class="p">)</span> <span class="o">+</span> <span class="mi">1</span>
<span class="n">min_loss</span> <span class="o">=</span> <span class="n">loss</span><span class="p">[</span><span class="n">min_loss_epoch</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Minimum training loss: </span><span class="si">&#123</span><span class="n">min_loss</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Epoch with minimum training loss: </span><span class="si">&#123</span><span class="n">min_loss_epoch</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>

<span class="c1"># Create DataFrame</span>
<span class="n">epochs</span> <span class="o">=</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">len</span><span class="p">(</span><span class="n">loss</span><span class="p">)</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span>
<span class="n">loss_df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'epoch'</span><span class="p">:</span> <span class="n">epochs</span><span class="p">,</span> <span class="s1">'training_loss'</span><span class="p">:</span> <span class="n">loss</span><span class="p">})</span>

<span class="c1"># Plot loss</span>
<span class="n">fig_loss</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">loss_df</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'epoch'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'training_loss'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Loss'</span><span class="p">,</span> <span class="s1">'epoch'</span><span class="p">:</span> <span class="s1">'Epoch'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Training Loss'</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Epoch: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Loss: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>
<span class="n">fig_loss</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Minimum training loss: 0.002400761004537344
Epoch with minimum training loss: 298
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_73.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[74]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="n">predictions_norm</span> <span class="o">=</span> <span class="p">[]</span>

<span class="n">first_eval_batch</span> <span class="o">=</span> <span class="n">train_data_norm</span><span class="p">[</span><span class="o">-</span><span class="n">n_input</span><span class="p">:]</span>
<span class="n">current_batch</span> <span class="o">=</span> <span class="n">first_eval_batch</span><span class="o">.</span><span class="n">reshape</span><span class="p">((</span><span class="mi">1</span><span class="p">,</span> <span class="n">n_input</span><span class="p">,</span> <span class="n">n_features</span><span class="p">))</span>

<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">test_data</span><span class="p">)):</span>

    <span class="c1"># get the prediction value for the first batch</span>
    <span class="n">current_pred</span> <span class="o">=</span> <span class="n">model</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">current_batch</span><span class="p">)[</span><span class="mi">0</span><span class="p">]</span>

    <span class="c1"># append the prediction into the array</span>
    <span class="n">predictions_norm</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">current_pred</span><span class="p">)</span>

    <span class="c1"># use the prediction to update the batch and remove the first value</span>
    <span class="n">current_batch</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">current_batch</span><span class="p">[:,</span><span class="mi">1</span><span class="p">:,:],[[</span><span class="n">current_pred</span><span class="p">]],</span><span class="n">axis</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>

<span class="n">predictions</span> <span class="o">=</span> <span class="n">scaler</span><span class="o">.</span><span class="n">inverse_transform</span><span class="p">(</span><span class="n">predictions_norm</span><span class="p">)</span>

<span class="n">residuals</span> <span class="o">=</span> <span class="n">test_data</span> <span class="o">-</span> <span class="n">predictions</span>

<span class="c1"># print(type(residuals))</span>
<span class="c1"># print(type(residuals))</span>

<span class="c1"># Plot residuals</span>
<span class="n">fig_resid</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Error'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Residuals from LSTM Model'</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s1">'error'</span><span class="p">,</span> <span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Error: %</span><span class="si">&#123y}</span><span class="s1">'</span><span class="p">)</span>

<span class="c1"># add the mean line</span>
<span class="n">mean_error</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="p">,</span> <span class="n">axis</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>
<span class="c1"># print(mean_error)</span>
<span class="c1"># print(type(mean_error))</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">add_shape</span><span class="p">(</span>
    <span class="nb">type</span><span class="o">=</span><span class="s2">"line"</span><span class="p">,</span>
    <span class="n">x0</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
    <span class="n">y0</span><span class="o">=</span><span class="n">mean_error</span><span class="o">.</span><span class="n">values</span><span class="p">,</span>
    <span class="n">x1</span><span class="o">=</span><span class="n">residuals</span><span class="o">.</span><span class="n">index</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="n">y1</span><span class="o">=</span><span class="n">mean_error</span><span class="o">.</span><span class="n">values</span><span class="p">,</span>
    <span class="n">line</span><span class="o">=</span><span class="nb">dict</span><span class="p">(</span><span class="n">color</span><span class="o">=</span><span class="s2">"red"</span><span class="p">,</span> <span class="n">dash</span><span class="o">=</span><span class="s2">"dot"</span><span class="p">),</span>
<span class="p">)</span>
<span class="n">fig_resid</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>1/1 [==============================] - 0s 247ms/step
1/1 [==============================] - 0s 12ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
1/1 [==============================] - 0s 11ms/step
</pre>
                        </div>
                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_74.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing code_cell rendered">
            <div class="input">
                <div class="prompt input_prompt">In&nbsp;[75]:</div>
                <div class="inner_cell">
                    <div class="input_area">
                        <div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># print(test_data_no_norm.index)</span>

<span class="n">plot_data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">index</span><span class="p">,</span> <span class="s1">'test_data'</span><span class="p">:</span> <span class="n">test_data</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">flatten</span><span class="p">(),</span> <span class="s1">'predictions'</span><span class="p">:</span> <span class="n">predictions</span><span class="o">.</span><span class="n">flatten</span><span class="p">()})</span>
<span class="c1"># print(plot_data)</span>
<span class="n">fig_pred_test</span> <span class="o">=</span> <span class="n">px</span><span class="o">.</span><span class="n">line</span><span class="p">(</span><span class="n">plot_data</span><span class="p">,</span> <span class="n">x</span><span class="o">=</span><span class="s1">'datetime'</span><span class="p">,</span> <span class="n">y</span><span class="o">=</span><span class="p">[</span><span class="s1">'test_data'</span><span class="p">,</span> <span class="s1">'predictions'</span><span class="p">],</span> <span class="n">labels</span><span class="o">=</span><span class="p">&#123</span><span class="s1">'datetime'</span><span class="p">:</span> <span class="s1">'Datetime'</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="s1">'Mean Temperature (°C)'</span><span class="p">},</span> <span class="n">title</span><span class="o">=</span><span class="s1">'Test Data and Predictions'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_xaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="s1">'M1'</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_yaxes</span><span class="p">(</span><span class="n">dtick</span><span class="o">=</span><span class="mf">0.5</span><span class="p">,</span> <span class="n">tickangle</span><span class="o">=</span><span class="mi">45</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">update_traces</span><span class="p">(</span><span class="n">hovertemplate</span><span class="o">=</span><span class="s1">'Datetime: %</span><span class="si">&#123x}</span><span class="s1">&lt;br&gt;Mean Temperature: %</span><span class="si">&#123y}</span><span class="s1">°C'</span><span class="p">)</span>
<span class="n">fig_pred_test</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Mean Absolute Percent Error: </span><span class="si">&#123</span><span class="nb">round</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">residuals</span><span class="o">/</span><span class="n">test_data</span><span class="p">),</span><span class="w"> </span><span class="n">axis</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span><span class="o">.</span><span class="n">item</span><span class="p">(),</span><span class="w"> </span><span class="mi">4</span><span class="p">)</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Root Mean Squared Error: </span><span class="si">&#123</span><span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">mean</span><span class="p">(</span><span class="n">residuals</span><span class="o">**</span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span class="n">axis</span><span class="o">=</span><span class="mi">0</span><span class="p">))</span><span class="o">.</span><span class="n">item</span><span class="p">()</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</pre></div>

                    </div>
                </div>
            </div>

            <div class="output_wrapper">
                <div class="output">


                    <div class="output_area">

                        <div class="prompt"></div>



                        <div class="output_html rendered_html output_subarea ">
                            <iframe scrolling="no" width="100%" height="545px" src="model_iframe_figures/figure_75.html" frameborder="0" allowfullscreen=""></iframe>

                        </div>

                    </div>

                    <div class="output_area">

                        <div class="prompt"></div>


                        <div class="output_subarea output_stream output_stdout output_text">
<pre>Mean Absolute Percent Error: 0.0128
Root Mean Squared Error: 0.44115552418544135
</pre>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>lr=0.001<br>No Dropout<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0145
                    Root Mean Squared Error: 0.463736843202713</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0125
                    Root Mean Squared Error: 0.4086067127565924</p>
                <p><strong>LSTM(300 epochs):</strong>
                    Mean Absolute Percent Error: 0.0161
                    Root Mean Squared Error: 0.49609234464576174</p>
                <p><strong>LSTM(400 epochs):</strong>
                    Mean Absolute Percent Error: 0.0215
                    Root Mean Squared Error: 0.7295606305187063</p>
                <p><strong>LSTM(500 epochs):</strong>
                    Mean Absolute Percent Error: 0.0186
                    Root Mean Squared Error: 0.6123747241425901</p>
                <p><strong>lr=0.001<br>Dropout=0.2<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0109
                    Root Mean Squared Error: 0.38060867079652533</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0232
                    Root Mean Squared Error: 0.8178379230143739</p>
                <p><strong>LSTM(300 epochs):</strong>
                    Mean Absolute Percent Error: 0.021
                    Root Mean Squared Error: 0.7211043996734204</p>
                <p><strong>LSTM(400 epochs):</strong>
                    Mean Absolute Percent Error: 0.0253
                    Root Mean Squared Error: 0.8241299234489794</p>
                <p><strong>LSTM(500 epochs):</strong>
                    Mean Absolute Percent Error: 0.0241
                    Root Mean Squared Error: 0.7807227061381148</p>
                <p><strong>lr=0.001<br>Dropout=0.5<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0093
                    Root Mean Squared Error: 0.35471921266149</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.019
                    Root Mean Squared Error: 0.6217788733394394</p>
                <p><strong>LSTM(300 epochs):</strong>
                    Mean Absolute Percent Error: 0.0128
                    Root Mean Squared Error: 0.44115552418544135</p>
                <p><strong>LSTM(400 epochs):</strong>
                    Mean Absolute Percent Error: 0.0199
                    Root Mean Squared Error: 0.6535082465484656</p>
                <p><strong>LSTM(500 epochs):</strong>
                    Mean Absolute Percent Error: 0.0167
                    Root Mean Squared Error: 0.5266831014363483</p>
                <p><strong>lr=0.001<br>Dropout=0.8<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0116
                    Root Mean Squared Error: 0.4013852371897046</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0131
                    Root Mean Squared Error: 0.4403628214828945</p>
                <p><strong>LSTM(300 epochs):</strong>
                    Mean Absolute Percent Error: 0.0176
                    Root Mean Squared Error: 0.5717841047326412</p>
                <p><strong>LSTM(400 epochs):</strong>
                    Mean Absolute Percent Error: 0.0229
                    Root Mean Squared Error: 0.72180557066981</p>
                <p><strong>LSTM(500 epochs):</strong>
                    Mean Absolute Percent Error: 0.0226
                    Root Mean Squared Error: 0.733328831209713</p>
                <p><strong>lr=0.01<br>No Dropout<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0146
                    Root Mean Squared Error: 0.5309802458123353</p>
                <p><strong>LSTM(200 epochs, still converging too slowly):</strong>
                    Mean Absolute Percent Error: 0.0297
                    Root Mean Squared Error: 1.010809026151784</p>
                <p><strong>lr=0.02<br>No Dropout<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0216
                    Root Mean Squared Error: 0.6944600408737768</p>
                <p><strong>LSTM(200 epochs, converging too fast):</strong>
                    Mean Absolute Percent Error: 0.0163
                    Root Mean Squared Error: 0.6073242624178974</p>
                <p><strong>lr=0.02<br>Dropout=0.2<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0215
                    Root Mean Squared Error: 0.6796303223036045</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.016
                    Root Mean Squared Error: 0.6058329055575409</p>
                <p><strong>lr=0.001<br>Dropout=0.5<br>Timestep=24<br>LSTM(100 epochs):</strong>
                    Mean Absolute Percent Error: 0.0143
                    Root Mean Squared Error: 0.45955529939231915</p>
                <p><strong>LSTM(200 epochs):</strong>
                    Mean Absolute Percent Error: 0.0169
                    Root Mean Squared Error: 0.5664092616646981</p>
                <p><strong>LSTM(300 epochs):</strong>
                    Mean Absolute Percent Error: 0.018
                    Root Mean Squared Error: 0.6234701666336724</p>
                <p><strong>LSTM(400 epochs):</strong>
                    Mean Absolute Percent Error: 0.0177
                    Root Mean Squared Error: 0.6411966596634251</p>
                <p><strong>LSTM(500 epochs):</strong>
                    Mean Absolute Percent Error: 0.0212
                    Root Mean Squared Error: 0.7293233216596274</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <h3 id="Model-Evaluation" data-toc-modified-id="Model-Evaluation-1.0.8"><a class="toc-mod-link" id="Model-Evaluation-1.0.8"></a><span class="toc-item-num">1.0.8&nbsp;&nbsp;</span>Model Evaluation<a class="anchor-link" href="#Model-Evaluation">¶</a></h3>
            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>After much tinkering, I have found out that dropout=0.5 was better than dropout=0.2, turns out dropout can improve predictions. However, I could not find the right parameters such that it would result in near perfect predictions. Hence, after much analysis, I have decided to go with the standard <strong>lr=0.001, dropout=0.5, timestep=12, 300 epochs</strong>. Although at 100 epochs, it would give me the lowest RMSE I have ever acheived (0.354719), the shape had a gentle trend and did not follow the shape of the test data very closely (much spikier), thus I deduced it was underfitting too much. This coincided with the fact that the training loss was still decreasing at a significant rate at epoch 100. Thus I decided to use epoch 300 instead. Despite its RMSE being higher, its shape followed closer to that of the test data, with the exception of Jun 2022, where it significantly underpredicted the temperature. For some reason, looking at the data, there is always that dip in temperature during June. According to sources, this could be due to the Southwest Monsoon. However, our model failed to learn about this.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p>As to whether to use LSTM or the ARIMA series, I have decide to go with the LSTM model (the one stated above) as its prediction results are more or less comparable with that of the ARIMA series. The ARIMA series also has its downsides: I realised that although its predictions follow the shape of the test data, they are somewhat lagging behind/after, with alternating over and underpredictions. Additionally, LSTM has an advantage over ARIMA wherby it can predict over longer ranges much quicker. With the rolling forecast origin, ARIMA models take a very long time to predict data in the long term e.g. 5, 10 years.</p>

            </div>
        </div>
        </div>
        <div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
        </div><div class="inner_cell">
            <div class="text_cell_render border-box-sizing rendered_html">
                <p><strong>Final model chosen:</strong> LSTM (activation=tanh, loss metric=mse) train on entire data, lr=0.001, dropout=0.5, timestep=12, 300 epochs.</p>

            </div>
        </div>
        </div>
    </div>
</div>
</body>
</html>

<style lang="postcss">
    html {
        font-family: sans-serif;
        -ms-text-size-adjust: 100%;
        -webkit-text-size-adjust: 100%;
    }

    body {
        margin: 0;
    }

    article,
    aside,
    details,
    figcaption,
    figure,
    footer,
    header,
    hgroup,
    main,
    menu,
    nav,
    section,
    summary {
        display: block;
    }

    audio,
    canvas,
    progress,
    video {
        display: inline-block;
        vertical-align: baseline;
    }

    audio:not([controls]) {
        display: none;
        height: 0;
    }

    [hidden],
    template {
        display: none;
    }

    a {
        background-color: transparent;
    }

    a:active,
    a:hover {
        outline: 0;
    }

    abbr[title] {
        border-bottom: 1px dotted;
    }

    b,
    strong {
        font-weight: bold;
    }

    dfn {
        font-style: italic;
    }

    h1 {
        font-size: 2em;
        margin: 0.67em 0;
    }

    mark {
        background: #ff0;
        color: #000;
    }

    small {
        font-size: 80%;
    }

    sub,
    sup {
        font-size: 75%;
        line-height: 0;
        position: relative;
        vertical-align: baseline;
    }

    sup {
        top: -0.5em;
    }

    sub {
        bottom: -0.25em;
    }

    img {
        border: 0;
    }

    svg:not(:root) {
        overflow: hidden;
    }

    figure {
        margin: 1em 40px;
    }

    hr {
        box-sizing: content-box;
        height: 0;
    }

    pre {
        overflow: auto;
    }

    code,
    kbd,
    pre,
    samp {
        font-family: monospace, monospace;
        font-size: 1em;
    }

    button,
    input,
    optgroup,
    select,
    textarea {
        color: inherit;
        font: inherit;
        margin: 0;
    }

    button {
        overflow: visible;
    }

    button,
    select {
        text-transform: none;
    }

    button,
    html input[type="button"],
    input[type="reset"],
    input[type="submit"] {
        -webkit-appearance: button;
        cursor: pointer;
    }

    button[disabled],
    html input[disabled] {
        cursor: default;
    }

    button::-moz-focus-inner,
    input::-moz-focus-inner {
        border: 0;
        padding: 0;
    }

    input {
        line-height: normal;
    }

    input[type="checkbox"],
    input[type="radio"] {
        box-sizing: border-box;
        padding: 0;
    }

    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        height: auto;
    }

    input[type="search"] {
        -webkit-appearance: textfield;
        box-sizing: content-box;
    }

    input[type="search"]::-webkit-search-cancel-button,
    input[type="search"]::-webkit-search-decoration {
        -webkit-appearance: none;
    }

    fieldset {
        border: 1px solid #c0c0c0;
        margin: 0 2px;
        padding: 0.35em 0.625em 0.75em;
    }

    legend {
        border: 0;
        padding: 0;
    }

    textarea {
        overflow: auto;
    }

    optgroup {
        font-weight: bold;
    }

    table {
        border-collapse: collapse;
        border-spacing: 0;
    }

    td,
    th {
        padding: 0;
    }

    /*! Source: https://github.com/h5bp/html5-boilerplate/blob/master/src/css/main.css */
    @media print {
        *,
        *:before,
        *:after {
            background: transparent !important;
            box-shadow: none !important;
            text-shadow: none !important;
        }

        a,
        a:visited {
            text-decoration: underline;
        }

        a[href]:after {
            content: " (" attr(href) ")";
        }

        abbr[title]:after {
            content: " (" attr(title) ")";
        }

        a[href^="#"]:after,
        a[href^="javascript:"]:after {
            content: "";
        }

        pre,
        blockquote {
            border: 1px solid #999;
            page-break-inside: avoid;
        }

        thead {
            display: table-header-group;
        }

        tr,
        img {
            page-break-inside: avoid;
        }

        img {
            max-width: 100% !important;
        }

        p,
        h2,
        h3 {
            orphans: 3;
            widows: 3;
        }

        h2,
        h3 {
            page-break-after: avoid;
        }

        .navbar {
            display: none;
        }

        .btn > .caret,
        .dropup > .btn > .caret {
            border-top-color: #000 !important;
        }

        .label {
            border: 1px solid #000;
        }

        .table {
            border-collapse: collapse !important;
        }

        .table td,
        .table th {
            background-color: #fff !important;
        }

        .table-bordered th,
        .table-bordered td {
            border: 1px solid #ddd !important;
        }
    }

    @font-face {
        font-family: 'Glyphicons Halflings';
        src: url('../components/bootstrap/fonts/glyphicons-halflings-regular.eot');
        src: url('../components/bootstrap/fonts/glyphicons-halflings-regular.eot?#iefix') format('embedded-opentype'), url('../components/bootstrap/fonts/glyphicons-halflings-regular.woff2') format('woff2'), url('../components/bootstrap/fonts/glyphicons-halflings-regular.woff') format('woff'), url('../components/bootstrap/fonts/glyphicons-halflings-regular.ttf') format('truetype'), url('../components/bootstrap/fonts/glyphicons-halflings-regular.svg#glyphicons_halflingsregular') format('svg');
    }

    * {
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }

    *:before,
    *:after {
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }

    html {
        /*font-size: 10px;*/
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }

    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 13px;
        line-height: 1.42857143;
        color: #000;
        background-color: #fff;
    }

    input,
    button,
    select,
    textarea {
        font-family: inherit;
        font-size: inherit;
        line-height: inherit;
    }

    a {
        color: #337ab7;
        text-decoration: none;
    }

    a:hover,
    a:focus {
        color: #23527c;
        text-decoration: underline;
    }

    a:focus {
        outline: 5px auto -webkit-focus-ring-color;
        outline-offset: -2px;
    }

    figure {
        margin: 0;
    }

    img {
        vertical-align: middle;
    }

    hr {
        margin-top: 18px;
        margin-bottom: 18px;
        border: 0;
        border-top: 1px solid #eeeeee;
    }

    [role="button"] {
        cursor: pointer;
    }

    p {
        margin: 0 0 9px;
    }

    @media (min-width: 768px) {
    }

    ul,
    ol {
        margin-top: 0;
        margin-bottom: 9px;
    }

    ul ul,
    ol ul,
    ul ol,
    ol ol {
        margin-bottom: 0;
    }

    .list-inline > li {
        display: inline-block;
        padding-left: 5px;
        padding-right: 5px;
    }

    dl {
        margin-top: 0;
        margin-bottom: 18px;
    }

    dt,
    dd {
        line-height: 1.42857143;
    }

    dt {
        font-weight: bold;
    }

    dd {
        margin-left: 0;
    }

    @media (min-width: 541px) {
        .dl-horizontal dt {
            float: left;
            width: 160px;
            clear: left;
            text-align: right;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .dl-horizontal dd {
            margin-left: 180px;
        }
    }

    abbr[title],
    abbr[data-original-title] {
        cursor: help;
        border-bottom: 1px dotted #777777;
    }

    blockquote {
        padding: 9px 18px;
        margin: 0 0 18px;
        font-size: inherit;
        border-left: 5px solid #eeeeee;
    }

    blockquote p:last-child,
    blockquote ul:last-child,
    blockquote ol:last-child {
        margin-bottom: 0;
    }

    address {
        margin-bottom: 18px;
        font-style: normal;
        line-height: 1.42857143;
    }

    code,
    kbd,
    pre,
    samp {
        font-family: monospace;
    }

    code {
        padding: 2px 4px;
        font-size: 90%;
        color: #c7254e;
        background-color: #f9f2f4;
        border-radius: 2px;
    }

    kbd {
        padding: 2px 4px;
        font-size: 90%;
        color: #888;
        background-color: transparent;
        border-radius: 1px;
        box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.25);
    }

    kbd kbd {
        padding: 0;
        font-size: 100%;
        font-weight: bold;
        box-shadow: none;
    }

    pre {
        display: block;
        padding: 8.5px;
        margin: 0 0 9px;
        font-size: 12px;
        line-height: 1.42857143;
        word-break: break-all;
        word-wrap: break-word;
        color: #333333;
        background-color: #f5f5f5;
        border: 1px solid #ccc;
        border-radius: 2px;
    }

    pre code {
        padding: 0;
        font-size: inherit;
        color: inherit;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
    }

    .container {
        margin-right: auto;
        margin-left: auto;
        padding-left: 0px;
        padding-right: 0px;
    }

    @media (min-width: 768px) {
        .container {
            width: 768px;
        }
    }

    @media (min-width: 992px) {
        .container {
            width: 940px;
        }
    }

    @media (min-width: 1200px) {
        .container {
            width: 1140px;
        }
    }

    @media (min-width: 768px) {

    }

    @media (min-width: 992px) {

    }

    @media (min-width: 1200px) {

    }

    table {
        background-color: transparent;
    }

    caption {
        padding-top: 8px;
        padding-bottom: 8px;
        color: #777777;
        text-align: left;
    }

    th {
        text-align: left;
    }

    .table > thead > tr > th,
    .table > tbody > tr > th,
    .table > tfoot > tr > th,
    .table > thead > tr > td,
    .table > tbody > tr > td,
    .table > tfoot > tr > td {
        padding: 8px;
        line-height: 1.42857143;
        vertical-align: top;
        border-top: 1px solid #ddd;
    }

    .table > thead > tr > th {
        vertical-align: bottom;
        border-bottom: 2px solid #ddd;
    }

    .table > caption + thead > tr:first-child > th,
    .table > colgroup + thead > tr:first-child > th,
    .table > thead:first-child > tr:first-child > th,
    .table > caption + thead > tr:first-child > td,
    .table > colgroup + thead > tr:first-child > td,
    .table > thead:first-child > tr:first-child > td {
        border-top: 0;
    }

    .table > tbody + tbody {
        border-top: 2px solid #ddd;
    }

    .table-condensed > thead > tr > th,
    .table-condensed > tbody > tr > th,
    .table-condensed > tfoot > tr > th,
    .table-condensed > thead > tr > td,
    .table-condensed > tbody > tr > td,
    .table-condensed > tfoot > tr > td {
        padding: 5px;
    }

    .table-bordered > thead > tr > th,
    .table-bordered > tbody > tr > th,
    .table-bordered > tfoot > tr > th,
    .table-bordered > thead > tr > td,
    .table-bordered > tbody > tr > td,
    .table-bordered > tfoot > tr > td {
        border: 1px solid #ddd;
    }

    .table-bordered > thead > tr > th,
    .table-bordered > thead > tr > td {
        border-bottom-width: 2px;
    }

    .table-striped > tbody > tr:nth-of-type(odd) {
        background-color: #f9f9f9;
    }

    .table-hover > tbody > tr:hover {
        background-color: #f5f5f5;
    }

    table col[class*="col-"] {
        position: static;
        float: none;
        display: table-column;
    }

    table td[class*="col-"],
    table th[class*="col-"] {
        position: static;
        float: none;
        display: table-cell;
    }

    @media screen and (max-width: 767px) {

        .table-responsive > .table > thead > tr > th,
        .table-responsive > .table > tbody > tr > th,
        .table-responsive > .table > tfoot > tr > th,
        .table-responsive > .table > thead > tr > td,
        .table-responsive > .table > tbody > tr > td,
        .table-responsive > .table > tfoot > tr > td {
            white-space: nowrap;
        }

        .table-responsive > .table-bordered > thead > tr > th:first-child,
        .table-responsive > .table-bordered > tbody > tr > th:first-child,
        .table-responsive > .table-bordered > tfoot > tr > th:first-child,
        .table-responsive > .table-bordered > thead > tr > td:first-child,
        .table-responsive > .table-bordered > tbody > tr > td:first-child,
        .table-responsive > .table-bordered > tfoot > tr > td:first-child {
            border-left: 0;
        }

        .table-responsive > .table-bordered > thead > tr > th:last-child,
        .table-responsive > .table-bordered > tbody > tr > th:last-child,
        .table-responsive > .table-bordered > tfoot > tr > th:last-child,
        .table-responsive > .table-bordered > thead > tr > td:last-child,
        .table-responsive > .table-bordered > tbody > tr > td:last-child,
        .table-responsive > .table-bordered > tfoot > tr > td:last-child {
            border-right: 0;
        }

        .table-responsive > .table-bordered > tbody > tr:last-child > th,
        .table-responsive > .table-bordered > tfoot > tr:last-child > th,
        .table-responsive > .table-bordered > tbody > tr:last-child > td,
        .table-responsive > .table-bordered > tfoot > tr:last-child > td {
            border-bottom: 0;
        }
    }

    fieldset {
        padding: 0;
        margin: 0;
        border: 0;
        min-width: 0;
    }

    legend {
        display: block;
        width: 100%;
        padding: 0;
        margin-bottom: 18px;
        font-size: 19.5px;
        line-height: inherit;
        color: #333333;
        border: 0;
        border-bottom: 1px solid #e5e5e5;
    }

    label {
        display: inline-block;
        max-width: 100%;
        margin-bottom: 5px;
        font-weight: bold;
    }

    input[type="search"] {
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }

    input[type="radio"],
    input[type="checkbox"] {
        margin: 4px 0 0;
        margin-top: 1px \9;
        line-height: normal;
    }

    input[type="file"] {
        display: block;
    }

    input[type="range"] {
        display: block;
        width: 100%;
    }

    select[multiple],
    select[size] {
        height: auto;
    }

    input[type="file"]:focus,
    input[type="radio"]:focus,
    input[type="checkbox"]:focus {
        outline: 5px auto -webkit-focus-ring-color;
        outline-offset: -2px;
    }

    output {
        display: block;
        padding-top: 7px;
        font-size: 13px;
        line-height: 1.42857143;
        color: #555555;
    }

    input[type="search"] {
        -webkit-appearance: none;
    }

    @media screen and (-webkit-min-device-pixel-ratio: 0) {

    }

    .radio label,
    .checkbox label {
        min-height: 18px;
        padding-left: 20px;
        margin-bottom: 0;
        font-weight: normal;
        cursor: pointer;
    }

    .radio input[type="radio"],
    .radio-inline input[type="radio"],
    .checkbox input[type="checkbox"],
    .checkbox-inline input[type="checkbox"] {
        position: absolute;
        margin-left: -20px;
        margin-top: 4px \9;
    }

    .radio.disabled label,
    .checkbox.disabled label,
    fieldset[disabled] .radio label,
    fieldset[disabled] .checkbox label {
        cursor: not-allowed;
    }

    @media (min-width: 768px) {

        .form-inline .radio label,
        .form-inline .checkbox label {
            padding-left: 0;
        }

        .form-inline .radio input[type="radio"],
        .form-inline .checkbox input[type="checkbox"] {
            position: relative;
            margin-left: 0;
        }

    }

    @media (min-width: 768px) {
    }

    @media (min-width: 768px) {
    }

    @media (min-width: 768px) {
    }

    .dropdown-menu > li > a {
        display: block;
        padding: 3px 20px;
        clear: both;
        font-weight: normal;
        line-height: 1.42857143;
        color: #333333;
        white-space: nowrap;
    }

    .dropdown-menu > li > a:hover,
    .dropdown-menu > li > a:focus {
        text-decoration: none;
        color: #262626;
        background-color: #f5f5f5;
    }

    .dropdown-menu > .active > a,
    .dropdown-menu > .active > a:hover,
    .dropdown-menu > .active > a:focus {
        color: #fff;
        text-decoration: none;
        outline: 0;
        background-color: #337ab7;
    }

    .dropdown-menu > .disabled > a,
    .dropdown-menu > .disabled > a:hover,
    .dropdown-menu > .disabled > a:focus {
        color: #777777;
    }

    .dropdown-menu > .disabled > a:hover,
    .dropdown-menu > .disabled > a:focus {
        text-decoration: none;
        background-color: transparent;
        background-image: none;
        /*filter: progid:DXImageTransform.Microsoft.gradient(enabled = false);*/
        cursor: not-allowed;
    }

    .open > a {
        outline: 0;
    }

    @media (min-width: 541px) {

    }

    [data-toggle="buttons"] > .btn input[type="radio"],
    [data-toggle="buttons"] > .btn-group > .btn input[type="radio"],
    [data-toggle="buttons"] > .btn input[type="checkbox"],
    [data-toggle="buttons"] > .btn-group > .btn input[type="checkbox"] {
        position: absolute;
        clip: rect(0, 0, 0, 0);
        pointer-events: none;
    }

    .input-group-addon input[type="radio"],
    .input-group-addon input[type="checkbox"] {
        margin-top: 0;
    }

    .nav > li {
        position: relative;
        display: block;
    }

    .nav > li > a {
        position: relative;
        display: block;
        padding: 10px 15px;
    }

    .nav > li > a:hover,
    .nav > li > a:focus {
        text-decoration: none;
        background-color: #eeeeee;
    }

    .nav > li.disabled > a {
        color: #777777;
    }

    .nav > li.disabled > a:hover,
    .nav > li.disabled > a:focus {
        color: #777777;
        text-decoration: none;
        background-color: transparent;
        cursor: not-allowed;
    }

    .nav .open > a,
    .nav .open > a:hover,
    .nav .open > a:focus {
        background-color: #eeeeee;
        border-color: #337ab7;
    }

    .nav > li > a > img {
        max-width: none;
    }

    .nav-tabs > li {
        float: left;
        margin-bottom: -1px;
    }

    .nav-tabs > li > a {
        margin-right: 2px;
        line-height: 1.42857143;
        border: 1px solid transparent;
        border-radius: 2px 2px 0 0;
    }

    .nav-tabs > li > a:hover {
        border-color: #eeeeee #eeeeee #ddd;
    }

    .nav-tabs > li.active > a,
    .nav-tabs > li.active > a:hover,
    .nav-tabs > li.active > a:focus {
        color: #555555;
        background-color: #fff;
        border: 1px solid #ddd;
        border-bottom-color: transparent;
        cursor: default;
    }

    .nav-tabs.nav-justified > li {
        float: none;
    }

    .nav-tabs.nav-justified > li > a {
        text-align: center;
        margin-bottom: 5px;
    }

    @media (min-width: 768px) {
        .nav-tabs.nav-justified > li {
            display: table-cell;
            width: 1%;
        }

        .nav-tabs.nav-justified > li > a {
            margin-bottom: 0;
        }
    }

    .nav-tabs.nav-justified > li > a {
        margin-right: 0;
        border-radius: 2px;
    }

    .nav-tabs.nav-justified > .active > a,
    .nav-tabs.nav-justified > .active > a:hover,
    .nav-tabs.nav-justified > .active > a:focus {
        border: 1px solid #ddd;
    }

    @media (min-width: 768px) {
        .nav-tabs.nav-justified > li > a {
            border-bottom: 1px solid #ddd;
            border-radius: 2px 2px 0 0;
        }

        .nav-tabs.nav-justified > .active > a,
        .nav-tabs.nav-justified > .active > a:hover,
        .nav-tabs.nav-justified > .active > a:focus {
            border-bottom-color: #fff;
        }
    }

    .nav-pills > li {
        float: left;
    }

    .nav-pills > li > a {
        border-radius: 2px;
    }

    .nav-pills > li + li {
        margin-left: 2px;
    }

    .nav-pills > li.active > a,
    .nav-pills > li.active > a:hover,
    .nav-pills > li.active > a:focus {
        color: #fff;
        background-color: #337ab7;
    }

    .nav-stacked > li {
        float: none;
    }

    .nav-stacked > li + li {
        margin-top: 2px;
        margin-left: 0;
    }

    .nav-justified > li {
        float: none;
    }

    .nav-justified > li > a {
        text-align: center;
        margin-bottom: 5px;
    }

    @media (min-width: 768px) {
        .nav-justified > li {
            display: table-cell;
            width: 1%;
        }

        .nav-justified > li > a {
            margin-bottom: 0;
        }
    }

    .nav-tabs-justified > li > a {
        margin-right: 0;
        border-radius: 2px;
    }

    .nav-tabs-justified > .active > a,
    .nav-tabs-justified > .active > a:hover,
    .nav-tabs-justified > .active > a:focus {
        border: 1px solid #ddd;
    }

    @media (min-width: 768px) {
        .nav-tabs-justified > li > a {
            border-bottom: 1px solid #ddd;
            border-radius: 2px 2px 0 0;
        }

        .nav-tabs-justified > .active > a,
        .nav-tabs-justified > .active > a:hover,
        .nav-tabs-justified > .active > a:focus {
            border-bottom-color: #fff;
        }
    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {

    }

    @media (max-device-width: 540px) and (orientation: landscape) {
    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {
    }

    .navbar-brand > img {
        display: block;
    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {
    }

    .navbar-nav > li > a {
        padding-top: 10px;
        padding-bottom: 10px;
        line-height: 18px;
    }

    @media (max-width: 540px) {

        .navbar-nav .open .dropdown-menu > li > a {
            line-height: 18px;
        }

        .navbar-nav .open .dropdown-menu > li > a:hover,
        .navbar-nav .open .dropdown-menu > li > a:focus {
            background-image: none;
        }
    }

    @media (min-width: 541px) {

        .navbar-nav > li {
            float: left;
        }

        .navbar-nav > li > a {
            padding-top: 6px;
            padding-bottom: 6px;
        }
    }

    @media (min-width: 768px) {

        .navbar-form .radio label,
        .navbar-form .checkbox label {
            padding-left: 0;
        }

        .navbar-form .radio input[type="radio"],
        .navbar-form .checkbox input[type="checkbox"] {
            position: relative;
            margin-left: 0;
        }

    }

    @media (max-width: 540px) {

    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {
    }

    @media (min-width: 541px) {

    }

    .navbar-default .navbar-nav > li > a {
        color: #777;
    }

    .navbar-default .navbar-nav > li > a:hover,
    .navbar-default .navbar-nav > li > a:focus {
        color: #333;
        background-color: transparent;
    }

    .navbar-default .navbar-nav > .active > a,
    .navbar-default .navbar-nav > .active > a:hover,
    .navbar-default .navbar-nav > .active > a:focus {
        color: #555;
        background-color: #e7e7e7;
    }

    .navbar-default .navbar-nav > .disabled > a,
    .navbar-default .navbar-nav > .disabled > a:hover,
    .navbar-default .navbar-nav > .disabled > a:focus {
        color: #ccc;
        background-color: transparent;
    }

    .navbar-default .navbar-nav > .open > a,
    .navbar-default .navbar-nav > .open > a:hover,
    .navbar-default .navbar-nav > .open > a:focus {
        background-color: #e7e7e7;
        color: #555;
    }

    @media (max-width: 540px) {
        .navbar-default .navbar-nav .open .dropdown-menu > li > a {
            color: #777;
        }

        .navbar-default .navbar-nav .open .dropdown-menu > li > a:hover,
        .navbar-default .navbar-nav .open .dropdown-menu > li > a:focus {
            color: #333;
            background-color: transparent;
        }

        .navbar-default .navbar-nav .open .dropdown-menu > .active > a,
        .navbar-default .navbar-nav .open .dropdown-menu > .active > a:hover,
        .navbar-default .navbar-nav .open .dropdown-menu > .active > a:focus {
            color: #555;
            background-color: #e7e7e7;
        }

        .navbar-default .navbar-nav .open .dropdown-menu > .disabled > a,
        .navbar-default .navbar-nav .open .dropdown-menu > .disabled > a:hover,
        .navbar-default .navbar-nav .open .dropdown-menu > .disabled > a:focus {
            color: #ccc;
            background-color: transparent;
        }
    }

    .navbar-inverse .navbar-nav > li > a {
        color: #9d9d9d;
    }

    .navbar-inverse .navbar-nav > li > a:hover,
    .navbar-inverse .navbar-nav > li > a:focus {
        color: #fff;
        background-color: transparent;
    }

    .navbar-inverse .navbar-nav > .active > a,
    .navbar-inverse .navbar-nav > .active > a:hover,
    .navbar-inverse .navbar-nav > .active > a:focus {
        color: #fff;
        background-color: #080808;
    }

    .navbar-inverse .navbar-nav > .disabled > a,
    .navbar-inverse .navbar-nav > .disabled > a:hover,
    .navbar-inverse .navbar-nav > .disabled > a:focus {
        color: #444;
        background-color: transparent;
    }

    .navbar-inverse .navbar-nav > .open > a,
    .navbar-inverse .navbar-nav > .open > a:hover,
    .navbar-inverse .navbar-nav > .open > a:focus {
        background-color: #080808;
        color: #fff;
    }

    @media (max-width: 540px) {

        .navbar-inverse .navbar-nav .open .dropdown-menu > li > a {
            color: #9d9d9d;
        }

        .navbar-inverse .navbar-nav .open .dropdown-menu > li > a:hover,
        .navbar-inverse .navbar-nav .open .dropdown-menu > li > a:focus {
            color: #fff;
            background-color: transparent;
        }

        .navbar-inverse .navbar-nav .open .dropdown-menu > .active > a,
        .navbar-inverse .navbar-nav .open .dropdown-menu > .active > a:hover,
        .navbar-inverse .navbar-nav .open .dropdown-menu > .active > a:focus {
            color: #fff;
            background-color: #080808;
        }

        .navbar-inverse .navbar-nav .open .dropdown-menu > .disabled > a,
        .navbar-inverse .navbar-nav .open .dropdown-menu > .disabled > a:hover,
        .navbar-inverse .navbar-nav .open .dropdown-menu > .disabled > a:focus {
            color: #444;
            background-color: transparent;
        }
    }

    .breadcrumb > li {
        display: inline-block;
    }

    .breadcrumb > li + li:before {
        content: "/\00a0";
        padding: 0 5px;
        color: #5e5e5e;
    }

    .pagination > li {
        display: inline;
    }

    .pagination > li > a,
    .pagination > li > span {
        position: relative;
        float: left;
        padding: 6px 12px;
        line-height: 1.42857143;
        text-decoration: none;
        color: #337ab7;
        background-color: #fff;
        border: 1px solid #ddd;
        margin-left: -1px;
    }

    .pagination > li:first-child > a,
    .pagination > li:first-child > span {
        margin-left: 0;
        border-bottom-left-radius: 2px;
        border-top-left-radius: 2px;
    }

    .pagination > li:last-child > a,
    .pagination > li:last-child > span {
        border-bottom-right-radius: 2px;
        border-top-right-radius: 2px;
    }

    .pagination > li > a:hover,
    .pagination > li > span:hover,
    .pagination > li > a:focus,
    .pagination > li > span:focus {
        z-index: 2;
        color: #23527c;
        background-color: #eeeeee;
        border-color: #ddd;
    }

    .pagination > .active > a,
    .pagination > .active > span,
    .pagination > .active > a:hover,
    .pagination > .active > span:hover,
    .pagination > .active > a:focus,
    .pagination > .active > span:focus {
        z-index: 3;
        color: #fff;
        background-color: #337ab7;
        border-color: #337ab7;
        cursor: default;
    }

    .pagination > .disabled > span,
    .pagination > .disabled > span:hover,
    .pagination > .disabled > span:focus,
    .pagination > .disabled > a,
    .pagination > .disabled > a:hover,
    .pagination > .disabled > a:focus {
        color: #777777;
        background-color: #fff;
        border-color: #ddd;
        cursor: not-allowed;
    }

    .pagination-lg > li > a,
    .pagination-lg > li > span {
        padding: 10px 16px;
        font-size: 17px;
        line-height: 1.3333333;
    }

    .pagination-lg > li:first-child > a,
    .pagination-lg > li:first-child > span {
        border-bottom-left-radius: 3px;
        border-top-left-radius: 3px;
    }

    .pagination-lg > li:last-child > a,
    .pagination-lg > li:last-child > span {
        border-bottom-right-radius: 3px;
        border-top-right-radius: 3px;
    }

    .pagination-sm > li > a,
    .pagination-sm > li > span {
        padding: 5px 10px;
        font-size: 12px;
        line-height: 1.5;
    }

    .pagination-sm > li:first-child > a,
    .pagination-sm > li:first-child > span {
        border-bottom-left-radius: 1px;
        border-top-left-radius: 1px;
    }

    .pagination-sm > li:last-child > a,
    .pagination-sm > li:last-child > span {
        border-bottom-right-radius: 1px;
        border-top-right-radius: 1px;
    }

    .pager li {
        display: inline;
    }

    .pager li > a,
    .pager li > span {
        display: inline-block;
        padding: 5px 14px;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 15px;
    }

    .pager li > a:hover,
    .pager li > a:focus {
        text-decoration: none;
        background-color: #eeeeee;
    }

    .pager .next > a,
    .pager .next > span {
        float: right;
    }

    .pager .previous > a,
    .pager .previous > span {
        float: left;
    }

    .pager .disabled > a,
    .pager .disabled > a:hover,
    .pager .disabled > a:focus,
    .pager .disabled > span {
        color: #777777;
        background-color: #fff;
        cursor: not-allowed;
    }

    .jumbotron p {
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: 200;
    }

    .jumbotron > hr {
        border-top-color: #d5d5d5;
    }

    .jumbotron .container {
        max-width: 100%;
    }

    @media screen and (min-width: 768px) {

    }

    .thumbnail > img,
    .thumbnail a > img {
        margin-left: auto;
        margin-right: auto;
    }

    .alert h4 {
        margin-top: 0;
        color: inherit;
    }

    .alert > p,
    .alert > ul {
        margin-bottom: 0;
    }

    .alert > p + p {
        margin-top: 5px;
    }

    .alert-success hr {
        border-top-color: #c9e2b3;
    }

    .alert-info hr {
        border-top-color: #a6e1ec;
    }

    .alert-warning hr {
        border-top-color: #f7e1b5;
    }

    .alert-danger hr {
        border-top-color: #e4b9c0;
    }

    @-webkit-keyframes progress-bar-stripes {
        from {
            background-position: 40px 0;
        }
        to {
            background-position: 0 0;
        }
    }

    @keyframes progress-bar-stripes {
        from {
            background-position: 40px 0;
        }
        to {
            background-position: 0 0;
        }
    }

    .panel > .table caption,
    .panel > .table-responsive > .table caption,
    .panel > .panel-collapse > .table caption {
        padding-left: 15px;
        padding-right: 15px;
    }

    .panel > .table:first-child > thead:first-child > tr:first-child,
    .panel > .table-responsive:first-child > .table:first-child > thead:first-child > tr:first-child,
    .panel > .table:first-child > tbody:first-child > tr:first-child,
    .panel > .table-responsive:first-child > .table:first-child > tbody:first-child > tr:first-child {
        border-top-left-radius: 1px;
        border-top-right-radius: 1px;
    }

    .panel > .table:first-child > thead:first-child > tr:first-child td:first-child,
    .panel > .table-responsive:first-child > .table:first-child > thead:first-child > tr:first-child td:first-child,
    .panel > .table:first-child > tbody:first-child > tr:first-child td:first-child,
    .panel > .table-responsive:first-child > .table:first-child > tbody:first-child > tr:first-child td:first-child,
    .panel > .table:first-child > thead:first-child > tr:first-child th:first-child,
    .panel > .table-responsive:first-child > .table:first-child > thead:first-child > tr:first-child th:first-child,
    .panel > .table:first-child > tbody:first-child > tr:first-child th:first-child,
    .panel > .table-responsive:first-child > .table:first-child > tbody:first-child > tr:first-child th:first-child {
        border-top-left-radius: 1px;
    }

    .panel > .table:first-child > thead:first-child > tr:first-child td:last-child,
    .panel > .table-responsive:first-child > .table:first-child > thead:first-child > tr:first-child td:last-child,
    .panel > .table:first-child > tbody:first-child > tr:first-child td:last-child,
    .panel > .table-responsive:first-child > .table:first-child > tbody:first-child > tr:first-child td:last-child,
    .panel > .table:first-child > thead:first-child > tr:first-child th:last-child,
    .panel > .table-responsive:first-child > .table:first-child > thead:first-child > tr:first-child th:last-child,
    .panel > .table:first-child > tbody:first-child > tr:first-child th:last-child,
    .panel > .table-responsive:first-child > .table:first-child > tbody:first-child > tr:first-child th:last-child {
        border-top-right-radius: 1px;
    }

    .panel > .table:last-child > tbody:last-child > tr:last-child,
    .panel > .table-responsive:last-child > .table:last-child > tbody:last-child > tr:last-child,
    .panel > .table:last-child > tfoot:last-child > tr:last-child,
    .panel > .table-responsive:last-child > .table:last-child > tfoot:last-child > tr:last-child {
        border-bottom-left-radius: 1px;
        border-bottom-right-radius: 1px;
    }

    .panel > .table:last-child > tbody:last-child > tr:last-child td:first-child,
    .panel > .table-responsive:last-child > .table:last-child > tbody:last-child > tr:last-child td:first-child,
    .panel > .table:last-child > tfoot:last-child > tr:last-child td:first-child,
    .panel > .table-responsive:last-child > .table:last-child > tfoot:last-child > tr:last-child td:first-child,
    .panel > .table:last-child > tbody:last-child > tr:last-child th:first-child,
    .panel > .table-responsive:last-child > .table:last-child > tbody:last-child > tr:last-child th:first-child,
    .panel > .table:last-child > tfoot:last-child > tr:last-child th:first-child,
    .panel > .table-responsive:last-child > .table:last-child > tfoot:last-child > tr:last-child th:first-child {
        border-bottom-left-radius: 1px;
    }

    .panel > .table:last-child > tbody:last-child > tr:last-child td:last-child,
    .panel > .table-responsive:last-child > .table:last-child > tbody:last-child > tr:last-child td:last-child,
    .panel > .table:last-child > tfoot:last-child > tr:last-child td:last-child,
    .panel > .table-responsive:last-child > .table:last-child > tfoot:last-child > tr:last-child td:last-child,
    .panel > .table:last-child > tbody:last-child > tr:last-child th:last-child,
    .panel > .table-responsive:last-child > .table:last-child > tbody:last-child > tr:last-child th:last-child,
    .panel > .table:last-child > tfoot:last-child > tr:last-child th:last-child,
    .panel > .table-responsive:last-child > .table:last-child > tfoot:last-child > tr:last-child th:last-child {
        border-bottom-right-radius: 1px;
    }

    .panel > .table > tbody:first-child > tr:first-child th,
    .panel > .table > tbody:first-child > tr:first-child td {
        border-top: 0;
    }

    .panel > .table-bordered > thead > tr > th:first-child,
    .panel > .table-responsive > .table-bordered > thead > tr > th:first-child,
    .panel > .table-bordered > tbody > tr > th:first-child,
    .panel > .table-responsive > .table-bordered > tbody > tr > th:first-child,
    .panel > .table-bordered > tfoot > tr > th:first-child,
    .panel > .table-responsive > .table-bordered > tfoot > tr > th:first-child,
    .panel > .table-bordered > thead > tr > td:first-child,
    .panel > .table-responsive > .table-bordered > thead > tr > td:first-child,
    .panel > .table-bordered > tbody > tr > td:first-child,
    .panel > .table-responsive > .table-bordered > tbody > tr > td:first-child,
    .panel > .table-bordered > tfoot > tr > td:first-child,
    .panel > .table-responsive > .table-bordered > tfoot > tr > td:first-child {
        border-left: 0;
    }

    .panel > .table-bordered > thead > tr > th:last-child,
    .panel > .table-responsive > .table-bordered > thead > tr > th:last-child,
    .panel > .table-bordered > tbody > tr > th:last-child,
    .panel > .table-responsive > .table-bordered > tbody > tr > th:last-child,
    .panel > .table-bordered > tfoot > tr > th:last-child,
    .panel > .table-responsive > .table-bordered > tfoot > tr > th:last-child,
    .panel > .table-bordered > thead > tr > td:last-child,
    .panel > .table-responsive > .table-bordered > thead > tr > td:last-child,
    .panel > .table-bordered > tbody > tr > td:last-child,
    .panel > .table-responsive > .table-bordered > tbody > tr > td:last-child,
    .panel > .table-bordered > tfoot > tr > td:last-child,
    .panel > .table-responsive > .table-bordered > tfoot > tr > td:last-child {
        border-right: 0;
    }

    .panel > .table-bordered > thead > tr:first-child > td,
    .panel > .table-responsive > .table-bordered > thead > tr:first-child > td,
    .panel > .table-bordered > tbody > tr:first-child > td,
    .panel > .table-responsive > .table-bordered > tbody > tr:first-child > td,
    .panel > .table-bordered > thead > tr:first-child > th,
    .panel > .table-responsive > .table-bordered > thead > tr:first-child > th,
    .panel > .table-bordered > tbody > tr:first-child > th,
    .panel > .table-responsive > .table-bordered > tbody > tr:first-child > th {
        border-bottom: 0;
    }

    .panel > .table-bordered > tbody > tr:last-child > td,
    .panel > .table-responsive > .table-bordered > tbody > tr:last-child > td,
    .panel > .table-bordered > tfoot > tr:last-child > td,
    .panel > .table-responsive > .table-bordered > tfoot > tr:last-child > td,
    .panel > .table-bordered > tbody > tr:last-child > th,
    .panel > .table-responsive > .table-bordered > tbody > tr:last-child > th,
    .panel > .table-bordered > tfoot > tr:last-child > th,
    .panel > .table-responsive > .table-bordered > tfoot > tr:last-child > th {
        border-bottom: 0;
    }

    .well blockquote {
        border-color: #ddd;
        border-color: rgba(0, 0, 0, 0.15);
    }

    @media (min-width: 768px) {

    }

    @media (min-width: 992px) {
    }

    .carousel-inner > .item > img,
    .carousel-inner > .item > a > img {
        line-height: 1;
    }

    @media all and (transform-3d), (-webkit-transform-3d) {

    }

    .carousel-indicators li {
        display: inline-block;
        width: 10px;
        height: 10px;
        margin: 1px;
        text-indent: -999px;
        border: 1px solid #fff;
        border-radius: 10px;
        cursor: pointer;
        background-color: #000 \9;
        background-color: rgba(0, 0, 0, 0);
    }

    @media screen and (min-width: 768px) {

    }

    @-ms-viewport {
        width: device-width;
    }

    @media (max-width: 767px) {

    }

    @media (max-width: 767px) {
    }

    @media (max-width: 767px) {
    }

    @media (max-width: 767px) {
    }

    @media (min-width: 768px) and (max-width: 991px) {

    }

    @media (min-width: 768px) and (max-width: 991px) {
    }

    @media (min-width: 768px) and (max-width: 991px) {
    }

    @media (min-width: 768px) and (max-width: 991px) {
    }

    @media (min-width: 992px) and (max-width: 1199px) {

    }

    @media (min-width: 992px) and (max-width: 1199px) {
    }

    @media (min-width: 992px) and (max-width: 1199px) {
    }

    @media (min-width: 992px) and (max-width: 1199px) {
    }

    @media (min-width: 1200px) {

    }

    @media (min-width: 1200px) {
    }

    @media (min-width: 1200px) {
    }

    @media (min-width: 1200px) {
    }

    @media (max-width: 767px) {
    }

    @media (min-width: 768px) and (max-width: 991px) {
    }

    @media (min-width: 992px) and (max-width: 1199px) {
    }

    @media (min-width: 1200px) {
    }

    @media print {
        .visible-print {
            display: block !important;
        }

        table.visible-print {
            display: table !important;
        }

        tr.visible-print {
            display: table-row !important;
        }

        th.visible-print,
        td.visible-print {
            display: table-cell !important;
        }
    }

    @media print {
        .visible-print-block {
            display: block !important;
        }
    }

    @media print {
        .visible-print-inline {
            display: inline !important;
        }
    }

    @media print {
        .visible-print-inline-block {
            display: inline-block !important;
        }
    }

    @media print {
        .hidden-print {
            display: none !important;
        }
    }

    /*!
*
* Font Awesome
*
*/
    /*!
 *  Font Awesome 4.7.0 by @davegandy - http://fontawesome.io - @fontawesome
 *  License - http://fontawesome.io/license (Font: SIL OFL 1.1, CSS: MIT License)
 */
    /* FONT PATH
 * -------------------------- */
    @font-face {
        font-family: 'FontAwesome';
        src: url('../components/font-awesome/fonts/fontawesome-webfont.eot?v=4.7.0');
        src: url('../components/font-awesome/fonts/fontawesome-webfont.eot?#iefix&v=4.7.0') format('embedded-opentype'), url('../components/font-awesome/fonts/fontawesome-webfont.woff2?v=4.7.0') format('woff2'), url('../components/font-awesome/fonts/fontawesome-webfont.woff?v=4.7.0') format('woff'), url('../components/font-awesome/fonts/fontawesome-webfont.ttf?v=4.7.0') format('truetype'), url('../components/font-awesome/fonts/fontawesome-webfont.svg?v=4.7.0#fontawesomeregular') format('svg');
        font-weight: normal;
        font-style: normal;
    }

    /* makes the font 33% larger relative to the icon container */

    .fa-ul > li {
        position: relative;
    }

    /* Deprecated as of 4.4.0 */

    @-webkit-keyframes fa-spin {
        0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
        }
        100% {
            -webkit-transform: rotate(359deg);
            transform: rotate(359deg);
        }
    }

    @keyframes fa-spin {
        0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
        }
        100% {
            -webkit-transform: rotate(359deg);
            transform: rotate(359deg);
        }
    }

    /* Font Awesome uses the Unicode Private Use Area (PUA) to ensure screen
   readers do not read off random characters that represent icons */

    /*!
*
* IPython base
*
*/

    code {
        color: #000;
    }

    pre {
        font-size: inherit;
        line-height: inherit;
    }

    label {
        font-weight: normal;
    }

    /* Make the page background atleast 100% the height of the view port */
    /* Make the page itself atleast 70% the height of the view port */
    .border-box-sizing {
        box-sizing: border-box;
        -moz-box-sizing: border-box;
        -webkit-box-sizing: border-box;
    }

    /* Flexible box model classes */
    /* Taken from Alex Russell http://infrequently.org/2009/08/css-3-progress/ */
    /* This file is a compatability layer.  It allows the usage of flexible box
model layouts accross multiple browsers, including older browsers.  The newest,
universal implementation of the flexible box model is used when available (see
`Modern browsers` comments below).  Browsers that are known to implement this
new spec completely include:

    Firefox 28.0+
    Chrome 29.0+
    Internet Explorer 11+
    Opera 17.0+

Browsers not listed, including Safari, are supported via the styling under the
`Old browsers` comments below.
*/

    .hbox > * {
        /* Old browsers */
        -webkit-box-flex: 0;
        -moz-box-flex: 0;
        box-flex: 0;
        /* Modern browsers */
        flex: none;
    }

    .vbox > * {
        /* Old browsers */
        -webkit-box-flex: 0;
        -moz-box-flex: 0;
        box-flex: 0;
        /* Modern browsers */
        flex: none;
    }

    div.error > h1 {
        font-size: 500%;
        line-height: normal;
    }

    div.error > p {
        font-size: 200%;
        line-height: normal;
    }

    /**
 * Primary styles
 *
 * Author: Jupyter Development Team
 */
    body {
        background-color: #fff;
        /* This makes sure that the body covers the entire window and needs to
       be in a different element than the display: box in wrapper below */
        /*position: absolute;*/
        left: 0px;
        right: 0px;
        top: 0px;
        bottom: 0px;
        overflow: visible;
    }

    @media print {
        body > #header {
            display: none !important;
        }
    }

    @media print {
        #header-spacer {
            display: none;
        }
    }

    #ipython_notebook img {
        height: 28px;
    }

    @media print {
        #site {
            height: auto !important;
        }
    }

    /* Smaller buttons */

    #header > span {
        margin-top: 10px;
    }

    @media (min-width: 768px) {
    }

    @media (min-width: 768px) {
    }

    /*!
*
* IPython auth
*
*/

    /*!
*
* IPython tree view
*
*/
    /* We need an invisible input field on top of the sentense*/
    /* "Drag file onto the list ..." */

    ::-webkit-file-upload-button {
        cursor: pointer;
    }

    /**
 * Primary styles
 *
 * Author: Jupyter Development Team
 */

    ul#tabs a {
        padding-top: 6px;
        padding-bottom: 4px;
    }

    [dir="rtl"] ul#tabs.nav-tabs > li {
        float: right;
    }

    ul.breadcrumb a:focus,
    ul.breadcrumb a:hover {
        text-decoration: none;
    }

    ul.breadcrumb span {
        color: #5e5e5e;
    }

    .list_toolbar [class*="span"] {
        min-height: 24px;
    }

    .list_container > div {
        border-bottom: 1px solid #ddd;
    }

    .list_container > div:last-child {
        border: none;
    }

    .list_item a {
        text-decoration: none;
    }

    .list_header > div,
    .list_item > div {
        padding-top: 4px;
        padding-bottom: 4px;
        padding-left: 7px;
        padding-right: 7px;
        line-height: 22px;
    }

    .list_header > div input,
    .list_item > div input {
        margin-right: 7px;
        margin-left: 14px;
        vertical-align: text-bottom;
        line-height: 22px;
        position: relative;
        top: -1px;
    }

    [dir="rtl"] .list_item > div input {
        margin-right: 0;
    }

    .new-file input[type=checkbox] {
        visibility: hidden;
    }

    .list_item input:not([type=checkbox]) {
        padding-top: 3px;
        padding-bottom: 3px;
        height: 22px;
        line-height: 14px;
        margin: 0px;
    }

    #running .panel-group .panel .panel-heading a:focus,
    #running .panel-group .panel .panel-heading a:hover {
        text-decoration: none;
    }

    /*!
*
* IPython text editor webapp
*
*/

    @media not print {
        #texteditor-backdrop {
            background-color: #EEE;
        }
    }

    @media print {
        #texteditor-backdrop #texteditor-container .CodeMirror-gutter,
        #texteditor-backdrop #texteditor-container .CodeMirror-gutters {
            background-color: #fff;
        }
    }

    @media not print {
        #texteditor-backdrop #texteditor-container .CodeMirror-gutter,
        #texteditor-backdrop #texteditor-container .CodeMirror-gutters {
            background-color: #fff;
        }
    }

    @media not print {
        #texteditor-backdrop #texteditor-container {
            padding: 0px;
            background-color: #fff;
            -webkit-box-shadow: 0px 0px 12px 1px rgba(87, 87, 87, 0.2);
            box-shadow: 0px 0px 12px 1px rgba(87, 87, 87, 0.2);
        }
    }

    /*!
*
* IPython notebook
*
*/
    /* CSS font colors for translated ANSI escape sequences */
    /* The color values are a mix of
   http://www.xcolors.net/dl/baskerville-ivorylight and
   http://www.xcolors.net/dl/euphrasia */

    /* The following styles are deprecated an will be removed in a future version */

    /* use dark versions for foreground, to improve visibility */

    /* and light for background, for the same reason */

    div.cell {
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: vertical;
        -moz-box-align: stretch;
        display: box;
        box-orient: vertical;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: column;
        align-items: stretch;
        border-radius: 2px;
        box-sizing: border-box;
        -moz-box-sizing: border-box;
        -webkit-box-sizing: border-box;
        border-width: 1px;
        border-style: solid;
        border-color: transparent;
        width: 100%;
        padding: 5px;
        /* This acts as a spacer between cells, that is outside the border */
        margin: 0px;
        outline: none;
        position: relative;
        overflow: visible;
    }

    div.cell:before {
        position: absolute;
        display: block;
        top: -1px;
        left: -1px;
        width: 5px;
        height: calc(100% + 2px);
        content: '';
        background: transparent;
    }

    @media print {
        div.cell.jupyter-soft-selected {
            border-color: transparent;
        }
    }

    @media print {
        div.cell.selected,
        div.cell.selected.jupyter-soft-selected {
            border-color: transparent;
        }
    }

    @media print {
        .edit_mode div.cell.selected {
            border-color: transparent;
        }
    }

    .prompt {
        /* This needs to be wide enough for 3 digit prompt numbers: In[100]: */
        min-width: 14ex;
        /* This padding is tuned to match the padding on the CodeMirror editor. */
        padding: 0.4em;
        margin: 0px;
        font-family: monospace;
        text-align: right;
        /* This has to match that of the the CodeMirror class line-height below */
        line-height: 1.21429em;
        /* Don't highlight prompt number selection */
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        /* Use default cursor */
        cursor: default;
    }

    @media (max-width: 540px) {
        .prompt {
            text-align: left;
        }
    }

    div.inner_cell {
        min-width: 0;
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: vertical;
        -moz-box-align: stretch;
        display: box;
        box-orient: vertical;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: column;
        align-items: stretch;
        /* Old browsers */
        -webkit-box-flex: 1;
        -moz-box-flex: 1;
        box-flex: 1;
        /* Modern browsers */
        flex: 1;
    }

    /* input_area and input_prompt must match in top border and margin for alignment */
    div.input_area {
        border: 1px solid #cfcfcf;
        border-radius: 2px;
        background: #f7f7f7;
        line-height: 1.21429em;
    }

    /* This is needed so that empty prompt areas can collapse to zero height when there
   is no content in the output_subarea and the prompt. The main purpose of this is
   to make sure that empty JavaScript output_subareas have no height. */
    div.prompt:empty {
        padding-top: 0;
        padding-bottom: 0;
    }

    div.unrecognized_cell .inner_cell {
        border-radius: 2px;
        padding: 5px;
        font-weight: bold;
        color: red;
        border: 1px solid #cfcfcf;
        background: #eaeaea;
    }

    div.unrecognized_cell .inner_cell a {
        color: inherit;
        text-decoration: none;
    }

    div.unrecognized_cell .inner_cell a:hover {
        color: inherit;
        text-decoration: none;
    }

    @media (max-width: 540px) {
        div.unrecognized_cell > div.prompt {
            display: none;
        }
    }

    div.code_cell {
        /* avoid page breaking on code cells when printing */
    }

    @media print {
        div.code_cell {
            page-break-inside: avoid;
        }
    }

    /* any special styling for code cells that are currently running goes here */
    div.input {
        page-break-inside: avoid;
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: horizontal;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: horizontal;
        -moz-box-align: stretch;
        display: box;
        box-orient: horizontal;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }

    @media (max-width: 540px) {
        div.input {
            /* Old browsers */
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-box-align: stretch;
            display: -moz-box;
            -moz-box-orient: vertical;
            -moz-box-align: stretch;
            display: box;
            box-orient: vertical;
            box-align: stretch;
            /* Modern browsers */
            display: flex;
            flex-direction: column;
            align-items: stretch;
        }
    }

    /* input_area and input_prompt must match in top border and margin for alignment */
    div.input_prompt {
        color: #303F9F;
        border-top: 1px solid transparent;
    }

    div.input_area > div.highlight {
        margin: 0.4em;
        border: none;
        padding: 0px;
        background-color: transparent;
    }

    div.input_area > div.highlight > pre {
        margin: 0px;
        border: none;
        padding: 0px;
        background-color: transparent;
    }

    /* The following gets added to the <head> if it is detected that the user has a
 * monospace font with inconsistent normal/bold/italic height.  See
 * notebookmain.js.  Such fonts will have keywords vertically offset with
 * respect to the rest of the text.  The user should select a better font.
 * See: https://github.com/ipython/ipython/issues/1503
 *
 * .CodeMirror span {
 *      vertical-align: bottom;
 * }
 */

    .CodeMirror pre {
        /* In CM3 this went to 4px from 0 in CM2. This sets horizontal padding only,
    use .CodeMirror-lines for vertical */
        padding: 0 0.4em;
        border: 0;
        border-radius: 0;
    }

    @media screen and (min-width: 2138px) and (max-width: 4319px) {
    }

    @media screen and (min-width: 4320px) {
    }

    /*

Original style from softwaremaniacs.org (c) Ivan Sagalaev <Maniac@SoftwareManiacs.Org>
Adapted from GitHub theme

*/

    /* previously not defined, copying from default codemirror */

    /* apply the same style to codemirror */

    div.output_wrapper {
        /* this position must be relative to enable descendents to be absolute within it */
        position: relative;
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: vertical;
        -moz-box-align: stretch;
        display: box;
        box-orient: vertical;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: column;
        align-items: stretch;
        z-index: 1;
    }

    /* class for the output area when it should be height-limited */

    /* output div while it is collapsed */

    div.output_prompt {
        color: #D84315;
    }

    /* This class is the outer container of all output sections. */
    div.output_area {
        padding: 0px;
        page-break-inside: avoid;
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: horizontal;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: horizontal;
        -moz-box-align: stretch;
        display: box;
        box-orient: horizontal;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }

    div.output_area .rendered_html table {
        margin-left: 0;
        margin-right: 0;
    }

    div.output_area .rendered_html img {
        margin-left: 0;
        margin-right: 0;
    }

    div.output_area img,
    div.output_area svg {
        max-width: 100%;
        height: auto;
    }

    div.output_area .mglyph > img {
        max-width: none;
    }

    /* This is needed to protect the pre formating from global settings such
   as that of bootstrap */
    .output {
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: vertical;
        -moz-box-align: stretch;
        display: box;
        box-orient: vertical;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }

    @media (max-width: 540px) {
        div.output_area {
            /* Old browsers */
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-box-align: stretch;
            display: -moz-box;
            -moz-box-orient: vertical;
            -moz-box-align: stretch;
            display: box;
            box-orient: vertical;
            box-align: stretch;
            /* Modern browsers */
            display: flex;
            flex-direction: column;
            align-items: stretch;
        }
    }

    div.output_area pre {
        margin: 0;
        padding: 1px 0 1px 0;
        border: 0;
        vertical-align: baseline;
        color: black;
        background-color: transparent;
        border-radius: 0;
    }

    /* This class is for the output subarea inside the output_area and after
   the prompt div. */
    div.output_subarea {
        overflow-x: auto;
        padding: 0.4em;
        /* Old browsers */
        -webkit-box-flex: 1;
        -moz-box-flex: 1;
        box-flex: 1;
        /* Modern browsers */
        flex: 1;
        max-width: calc(100% - 14ex);
    }

    div.output_scroll div.output_subarea {
        overflow-x: visible;
    }

    /* The rest of the output_* classes are for special styling of the different
   output types */
    /* all text output has this class: */
    div.output_text {
        text-align: left;
        color: #000;
        /* This has to match that of the the CodeMirror class line-height below */
        line-height: 1.21429em;
    }

    /* stdout/stderr are 'text' as well as 'stream', but execute_result/error are *not* streams */
    div.output_stderr {
        background: #fdd;
        /* very light red background for stderr */
    }

    /* Empty output_javascript divs should have no height */

    /* raw_input styles */

    div.output_unrecognized a {
        color: inherit;
        text-decoration: none;
    }

    div.output_unrecognized a:hover {
        color: inherit;
        text-decoration: none;
    }

    .rendered_html {
        color: #000;
        /* any extras will just be numbers: */
    }

    .rendered_html em {
        font-style: italic;
    }

    .rendered_html strong {
        font-weight: bold;
    }

    .rendered_html u {
        text-decoration: underline;
    }

    .rendered_html :link {
        text-decoration: underline;
    }

    .rendered_html :visited {
        text-decoration: underline;
    }

    .rendered_html h1 {
        font-size: 185.7%;
        margin: 1.08em 0 0 0;
        font-weight: bold;
        line-height: 1.0;
    }

    .rendered_html h2 {
        font-size: 157.1%;
        margin: 1.27em 0 0 0;
        font-weight: bold;
        line-height: 1.0;
    }

    .rendered_html h3 {
        font-size: 128.6%;
        margin: 1.55em 0 0 0;
        font-weight: bold;
        line-height: 1.0;
    }

    .rendered_html h4 {
        font-size: 100%;
        margin: 2em 0 0 0;
        font-weight: bold;
        line-height: 1.0;
    }

    .rendered_html h5 {
        font-size: 100%;
        margin: 2em 0 0 0;
        font-weight: bold;
        line-height: 1.0;
        font-style: italic;
    }

    .rendered_html h6 {
        font-size: 100%;
        margin: 2em 0 0 0;
        font-weight: bold;
        line-height: 1.0;
        font-style: italic;
    }

    .rendered_html h1:first-child {
        margin-top: 0.538em;
    }

    .rendered_html h2:first-child {
        margin-top: 0.636em;
    }

    .rendered_html h3:first-child {
        margin-top: 0.777em;
    }

    .rendered_html h4:first-child {
        margin-top: 1em;
    }

    .rendered_html h5:first-child {
        margin-top: 1em;
    }

    .rendered_html h6:first-child {
        margin-top: 1em;
    }

    .rendered_html ul {
        list-style: disc;
    }

    .rendered_html ul ul {
        list-style: square;
        margin-top: 0;
    }

    .rendered_html ul ul ul {
        list-style: circle;
    }

    .rendered_html ol {
        list-style: decimal;
    }

    .rendered_html ol ol {
        list-style: upper-alpha;
        margin-top: 0;
    }

    .rendered_html ol ol ol {
        list-style: lower-alpha;
    }

    .rendered_html ol ol ol ol {
        list-style: lower-roman;
    }

    .rendered_html ol ol ol ol ol {
        list-style: decimal;
    }

    .rendered_html * + ul {
        margin-top: 1em;
    }

    .rendered_html * + ol {
        margin-top: 1em;
    }

    .rendered_html hr {
        color: black;
        background-color: black;
    }

    .rendered_html pre {
        margin: 1em 2em;
        padding: 0px;
        background-color: #fff;
    }

    .rendered_html code {
        background-color: #eff0f1;
    }

    .rendered_html p code {
        padding: 1px 5px;
    }

    .rendered_html pre code {
        background-color: #fff;
    }

    .rendered_html pre,
    .rendered_html code {
        border: 0;
        color: #000;
        font-size: 100%;
    }

    .rendered_html blockquote {
        margin: 1em 2em;
    }

    .rendered_html table {
        margin-left: auto;
        margin-right: auto;
        border: none;
        border-collapse: collapse;
        border-spacing: 0;
        color: black;
        font-size: 12px;
        table-layout: fixed;
    }

    .rendered_html thead {
        border-bottom: 1px solid black;
        vertical-align: bottom;
    }

    .rendered_html tr,
    .rendered_html th,
    .rendered_html td {
        text-align: right;
        vertical-align: middle;
        padding: 0.5em 0.5em;
        line-height: normal;
        white-space: normal;
        max-width: none;
        border: none;
    }

    .rendered_html th {
        font-weight: bold;
    }

    .rendered_html tbody tr:nth-child(odd) {
        background: #f5f5f5;
    }

    .rendered_html tbody tr:hover {
        background: rgba(66, 165, 245, 0.2);
    }

    .rendered_html * + table {
        margin-top: 1em;
    }

    .rendered_html p {
        text-align: left;
    }

    .rendered_html * + p {
        margin-top: 1em;
    }

    .rendered_html img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    .rendered_html * + img {
        margin-top: 1em;
    }

    .rendered_html img,
    .rendered_html svg {
        max-width: 100%;
        height: auto;
    }

    [dir="rtl"] .rendered_html p {
        text-align: right;
    }

    div.text_cell {
        /* Old browsers */
        display: -webkit-box;
        -webkit-box-orient: horizontal;
        -webkit-box-align: stretch;
        display: -moz-box;
        -moz-box-orient: horizontal;
        -moz-box-align: stretch;
        display: box;
        box-orient: horizontal;
        box-align: stretch;
        /* Modern browsers */
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }

    @media (max-width: 540px) {
        div.text_cell > div.prompt {
            display: none;
        }
    }

    div.text_cell_render {
        /*font-family: "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;*/
        outline: none;
        resize: none;
        width: inherit;
        border-style: none;
        padding: 0.5em 0.5em 0.5em 0.4em;
        color: #000;
        box-sizing: border-box;
        -moz-box-sizing: border-box;
        -webkit-box-sizing: border-box;
    }

    a.anchor-link:link {
        text-decoration: none;
        padding: 0px 20px;
        visibility: hidden;
    }

    h1:hover .anchor-link,
    h2:hover .anchor-link,
    h3:hover .anchor-link,
    h4:hover .anchor-link,
    h5:hover .anchor-link,
    h6:hover .anchor-link {
        visibility: visible;
    }

    .text_cell.rendered .input_area {
        display: none;
    }

    .text_cell.rendered .rendered_html {
        overflow-x: auto;
        overflow-y: hidden;
    }

    .text_cell.rendered .rendered_html tr,
    .text_cell.rendered .rendered_html th,
    .text_cell.rendered .rendered_html td {
        max-width: none;
    }

    .text_cell.unrendered .text_cell_render {
        display: none;
    }

    .text_cell .dropzone .input_area {
        border: 2px dashed #bababa;
        margin: -1px;
    }

    /*!
*
* IPython notebook webapp
*
*/
    @media (max-width: 767px) {
    }

    div#notebook {
        font-size: 14px;
        line-height: 20px;
        overflow-y: hidden;
        overflow-x: auto;
        width: 100%;
        /* This spaces the page away from the edge of the notebook area */
        padding-top: 20px;
        margin: 0px;
        outline: none;
        box-sizing: border-box;
        -moz-box-sizing: border-box;
        -webkit-box-sizing: border-box;
        min-height: 100%;
    }

    @media not print {
        #notebook-container {
            padding: 15px;
            background-color: #fff;
            min-height: 0;
            -webkit-box-shadow: 0px 0px 12px 1px rgba(87, 87, 87, 0.2);
            box-shadow: 0px 0px 12px 1px rgba(87, 87, 87, 0.2);
        }
    }

    @media print {
        #notebook-container {
            width: 100%;
        }
    }

    /* Word-wrap output correctly.  This is the CSS3 spelling, though Firefox seems
   to not honor it correctly.  Webkit browsers (Chrome, rekonq, Safari) do.
 */
    pre,
    code,
    kbd,
    samp {
        white-space: pre-wrap;
    }

    p {
        margin-bottom: 0;
    }

    @media not print {
        .notebook_app {
            background-color: #EEE;
        }
    }

    kbd {
        border-style: solid;
        border-width: 1px;
        box-shadow: none;
        margin: 2px;
        padding-left: 2px;
        padding-right: 2px;
        padding-top: 1px;
        padding-bottom: 1px;
    }

    .jupyter-keybindings input {
        margin: 0;
        padding: 0;
        border: none;
    }

    .jupyter-keybindings i {
        padding: 6px;
    }

    .well code {
        background-color: #ffffff;
        border-color: #ababab;
        border-width: 1px;
        border-style: solid;
        padding: 2px;
        padding-top: 1px;
        padding-bottom: 1px;
    }

    /* CSS for the cell toolbar */

    @media print {
        .celltoolbar {
            display: none;
        }
    }

    /* ctb_show is added to the ctb_hideshow div to show the cell toolbar.
   Cell toolbars are only shown when the ctb_global_show class is also set.
*/

    .ctb_global_show .ctb_show ~ div.text_cell_render {
        border: 1px solid #cfcfcf;
    }

    .celltoolbar select {
        display: block;
        width: 100%;
        height: 32px;
        padding: 6px 12px;
        font-size: 13px;
        line-height: 1.42857143;
        color: #555555;
        background-color: #fff;
        background-image: none;
        border: 1px solid #ccc;
        border-radius: 2px;
        -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
        box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
        -webkit-transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
        -o-transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
        transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
        height: 30px;
        padding: 5px 10px;
        font-size: 12px;
        line-height: 1.5;
        border-radius: 1px;
        width: inherit;
        font-size: inherit;
        height: 22px;
        padding: 0px;
        display: inline-block;
    }

    .celltoolbar select:focus {
        border-color: #66afe9;
        outline: 0;
        -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(102, 175, 233, 0.6);
        box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(102, 175, 233, 0.6);
    }

    .celltoolbar select::-moz-placeholder {
        color: #999;
        opacity: 1;
    }

    .celltoolbar select:-ms-input-placeholder {
        color: #999;
    }

    .celltoolbar select::-webkit-input-placeholder {
        color: #999;
    }

    .celltoolbar select::-ms-expand {
        border: 0;
        background-color: transparent;
    }

    .celltoolbar select[disabled],
    .celltoolbar select[readonly],
    fieldset[disabled] .celltoolbar select {
        background-color: #eeeeee;
        opacity: 1;
    }

    .celltoolbar select[disabled],
    fieldset[disabled] .celltoolbar select {
        cursor: not-allowed;
    }

    textarea.celltoolbar select {
        height: auto;
    }

    select.celltoolbar select {
        height: 30px;
        line-height: 30px;
    }

    textarea.celltoolbar select,
    select[multiple].celltoolbar select {
        height: auto;
    }

    .celltoolbar label {
        margin-left: 5px;
        margin-right: 5px;
    }

    .tag-container > * {
        margin: 0 4px;
    }

    .tags-input > * {
        margin-left: 4px;
    }

    .tags-input input[type=text]:focus {
        outline: none;
        box-shadow: none;
        border-color: #ccc;
    }

    .completions select {
        background: white;
        outline: none;
        border: none;
        padding: 0px;
        margin: 0px;
        overflow: auto;
        font-family: monospace;
        font-size: 110%;
        color: #000;
        width: auto;
    }

    [dir="rtl"] #menubar .navbar-nav > li {
        float: right;
    }

    ul#help_menu li a {
        overflow: hidden;
        padding-right: 2.2em;
    }

    ul#help_menu li a i {
        margin-right: -1.2em;
    }

    [dir="rtl"] ul#help_menu li a {
        padding-left: 2.2em;
    }

    [dir="rtl"] ul#help_menu li a i {
        margin-right: 0;
        margin-left: -1.2em;
    }

    .dropdown-submenu > a:after {
        display: inline-block;
        font: normal normal normal 14px/1 FontAwesome;
        font-size: inherit;
        text-rendering: auto;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        display: block;
        content: "\f0da";
        float: right;
        color: #333333;
        margin-top: 2px;
        margin-right: -10px;
    }

    [dir="rtl"] .dropdown-submenu > a:after {
        float: left;
        content: "\f0d9";
        margin-right: 0;
        margin-left: -10px;
    }

    .dropdown-submenu:hover > a:after {
        color: #262626;
    }

    div#pager pre {
        line-height: 1.21429em;
        color: #000;
        background-color: #f7f7f7;
        padding: 0.4em;
    }

    @media (max-width: 767px) {

    }

    @media (min-width: 768px) and (max-width: 991px) {

    }

    .toolbar select,
    .toolbar label {
        width: auto;
        vertical-align: middle;
        margin-right: 2px;
        margin-bottom: 0px;
        display: inline;
        font-size: 92%;
        margin-left: 0.3em;
        margin-right: 0.3em;
        padding: 0px;
        padding-top: 3px;
    }

    /**
 * Primary styles
 *
 * Author: Jupyter Development Team
 */
    /** WARNING IF YOU ARE EDITTING THIS FILE, if this is a .css file, It has a lot
 * of chance of beeing generated from the ../less/[samename].less file, you can
 * try to get back the less file by reverting somme commit in history
 **/
    /*
 * We'll try to get something pretty, so we
 * have some strange css to have the scroll bar on
 * the left with fix button on the top right of the tooltip
 */
    @-moz-keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }

    @-webkit-keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }

    @-moz-keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @-webkit-keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    /*properties of tooltip after "expand"*/

    /*properties of tooltip before "expand"*/

    .ipython_tooltip a {
        float: right;
    }

    .ipython_tooltip .tooltiptext pre {
        border: 0;
        border-radius: 0;
        font-size: 100%;
        background-color: #f7f7f7;
    }

    ul.typeahead-list i {
        margin-left: -10px;
        width: 18px;
    }

    [dir="rtl"] ul.typeahead-list i {
        margin-left: 0;
        margin-right: -10px;
    }

    ul.typeahead-list > li > a {
        /** Firefox bug **/
        /* see https://github.com/jupyter/notebook/issues/559 */
        white-space: normal;
    }

    .cmd-palette form {
        background: white;
    }

    .cmd-palette input {
        outline: none;
    }

    #find-and-replace #replace-preview pre {
        padding: 5px 10px;
    }

    /*# sourceMappingURL=style.min.css.map */
    pre {
        line-height: 125%;
    }

    .highlight {
        background: #f8f8f8;
    }

    /* Comment */

    /* Error */
    .highlight .k {
        color: #008000;
        font-weight: bold
    }

    /* Keyword */
    .highlight .o {
        color: #666666
    }

    /* Operator */

    /* Comment.Hashbang */

    /* Comment.Multiline */

    /* Comment.Preproc */

    /* Comment.PreprocFile */
    .highlight .c1 {
        color: #3D7B7B;
        font-style: italic
    }

    /* Comment.Single */

    /* Comment.Special */

    /* Generic.Deleted */

    /* Generic.Emph */

    /* Generic.Error */

    /* Generic.Heading */

    /* Generic.Inserted */

    /* Generic.Output */

    /* Generic.Prompt */

    /* Generic.Strong */

    /* Generic.Subheading */

    /* Generic.Traceback */
    .highlight .kc {
        color: #008000;
        font-weight: bold
    }

    /* Keyword.Constant */

    /* Keyword.Declaration */
    .highlight .kn {
        color: #008000;
        font-weight: bold
    }

    /* Keyword.Namespace */

    /* Keyword.Pseudo */

    /* Keyword.Reserved */

    /* Keyword.Type */

    /* Literal.Number */

    /* Literal.String */

    /* Name.Attribute */
    .highlight .nb {
        color: #008000
    }

    /* Name.Builtin */

    /* Name.Class */

    /* Name.Constant */

    /* Name.Decorator */

    /* Name.Entity */

    /* Name.Exception */
    .highlight .nf {
        color: #0000FF
    }

    /* Name.Function */

    /* Name.Label */
    .highlight .nn {
        color: #0000FF;
        font-weight: bold
    }

    /* Name.Namespace */

    /* Name.Tag */

    /* Name.Variable */
    .highlight .ow {
        color: #AA22FF;
        font-weight: bold
    }

    /* Operator.Word */
    .highlight .w {
        color: #bbbbbb
    }

    /* Text.Whitespace */

    /* Literal.Number.Bin */
    .highlight .mf {
        color: #666666
    }

    /* Literal.Number.Float */

    /* Literal.Number.Hex */
    .highlight .mi {
        color: #666666
    }

    /* Literal.Number.Integer */

    /* Literal.Number.Oct */
    .highlight .sa {
        color: #BA2121
    }

    /* Literal.String.Affix */

    /* Literal.String.Backtick */

    /* Literal.String.Char */

    /* Literal.String.Delimiter */

    /* Literal.String.Doc */
    .highlight .s2 {
        color: #BA2121
    }

    /* Literal.String.Double */
    .highlight .se {
        color: #AA5D1F;
        font-weight: bold
    }

    /* Literal.String.Escape */

    /* Literal.String.Heredoc */
    .highlight .si {
        color: #A45A77;
        font-weight: bold
    }

    /* Literal.String.Interpol */

    /* Literal.String.Other */

    /* Literal.String.Regex */
    .highlight .s1 {
        color: #BA2121
    }

    /* Literal.String.Single */

    /* Literal.String.Symbol */

    /* Name.Builtin.Pseudo */

    /* Name.Function.Magic */

    /* Name.Variable.Class */

    /* Name.Variable.Global */

    /* Name.Variable.Instance */

    /* Name.Variable.Magic */

    /* Literal.Number.Integer.Long */
    /* Overrides of notebook CSS for static HTML export */
    body {
        overflow: visible;
        /*padding: 8px;*/
    }

    div#notebook {
        overflow: visible;
        border-top: none;
    }

    @media print {
        div.cell {
            display: block;
            page-break-inside: avoid;
        }

        div.output_wrapper {
            display: block;
            page-break-inside: avoid;
        }

        div.output {
            display: block;
            page-break-inside: avoid;
        }
    }
</style>
