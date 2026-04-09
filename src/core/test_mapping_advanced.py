"""
Advanced test data mapping module with DataFrame and matplotlib visualization.

This module provides comprehensive test data mapping functionality with:
- DataFrame-based result storage
- Matplotlib visualization with 2x2 subplot grid
- Proper assignment to best ideal functions with deviation thresholds
"""

import math
from typing import List, Tuple, Optional, Dict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import os
from src.models.models import TestData, IdealFunction, TrainingData
from src.utils.exceptions import MappingError, VisualizationError


def calculate_abs_deviation(test_y: float, ideal_y: float) -> float:
    """Return the absolute deviation between a test value and an ideal value."""
    return abs(test_y - ideal_y)


def interpolate_ideal_y(x_target: float, x_values: List[float], y_values: List[float]) -> Optional[float]:
    """Return the ideal function Y value at the target X using linear interpolation."""
    if not x_values or not y_values or len(x_values) != len(y_values):
        return None

    x_array = np.asarray(x_values, dtype=float)
    if x_target <= x_array[0]:
        return float(y_values[0])
    if x_target >= x_array[-1]:
        return float(y_values[-1])

    idx = np.searchsorted(x_array, x_target)
    if idx < len(x_array) and abs(x_array[idx] - x_target) < 1e-9:
        return float(y_values[idx])

    left_idx = max(0, idx - 1)
    right_idx = min(len(x_array) - 1, idx)
    x_left, x_right = x_array[left_idx], x_array[right_idx]
    y_left, y_right = float(y_values[left_idx]), float(y_values[right_idx])

    if x_right == x_left:
        return float(y_left)

    fraction = (x_target - x_left) / (x_right - x_left)
    return float(y_left + fraction * (y_right - y_left))


class SelectedIdealFunctionMapper:
    """Map test dataset points to four previously selected ideal functions."""

    def __init__(
        self,
        selected_ideal_functions: Dict[str, IdealFunction],
        training_x_values: List[float],
        max_training_deviations: Dict[str, float],
    ) -> None:
        """Initialize the mapper with selected ideal functions and thresholds."""
        self.selected_ideal_functions = selected_ideal_functions
        self.training_x_values = training_x_values
        self.max_training_deviations = max_training_deviations

    def map_test_point(
        self,
        x: float,
        y: float,
    ) -> Dict[str, Optional[float]]:
        """Map a single test point to the best selected ideal function."""
        candidates = []

        for label, ideal_function in self.selected_ideal_functions.items():
            ideal_y = interpolate_ideal_y(
                x,
                self.training_x_values,
                ideal_function.y_values,
            )
            if ideal_y is None:
                continue

            deviation = calculate_abs_deviation(y, ideal_y)
            threshold = self.max_training_deviations.get(label, 0.0) * math.sqrt(2)

            if deviation <= threshold:
                candidates.append((label, deviation))

        if not candidates:
            return {
                'x': x,
                'y': y,
                'delta_y': None,
                'ideal_function': None,
            }

        best_label, best_deviation = min(candidates, key=lambda item: item[1])
        return {
            'x': x,
            'y': y,
            'delta_y': best_deviation,
            'ideal_function': best_label,
        }

    def map_test_dataframe(self, test_df: pd.DataFrame) -> pd.DataFrame:
        """Map all test points in a DataFrame and return the results DataFrame."""
        if 'x' not in test_df.columns or 'y' not in test_df.columns:
            raise ValueError("Test DataFrame must contain 'x' and 'y' columns")

        mapped_rows = []
        for _, row in test_df.iterrows():
            mapped_rows.append(self.map_test_point(float(row['x']), float(row['y'])))

        result_df = pd.DataFrame(mapped_rows)
        result_df = result_df[['x', 'y', 'delta_y', 'ideal_function']]
        return result_df


class AdvancedTestDataMapper:
    """
    Maps test data points to selected ideal functions with comprehensive analysis.
    
    For each test point, computes deviation to all ideal functions and assigns
    to the best match if deviation <= max_training_deviation * sqrt(2).
    """

    def __init__(self):
        """Initialize the advanced mapper."""
        self.results_df: Optional[pd.DataFrame] = None
        self.mapping_details: Dict = {}

    def map_test_data_comprehensive(
        self,
        test_data: List[TestData],
        ideal_functions: List[IdealFunction],
        training_data: List[TrainingData],
        selected_ideal_indices: Dict[str, Dict],
    ) -> pd.DataFrame:
        """
        Map all test data points to the four selected ideal functions.

        Args:
            test_data: List of test data points to map.
            ideal_functions: List of all 50 ideal functions.
            training_data: List of training data points (for reference).
            selected_ideal_indices: Dict with keys 'y1', 'y2', 'y3', 'y4'
                containing {'index': int, 'max_deviation': float} for each.

        Returns:
            DataFrame with columns: x, y, ideal_function, delta_y

        Raises:
            MappingError: If mapping process fails.
        """
        try:
            if not test_data:
                raise ValueError("No test data provided")
            if not ideal_functions:
                raise ValueError("No ideal functions provided")
            if not training_data:
                raise ValueError("No training data provided")

            # Get X values from training data (assuming same X coordinate range)
            training_x_values = [t.x for t in training_data]
            
            results = []
            unassigned_count = 0

            # Process each test point
            for test_point in test_data:
                mapped_result = self._map_single_test_point(
                    test_point,
                    ideal_functions,
                    training_x_values,
                    selected_ideal_indices,
                )
                
                results.append(mapped_result)
                
                if mapped_result['ideal_function'] is None:
                    unassigned_count += 1

            # Create DataFrame
            self.results_df = pd.DataFrame(results)
            
            print(f"Mapping complete: {len(test_data) - unassigned_count} assigned, "
                  f"{unassigned_count} unassigned")
            
            return self.results_df

        except Exception as e:
            raise MappingError(f"Error in comprehensive test mapping: {str(e)}") from e

    def _map_single_test_point(
        self,
        test_point: TestData,
        ideal_functions: List[IdealFunction],
        training_x_values: List[float],
        selected_ideal_indices: Dict[str, Dict],
    ) -> Dict:
        """
        Map a single test point to the best of four selected ideal functions.

        Algorithm:
        1. For each of 4 selected ideal functions:
           - Find the Y value at the test point's X coordinate (via interpolation)
           - Calculate absolute deviation
           - Check if deviation <= max_training_deviation * sqrt(2)
        2. Select the function with smallest deviation among qualifying options
        3. If no function qualifies, mark as unassigned

        Args:
            test_point: Single test data point.
            ideal_functions: List of all ideal functions.
            training_x_values: X values from training data.
            selected_ideal_indices: Dictionary of selected ideal functions.

        Returns:
            Dictionary with keys: x, y, ideal_function, deviation
        """
        result = {
            'x': test_point.x,
            'y': test_point.y,
            'ideal_function': None,
            'delta_y': None,
        }

        candidates = []  # List of (ideal_func_label, ideal_func_index, deviation)

        # Check all 4 selected ideal functions
        for label in ['y1', 'y2', 'y3', 'y4']:
            if label not in selected_ideal_indices:
                continue

            info = selected_ideal_indices[label]
            ideal_idx = info.get('index')
            max_training_dev = info.get('max_deviation', 0)

            if ideal_idx is None or ideal_idx < 0 or ideal_idx >= len(ideal_functions):
                continue

            # Get the ideal function's Y value at test point's X
            ideal_y = self._interpolate_ideal_function_y(
                test_point.x,
                ideal_functions[ideal_idx],
                training_x_values,
            )

            if ideal_y is None:
                continue

            # Calculate deviation
            deviation = abs(test_point.y - ideal_y)

            # Check threshold condition
            threshold = max_training_dev * math.sqrt(2)
            if deviation <= threshold:
                candidates.append((label, ideal_idx, deviation))

        # Select best candidate (smallest deviation)
        if candidates:
            best_label, best_idx, best_deviation = min(candidates, key=lambda x: x[2])
            result['ideal_function'] = best_label
            result['delta_y'] = best_deviation

        return result

    def _interpolate_ideal_function_y(
        self,
        x_target: float,
        ideal_function: IdealFunction,
        training_x_values: List[float],
    ) -> Optional[float]:
        """
        Get the Y value from an ideal function at target X coordinate.

        Uses linear interpolation if exact X value not found; otherwise returns
        the Y value at the closest X point.

        Args:
            x_target: Target X coordinate.
            ideal_function: The ideal function to query.
            training_x_values: X values for the ideal function data points.

        Returns:
            Interpolated Y value, or None if interpolation fails.
        """
        if not training_x_values or not ideal_function.y_values:
            return None

        # Find the index of the closest X value
        x_values_array = np.array(training_x_values)
        idx_closest = np.argmin(np.abs(x_values_array - x_target))
        x_closest = x_values_array[idx_closest]

        # If exact match or very close, return directly
        if abs(x_closest - x_target) < 1e-6:
            return float(ideal_function.y_values[idx_closest])

        # Linear interpolation if possible
        if idx_closest == 0:
            # Target is before the first point
            return float(ideal_function.y_values[0])
        elif idx_closest == len(x_values_array) - 1:
            # Target is after the last point
            return float(ideal_function.y_values[-1])
        else:
            # Check both neighbors for better interpolation
            x1, x2 = x_values_array[idx_closest - 1], x_values_array[idx_closest + 1]
            y1, y2 = ideal_function.y_values[idx_closest - 1], ideal_function.y_values[idx_closest + 1]

            # Linear interpolation
            if x2 != x1:
                y_interp = y1 + (x_target - x1) * (y2 - y1) / (x2 - x1)
                return float(y_interp)

        return float(ideal_function.y_values[idx_closest])


class TestMappingVisualizer:
    """
    Visualizes test data mapping results using matplotlib with 2x2 subplot grid.
    """

    def __init__(self):
        """Initialize the visualizer."""
        self.fig = None
        self.axes = None
        self.colors_map = {
            'y1': '#1f77b4',  # Blue
            'y2': '#ff7f0e',  # Orange
            'y3': '#2ca02c',  # Green
            'y4': '#d62728',  # Red
            'unassigned': '#808080',  # Gray
        }

    def visualize_mapping_results(
        self,
        results_df: pd.DataFrame,
        ideal_functions: List[IdealFunction],
        training_data: List[TrainingData],
        selected_ideal_indices: Dict[str, Dict],
        output_path: str = "test_mapping_results.png",
    ) -> None:
        """
        Create a 2x2 subplot grid visualizing test data mapping.

        Layout:
        - (0, 0): Y1 vs Ideal Function Y1
        - (0, 1): Y2 vs Ideal Function Y2
        - (1, 0): Y3 vs Ideal Function Y3
        - (1, 1): Y4 vs Ideal Function Y4

        Each subplot shows:
        - Ideal function as a line
        - Assigned test points as scatter
        - Unassigned points as gray scatter

        Args:
            results_df: DataFrame with mapping results.
            ideal_functions: List of all ideal functions.
            training_data: Training data for reference.
            selected_ideal_indices: Dictionary of selected ideal functions.
            output_path: Path to save the visualization.

        Raises:
            VisualizationError: If visualization fails.
        """
        try:
            if results_df is None or results_df.empty:
                raise ValueError("Results DataFrame is empty")

            # Create figure and axes
            self.fig, self.axes = plt.subplots(2, 2, figsize=(14, 10))
            self.fig.suptitle('Test Data Mapping to Ideal Functions', fontsize=16, fontweight='bold')

            training_x = np.array([t.x for t in training_data])

            # Process each of 4 subplots
            subplot_configs = [
                (0, 0, 'y1'),
                (0, 1, 'y2'),
                (1, 0, 'y3'),
                (1, 1, 'y4'),
            ]

            for row, col, label in subplot_configs:
                ax = self.axes[row, col]
                
                # Get the selected ideal function for this label
                ideal_info = selected_ideal_indices.get(label, {})
                ideal_idx = ideal_info.get('index')

                if ideal_idx is None or ideal_idx >= len(ideal_functions):
                    ax.text(0.5, 0.5, f'No {label.upper()} data', 
                            ha='center', va='center', fontsize=12)
                    ax.set_title(f'No {label.upper()} Data')
                    continue

                ideal_func = ideal_functions[ideal_idx]
                ideal_y = np.array(ideal_func.y_values)

                # Plot the ideal function as a line
                ax.plot(training_x, ideal_y, color=self.colors_map[label], 
                       linewidth=2.5, label=f'Ideal Function ({label.upper()})', zorder=2)

                # Plot training data points for this Y column
                training_y_idx = int(label[1]) - 1  # 'y1' -> 0, 'y2' -> 1, etc.
                train_x = [t.x for t in training_data]
                train_y = [t.y_values[training_y_idx] for t in training_data]
                ax.scatter(train_x, train_y, 
                          color=self.colors_map[label], s=30, alpha=0.4, 
                          marker='^', label=f'Training Data ({label.upper()})', 
                          zorder=1, edgecolors='black', linewidth=0.3)

                # Separate assigned and unassigned points for this label
                assigned = results_df[results_df['ideal_function'] == label]
                unassigned = results_df[results_df['ideal_function'].isna()]

                # Plot assigned test points
                if not assigned.empty:
                    ax.scatter(assigned['x'], assigned['y'], 
                              color=self.colors_map[label], s=50, alpha=0.6, 
                              label=f'Assigned to {label.upper()}', zorder=3, edgecolors='black', linewidth=0.5)

                # Plot unassigned test points
                if not unassigned.empty:
                    ax.scatter(unassigned['x'], unassigned['y'], 
                              color=self.colors_map['unassigned'], s=50, alpha=0.6, 
                              marker='x', linewidth=1.5, label='Unassigned', zorder=3)

                # Formatting
                ax.set_xlabel('X', fontsize=10)
                ax.set_ylabel('Y', fontsize=10)
                ax.set_title(f'{label.upper()} - Ideal Function {ideal_idx + 1}', fontsize=11, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend(fontsize=9, loc='best')

            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {output_path}")
            
            # Open the visualization in the default browser
            try:
                file_path = os.path.abspath(output_path)
                webbrowser.open(f'file://{file_path}')
                print(f"Visualization opened in browser: {file_path}")
            except Exception as e:
                print(f"Could not open visualization in browser: {e}")
            
            plt.close()

        except Exception as e:
            raise VisualizationError(f"Error creating visualization: {str(e)}") from e

    def visualize_combined_view(
        self,
        results_df: pd.DataFrame,
        ideal_functions: List[IdealFunction],
        training_data: List[TrainingData],
        selected_ideal_indices: Dict[str, Dict],
        output_path: str = "test_mapping_combined.png",
    ) -> None:
        """
        Create a combined view showing all assigned points and ideal functions.

        Args:
            results_df: DataFrame with mapping results.
            ideal_functions: List of all ideal functions.
            training_data: Training data for reference.
            selected_ideal_indices: Dictionary of selected ideal functions.
            output_path: Path to save the visualization.

        Raises:
            VisualizationError: If visualization fails.
        """
        try:
            fig, ax = plt.subplots(figsize=(12, 8))

            training_x = np.array([t.x for t in training_data])

            # Plot all ideal functions
            for label in ['y1', 'y2', 'y3', 'y4']:
                ideal_info = selected_ideal_indices.get(label, {})
                ideal_idx = ideal_info.get('index')

                if ideal_idx is not None and ideal_idx < len(ideal_functions):
                    ideal_func = ideal_functions[ideal_idx]
                    ideal_y = np.array(ideal_func.y_values)
                    ax.plot(training_x, ideal_y, color=self.colors_map[label],
                           linewidth=2.5, label=f'Ideal Function {label.upper()} (#{ideal_idx + 1})', zorder=2)

            # Plot training data points for all Y columns
            for i, label in enumerate(['y1', 'y2', 'y3', 'y4']):
                train_x = [t.x for t in training_data]
                train_y = [t.y_values[i] for t in training_data]
                ax.scatter(train_x, train_y, 
                          color=self.colors_map[label], s=40, alpha=0.3, 
                          marker='^', label=f'Training Data ({label.upper()})', 
                          zorder=1, edgecolors='black', linewidth=0.3)

            # Plot assigned points by color
            for label in ['y1', 'y2', 'y3', 'y4']:
                assigned = results_df[results_df['ideal_function'] == label]
                if not assigned.empty:
                    ax.scatter(assigned['x'], assigned['y'], 
                              color=self.colors_map[label], s=60, alpha=0.6,
                              label=f'Assigned to {label.upper()}', zorder=3, edgecolors='black', linewidth=0.5)

            # Plot unassigned points
            unassigned = results_df[results_df['ideal_function'].isna()]
            if not unassigned.empty:
                ax.scatter(unassigned['x'], unassigned['y'],
                          color=self.colors_map['unassigned'], s=60, alpha=0.6,
                          marker='x', linewidth=1.5, label='Unassigned', zorder=3)

            ax.set_xlabel('X', fontsize=11, fontweight='bold')
            ax.set_ylabel('Y', fontsize=11, fontweight='bold')
            ax.set_title('Test Data Mapping to Selected Ideal Functions', fontsize=13, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10, loc='best', ncol=2)

            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Combined view saved to: {output_path}")
            
            # Open the visualization in the default browser
            try:
                file_path = os.path.abspath(output_path)
                webbrowser.open(f'file://{file_path}')
                print(f"Combined view opened in browser: {file_path}")
            except Exception as e:
                print(f"Could not open combined view in browser: {e}")
            
            plt.close()

        except Exception as e:
            raise VisualizationError(f"Error creating combined view: {str(e)}") from e

    def visualize_deviation_histogram(
        self,
        results_df: pd.DataFrame,
        output_path: str = "test_mapping_deviation_histogram.png",
    ) -> None:
        """
        Create a histogram of deviation values for mapped test points.

        Args:
            results_df: DataFrame with mapping results.
            output_path: Path to save the histogram image.

        Raises:
            VisualizationError: If histogram creation fails.
        """
        try:
            if results_df is None or results_df.empty:
                raise ValueError("Results DataFrame is empty")

            mapped_deviations = results_df['delta_y'].dropna().astype(float)
            if mapped_deviations.empty:
                raise ValueError("No mapped test point deviations available to plot")

            plt.figure(figsize=(10, 6))
            plt.hist(
                mapped_deviations,
                bins=15,
                color='#1f77b4',
                edgecolor='black',
                alpha=0.75,
            )
            plt.title('Histogram of Deviation for Mapped Test Points', fontsize=14, fontweight='bold')
            plt.xlabel('Absolute Deviation', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.grid(axis='y', alpha=0.35)

            mean_dev = mapped_deviations.mean()
            median_dev = mapped_deviations.median()
            plt.axvline(mean_dev, color='red', linestyle='--', linewidth=1.5, label=f'Mean = {mean_dev:.3f}')
            plt.axvline(median_dev, color='green', linestyle='-.', linewidth=1.5, label=f'Median = {median_dev:.3f}')
            plt.legend(fontsize=10)

            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Deviation histogram saved to: {output_path}")

            try:
                file_path = os.path.abspath(output_path)
                webbrowser.open(f'file://{file_path}')
                print(f"Deviation histogram opened in browser: {file_path}")
            except Exception as e:
                print(f"Could not open deviation histogram in browser: {e}")

            plt.close()

        except Exception as e:
            raise VisualizationError(f"Error creating deviation histogram: {str(e)}") from e
