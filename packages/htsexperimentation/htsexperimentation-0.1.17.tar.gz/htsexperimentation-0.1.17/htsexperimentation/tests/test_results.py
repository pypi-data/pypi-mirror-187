import unittest
import pandas as pd
import pickle

from htsexperimentation.compute_results.results_handler import ResultsHandler
from htsexperimentation.visualization.plotting import (
    boxplot,
    plot_predictions_hierarchy,
    plot_mase,
)


class TestModel(unittest.TestCase):
    def setUp(self):
        self.datasets = ["prison", "tourism"]
        data = {}
        for i in range(len(self.datasets)):
            with open(
                f"./data/data_{self.datasets[i]}.pickle",
                "rb",
            ) as handle:
                data[i] = pickle.load(handle)

        self.results_prison_gpf = ResultsHandler(
            path="./results/",
            dataset=self.datasets[0],
            algorithms=["gpf_exact", "gpf_svg"],
            groups=data[0],
        )
        self.results_tourism_gpf = ResultsHandler(
            path="./results/",
            dataset=self.datasets[1],
            algorithms=["gpf_exact", "gpf_svg"],
            groups=data[1],
        )

        self.results_prison = ResultsHandler(
            path="./results/",
            dataset=self.datasets[0],
            algorithms=["mint", "gpf_exact", "deepar", "standard_gp", "ets_bu"],
            groups=data[0],
        )
        self.results_tourism = ResultsHandler(
            path="./results/",
            dataset=self.datasets[1],
            algorithms=["mint", "gpf_exact", "deepar", "standard_gp", "ets_bu"],
            groups=data[1],
        )

    def test_results_load(self):
        res = self.results_prison.load_results_algorithm(
            algorithm="ets_bu",
            res_type="fitpred",
            res_measure="mean",
            output_type="results",
        )
        self.assertTrue(res)

    def test_compute_differences_gpf_variants(self):
        results = self.results_prison_gpf.compute_error_metrics(
            algorithms_list=["gpf_exact", "gpf_svg"], metric="rmse"
        )
        differences = self.results_prison_gpf.calculate_percent_diff(
            base_algorithm="gpf_exact", results=results
        )
        differences_algorithms = {}
        differences_algorithms["gpf_svg"] = self.results_prison_gpf.dict_to_df(
            differences, "gpf_svg"
        )
        boxplot(datasets_err=differences_algorithms, err="rmse")

    def test_create_boxplot_all_algorithms(self):
        dataset_res = {}
        dataset_res[self.datasets[0]] = self.results_prison.data_to_boxplot(
            "mase", output_type="metrics"
        )
        dataset_res[self.datasets[1]] = self.results_tourism.data_to_boxplot(
            "mase", output_type="metrics"
        )
        res = boxplot(datasets_err=dataset_res, err="mase")

    def test_compute_mase(self):
        (
            results_hierarchy,
            results_by_group_element,
            group_elements,
        ) = self.results_prison.compute_results_hierarchy(algorithm="gpf_exact")
        plot_predictions_hierarchy(
            *results_hierarchy,
            *results_by_group_element,
            group_elements,
            self.results_prison.h,
            "gpf_exact",
        )
        mase_by_group = self.results_prison._compute_metric(
            results_hierarchy, results_by_group_element, group_elements, "mase"
        )
        self.assertTrue(
            list(mase_by_group.keys()) == ["bottom", "top", "state", "gender", "legal"]
        )

    def test_create_plot_hierarchy(self):
        (
            results_hierarchy,
            results_by_group_element,
            group_elements,
        ) = self.results_prison.compute_results_hierarchy(algorithm="mint")
        mase_by_group = self.results_prison.compute_mase(
            results_hierarchy, results_by_group_element, group_elements
        )
        plot_mase(mase_by_group)
