import os
import tempfile
import pandas as pd
from src.core.test_mapping_advanced import TestMappingVisualizer


def test_visualize_deviation_histogram_creates_file():
    visualizer = TestMappingVisualizer()
    results_df = pd.DataFrame(
        {
            'x': [1.0, 2.0, 3.0, 4.0],
            'y': [1.1, 2.1, 3.2, 4.1],
            'ideal_function': ['y1', 'y1', 'y2', None],
            'delta_y': [0.05, 0.20, 0.10, None],
        }
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'deviation_histogram.png')
        visualizer.visualize_deviation_histogram(results_df, output_path=output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
