"""
Visualization module using Bokeh for the IU CSEMDSPWP01 project.

This module creates visualizations for training data, selected ideal functions,
and test data with their assignments.
"""

from typing import List, Dict
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import HoverTool
from src.models.models import TrainingData, IdealFunction, TestData
from src.utils.exceptions import VisualizationError
import numpy as np
import webbrowser
import os
import threading
import socketserver
import http.server
import functools
from pathlib import Path


class Visualizer:
    """
    Visualizer class for creating Bokeh plots of training data,
    ideal functions, and test data mappings.
    """

    def __init__(self, output_path: str = "visualization.html") -> None:
        """
        Initialize the visualizer.

        Args:
            output_path: Path for the output HTML file.
        """
        self.output_path = output_path
        self.plots = []

    def plot_training_data_with_ideal_function(
        self,
        training_data: List[TrainingData],
        ideal_function: IdealFunction,
        training_index: int,
        ideal_function_index: int,
    ) -> None:
        """
        Create a plot of training data with its selected ideal function.

        Args:
            training_data: List of training data points.
            ideal_function: The selected ideal function to plot.
            training_index: Index of the training dataset (0-3 for Y1-Y4).
            ideal_function_index: Index of the ideal function (0-49).

        Raises:
            VisualizationError: If plot creation fails.
        """
        try:
            # Extract data
            x_train = [t.x for t in training_data]
            y_train = [t.y_values[training_index] for t in training_data]
            x_ideal = [ideal_function.x]
            y_ideal = [ideal_function.y_values[ideal_function_index]]

            # Create figure
            p = figure(
                title=f"Training Data Y{training_index + 1} vs Ideal Function {ideal_function_index + 1}",
                x_axis_label="X",
                y_axis_label="Y",
                width=800,
                height=400,
                toolbar_location="right",
            )

            # Plot training data
            p.scatter(
                x_train,
                y_train,
                size=8,
                color="blue",
                alpha=0.6,
                legend_label="Training Data",
            )

            # Plot ideal function
            p.line(
                x_ideal,
                y_ideal,
                line_width=2,
                color="red",
                legend_label=f"Ideal Function {ideal_function_index + 1}",
            )

            # Add hover tool
            hover = HoverTool(tooltips=[("X", "@x"), ("Y", "@y")])
            p.add_tools(hover)

            p.legend.click_policy = "hide"
            self.plots.append(p)

        except Exception as e:
            raise VisualizationError(f"Error creating training data plot: {str(e)}") from e

    def plot_test_data_with_assignments(
        self,
        test_data: List[TestData],
        ideal_functions: List[IdealFunction],
        selected_indices: dict,
    ) -> None:
        """
        Create a plot of test data with their ideal function assignments.

        Args:
            test_data: List of test data points.
            ideal_functions: List of all ideal functions.
            selected_indices: Dictionary with selected ideal function indices.

        Raises:
            VisualizationError: If plot creation fails.
        """
        try:
            # Extract test data
            x_test = [t.x for t in test_data]
            y_test = [t.y for t in test_data]

            # Create figure
            p = figure(
                title="Test Data Assignments",
                x_axis_label="X",
                y_axis_label="Y",
                width=800,
                height=400,
                toolbar_location="right",
            )

            # Plot test data points
            p.scatter(
                x_test,
                y_test,
                size=8,
                color="green",
                alpha=0.6,
                legend_label="Test Data",
            )

            # Add lines for assigned ideal functions
            colors = ["red", "blue", "orange", "purple"]
            for i, (key, value) in enumerate(selected_indices.items()):
                ideal_idx = value.get("index")
                if ideal_idx is not None:
                    ideal_func = ideal_functions[ideal_idx]
                    x_ideal = [ideal_func.x]
                    y_ideal = [ideal_func.y_values[ideal_idx]]

                    p.line(
                        x_ideal,
                        y_ideal,
                        line_width=2,
                        color=colors[i],
                        legend_label=f"Ideal {key} (Function {ideal_idx + 1})",
                    )

            hover = HoverTool(tooltips=[("X", "@x"), ("Y", "@y")])
            p.add_tools(hover)
            p.legend.click_policy = "hide"
            self.plots.append(p)

        except Exception as e:
            raise VisualizationError(f"Error creating test data plot: {str(e)}") from e

    def plot_all_ideal_functions(
        self,
        ideal_functions: List[IdealFunction],
        x_values: List[float] = None,
    ) -> None:
        """
        Create a plot showing all ideal functions.

        Args:
            ideal_functions: List of all ideal functions.
            x_values: Optional list of X values (if None, uses indices).

        Raises:
            VisualizationError: If plot creation fails.
        """
        try:
            # Create figure
            p = figure(
                title="All 50 Ideal Functions",
                x_axis_label="X",
                y_axis_label="Y",
                width=800,
                height=400,
                toolbar_location="right",
            )

            # Plot each ideal function
            # Use a palette of distinct Bokeh colors
            bokeh_colors = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
            ]
            for i, ideal_func in enumerate(ideal_functions[:20]):  # Plot first 20 for clarity
                x_data = [ideal_func.x] if x_values is None else [x_values[0]]
                y_data = [ideal_func.y_values[i]]

                p.line(
                    x_data,
                    y_data,
                    line_width=1,
                    color=bokeh_colors[i % len(bokeh_colors)],
                    alpha=0.7,
                    legend_label=f"Function {i + 1}",
                )

            hover = HoverTool(tooltips=[("X", "@x"), ("Y", "@y")])
            p.add_tools(hover)
            p.legend.click_policy = "hide"
            self.plots.append(p)

        except Exception as e:
            raise VisualizationError(f"Error creating ideal functions plot: {str(e)}") from e

    def save_visualizations(self) -> None:
        """
        Save all plots to an HTML file and open it in the default browser.

        Raises:
            VisualizationError: If save fails.
        """
        try:
            if not self.plots:
                raise VisualizationError("No plots to save")

            # Ensure we use an absolute path and a proper file URI on all OSes
            file_path = Path(self.output_path).resolve()
            output_file(str(file_path))
            layout = column(*self.plots)
            save(layout)

            # Create a small live wrapper that reloads when the HTML changes
            wrapper_path = file_path.parent / "visualization_live.html"
            wrapper_html = f"""<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\">
    <title>Live Visualization</title>
    <style>html,body{{height:100%;margin:0;padding:0}}</style>
  </head>
  <body>
    <iframe id=\"viz\" src=\"{file_path.name}\" style=\"width:100%;height:100vh;border:none;\"></iframe>
    <script>
      let last = null;
      async function check(){{
        try{{
          const res = await fetch('{file_path.name}', {{method:'HEAD', cache:'no-store'}});
          const lm = res.headers.get('Last-Modified');
          if (last && lm && lm !== last) {{
            document.getElementById('viz').src = '{file_path.name}#' + Date.now();
          }}
          last = lm;
        }}catch(e){{}}
      }}
      setInterval(check, 2000);
    </script>
  </body>
</html>"""
            try:
                wrapper_path.write_text(wrapper_html, encoding="utf-8")
            except Exception:
                pass

            # Try to start a local HTTP server serving the file's directory
            server_started = False
            if not getattr(self, "_server_thread", None):
                try:
                    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(file_path.parent))
                    from http.server import ThreadingHTTPServer

                    server = None
                    # scan for an available port
                    for port_try in range(8000, 8100):
                        try:
                            server = ThreadingHTTPServer(("127.0.0.1", port_try), Handler)
                            port = port_try
                            break
                        except OSError:
                            server = None
                            continue

                    if server is None:
                        raise OSError("No available port in range 8000-8099")

                    thread = threading.Thread(target=server.serve_forever, daemon=True)
                    thread.start()
                    self._server_thread = thread
                    self._httpd = server
                    server_started = True
                except Exception as ex:
                    print(f"Could not start local HTTP server: {ex}")
                    server_started = False

            # Prefer opening the live wrapper via HTTP so auto-reload works
            try:
                if server_started:
                    url = f"http://127.0.0.1:{port}/{wrapper_path.name}"
                    try:
                        webbrowser.open_new_tab(url)
                    except Exception:
                        pass
                    print(f"Visualization served at: {url}")
                    try:
                        input("Press Enter to stop the local visualization server and exit...\n")
                    finally:
                        try:
                            if hasattr(self, "_httpd") and self._httpd:
                                self._httpd.shutdown()
                        except Exception:
                            pass
                else:
                    # Fall back to opening the file directly
                    opened = False
                    try:
                        opened = webbrowser.open_new_tab(file_path.as_uri())
                    except Exception:
                        opened = False

                    if not opened:
                        try:
                            if os.name == "nt":
                                os.startfile(str(file_path))
                            else:
                                webbrowser.open(str(file_path))
                            print(f"Visualization opened (file): {file_path}")
                        except Exception:
                            print(f"Visualization saved to: {file_path}")
                    else:
                        print(f"Visualization opened in browser: {file_path}")
            except Exception:
                print(f"Visualization saved to: {file_path}")
        except Exception as e:
            raise VisualizationError(f"Error saving visualizations: {str(e)}") from e

    def clear_plots(self) -> None:
        """Clear all stored plots."""
        self.plots = []
