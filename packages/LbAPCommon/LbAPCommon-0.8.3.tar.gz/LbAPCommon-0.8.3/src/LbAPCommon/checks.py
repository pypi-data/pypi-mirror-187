###############################################################################
# (c) Copyright 2021-2022 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import math
import re
from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, List

import hist
import numpy
import uproot
from hist import Hist


@dataclass
class CheckResult:
    """Class for representing the return result of ntuple checks."""

    check_type: str
    passed: bool
    can_combine: bool
    messages: List[str] = field(default_factory=list)
    tree_data: Dict[str, Dict] = field(default_factory=dict)


def run_job_checks(checks_list, check_data, test_ntuple_path_list):
    """Run the checks listed using data from ntuples.

    Run a list of checks (can be a subset of all the checks defined in check_data).
    Requires that the data ntuples are already created (eg. by `lb-ap test`).

    Returns:
        dict: CheckResult objects
    """
    check_results = {}

    for check in checks_list:
        data = check_data[check]

        if data["type"] == "range":
            check_results[check] = range_check(
                test_ntuple_path_list,
                expression=data.get("expression"),
                limits=data.get("limits"),
                n_bins=data.get("n_bins"),
                blind_ranges=data.get("blind_ranges"),
                exp_mean=data.get("exp_mean"),
                exp_std=data.get("exp_std"),
                mean_tolerance=data.get("mean_tolerance"),
                std_tolerance=data.get("std_tolerance"),
                tree_pattern=data.get("tree_pattern"),
            )
        elif data["type"] == "range_bkg_subtracted":
            check_results[check] = range_check_bkg_subtracted(
                test_ntuple_path_list,
                expression=data.get("expression"),
                limits=data.get("limits"),
                expr_for_subtraction=data.get("expr_for_subtraction"),
                mean_sig=data.get("mean_sig"),
                background_shift=data.get("background_shift"),
                background_window=data.get("background_window"),
                signal_window=data.get("signal_window"),
                n_bins=data.get("n_bins"),
                blind_ranges=data.get("blind_ranges"),
                tree_pattern=data.get("tree_pattern"),
            )
        elif data["type"] == "range_nd":
            check_results[check] = range_check_nd(
                test_ntuple_path_list,
                expressions=data.get("expressions"),
                limits=data.get("limits"),
                n_bins=data.get("n_bins"),
                blind_ranges=data.get("blind_ranges"),
                tree_pattern=data.get("tree_pattern"),
            )
        elif data["type"] == "num_entries":
            check_results[check] = num_entries(
                test_ntuple_path_list,
                count=data.get("count"),
                tree_pattern=data.get("tree_pattern"),
            )
        elif data["type"] == "num_entries_per_invpb":
            check_results[check] = num_entries_per_invpb(
                test_ntuple_path_list,
                count_per_invpb=data.get("count_per_invpb"),
                tree_pattern=data.get("tree_pattern"),
                lumi_pattern=data.get("lumi_pattern"),
            )
        elif data["type"] == "branches_exist":
            check_results[check] = branches_exist(
                test_ntuple_path_list,
                branches=data.get("branches"),
                tree_pattern=data.get("tree_pattern"),
            )

    return check_results


def num_entries(
    filepath_list,
    count,
    tree_pattern,
):
    """Number of entries check.

    Check that all matching TTree objects contain a minimum number of entries.

    Args:
        filepath_list (list[file-like]): List of paths to files to analyse
        count (int): The minimum number of entries required
        tree_pattern (regex): A regular expression for the TTree objects to check

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            num_entries: The total number of events in the TTree
    """
    result = CheckResult("num_entries", False, True)
    for filepath in filepath_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if not re.fullmatch(tree_pattern, key):
                    continue
                if key in trees_opened:
                    continue
                trees_opened.append(key)

                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}
                    result.tree_data[key]["num_entries"] = 0

                result.tree_data[key]["num_entries"] += obj.num_entries

    result.passed = (
        all([data["num_entries"] >= count for data in result.tree_data.values()])
        and len(result.tree_data) > 0
    )
    for key, data in result.tree_data.items():
        nentries = data["num_entries"]
        result.messages += [f"Found {nentries} in {key} ({count} required)"]

    # If no matches were found the check should be marked as failed
    if len(result.tree_data) == 0:
        result.passed = False
        result.can_combine = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]

    return result


def range_check(
    filepath_list,
    expression,
    limits,
    n_bins,
    blind_ranges,
    tree_pattern,
    exp_mean,
    exp_std,
    mean_tolerance,
    std_tolerance,
):
    """Range check.

    Check if there is at least one entry in the TTree object with a specific variable falling in a pre-defined range.
    If the expected mean and standard deviation values are given in input, they are compared with the observed ones
    and their agreement within the provided *_tolerance is checked. It is also possible to blind some regions.

    Args:
        filepath_list (list[file-like]): List of paths to files to analyse
        expression (str): Name of the variable (or expression depending on varibales in the TTree) to be checked
        limits (dict): Pre-defined range for x axis
        n_bins (int): Number of bins for the histogram
        blind_ranges (dict): Regions to be blinded in the histogram
        exp_mean (float): Expected mean value (optional)
        exp_std (float): Expected standard deviation (optional)
        mean_tolerance (float): Maximum shift tolerated between expected and observed mean values (optional)
        std_tolerance (float): Maximum shift tolerated between expected and observed values of standard deviation
            (optional)
        tree_pattern (regex): A regular expression for the TTree object to check

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            histograms (list[Hist]): Filled 1D histogram of the quantity defined by the expression parameter
            num_entries (float): The total number of entries in the histogram (with blind ranges applied)
            mean (float): The mean of the histogram (approximated using binned data)
            variance (float): The variance of the histogram (approximated using binned data)
            stddev (float): The standard deviation of the histogram (approximated using binned data)
            num_entries_in_mean_window (float): The number of events falling in the exp_mean +- exp_std region (with
                blind ranges applied)
    """
    result = CheckResult("range", True, True)
    bin_centers = None

    for filepath in filepath_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if not re.fullmatch(tree_pattern, key):
                    continue
                if key in trees_opened:
                    continue
                trees_opened.append(key)

                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}
                    axis0 = hist.axis.Regular(
                        n_bins, limits["min"], limits["max"], name=expression
                    )
                    bin_centers = axis0.centers
                    h = Hist(axis0, name=f"{key} {expression}")
                    result.tree_data[key]["histograms"] = [h]
                    result.tree_data[key]["num_entries"] = 0
                    result.tree_data[key]["mean"] = 0
                    result.tree_data[key]["variance"] = 0
                    result.tree_data[key]["stddev"] = 0
                    result.tree_data[key]["num_entries_in_mean_window"] = 0

                values_obj = {}
                # Check if the branch is in the Tree or if the expression is correctly written
                try:
                    values_obj = obj.arrays(expression, library="np")
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [f"Missing branch in {key!r} with {e!r}"]
                    result.passed = False
                    result.can_combine = False
                    continue

                # Evaluate expression & apply limits
                test_array = values_obj[expression]
                test_array = test_array[
                    numpy.where(
                        (test_array < limits["max"]) & (test_array > limits["min"])
                    )
                ]

                # Apply blinding
                if blind_ranges is not None:
                    if isinstance(blind_ranges, dict):
                        # Take into account that there could be multiple regions to blind
                        blind_ranges = [blind_ranges]
                    for blind_range in blind_ranges:
                        lower, upper = blind_range["min"], blind_range["max"]
                        test_array = test_array[
                            ~((lower < test_array) & (test_array < upper))
                        ]

                # Fill histogram
                result.tree_data[key]["histograms"][0].fill(test_array)

                # Add to event counters
                result.tree_data[key]["num_entries"] += test_array.size

                if exp_mean is not None and exp_std is not None:
                    events_in_exp_mean_region = test_array[
                        (exp_mean - exp_std < test_array)
                        & (test_array < exp_mean + exp_std)
                    ]
                    result.tree_data[key][
                        "num_entries_in_mean_window"
                    ] += events_in_exp_mean_region.size

    # If no matches are found the check should be marked as failed, and can return early
    if len(result.tree_data) == 0:
        result.passed = False
        result.can_combine = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
        return result

    # Check the completely filled histograms
    if result.passed:
        for key in result.tree_data:
            # Get this tree's histogram
            h = result.tree_data[key]["histograms"][0]

            # Require at least one event
            # However, even if the histogram is empty, we want to be able to combine
            # the result later (so "can_combine" flag is left "True")
            if h.sum() == 0:
                result.passed = False
                result.messages += [f"No events found in range for Tree {key}"]
                continue

            # Calculate mean, variance, & standard deviation
            mean = sum(bin_centers * h.values()) / h.sum()
            result.tree_data[key]["mean"] = mean

            if h.sum() >= 2:
                variance = sum((bin_centers - mean) ** 2 * h.values()) / (h.sum() - 1)
            else:
                variance = 0
            result.tree_data[key]["variance"] = variance

            stddev = variance**0.5
            result.tree_data[key]["stddev"] = stddev

            # Apply expected mean requirement
            if exp_mean is not None and mean_tolerance is not None:
                delta_mean = abs(mean - exp_mean)
                if delta_mean > mean_tolerance:
                    result.passed = False
                    result.messages += [
                        f"The observed mean ({mean}) differs from the expected value by {delta_mean} (<={mean_tolerance} required)"
                    ]
                    continue

            # Apply expected standard deviation requirement
            if exp_std is not None and std_tolerance is not None:
                delta_std = abs(stddev - exp_std)
                if delta_std > std_tolerance:
                    result.passed = False
                    result.messages += [
                        (
                            f"The observed standard deviation ({stddev}) differs from the expected value by "
                            f"{delta_std} (<={std_tolerance} required)"
                        )
                    ]
                    continue

            # Histogram check successful
            result.messages += [
                f"Histogram of {expression} successfully filled from TTree {key} (contains {h.sum()} events)"
            ]

    return result


def range_check_nd(
    filepath_list,
    expressions,
    limits,
    n_bins,
    blind_ranges,
    tree_pattern,
):
    """N-dimensional range check.

    Produce 2-dimensional histograms of variables taken from a TTree object.

    Args:
        filepath_list (list[file-like]): List of paths to files to analyse
        expressions (dict): Name of the variables (or expressions) to be checked.
        limits (dict): Pre-defined ranges
        n_bins (dict): Number of bins for the histogram
        blind_ranges (dict): Regions to be blinded in the histogram
        tree_pattern (regex): A regular expression for the TTree object to check

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            histograms (list[Hist]): A list of filled histograms of the quantities defined by the expression parameters
            num_entries (float): The total number of entries in the histogram (with blind ranges applied)
    """
    result = CheckResult("range_nd", True, True)

    # Check if the number of variables matches expectations
    length_expr = len(expressions)
    length_limits = len(limits)
    if length_expr != 2 and length_expr != 3:
        result.messages += ["Expected two or three variables."]
        result.passed = False
        result.can_combine = False
        return result
    if length_expr != length_limits:
        result.messages += [
            "For each variable, a corresponding range should be defined."
        ]
        result.passed = False
        result.can_combine = False
        return result

    for filepath in filepath_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if not re.fullmatch(tree_pattern, key):
                    continue
                if key in trees_opened:
                    continue
                trees_opened.append(key)

                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}
                    result.tree_data[key]["histograms"] = []
                    for key_i, key_j in combinations(list(expressions.keys()), 2):
                        axis0 = hist.axis.Regular(
                            n_bins[key_i],
                            limits[key_i]["min"],
                            limits[key_i]["max"],
                            name=expressions[key_i],
                        )
                        axis1 = hist.axis.Regular(
                            n_bins[key_j],
                            limits[key_j]["min"],
                            limits[key_j]["max"],
                            name=expressions[key_j],
                        )
                        h = Hist(
                            axis0,
                            axis1,
                            name=f"{key} {expressions[key_i]}/{expressions[key_j]}",
                        )
                        result.tree_data[key]["histograms"] += [h]
                    if length_expr == 3:
                        for key_i, key_j, key_k in combinations(
                            list(expressions.keys()), 3
                        ):
                            axis0 = hist.axis.Regular(
                                n_bins[key_i],
                                limits[key_i]["min"],
                                limits[key_i]["max"],
                                name=expressions[key_i],
                            )
                            axis1 = hist.axis.Regular(
                                n_bins[key_j],
                                limits[key_j]["min"],
                                limits[key_j]["max"],
                                name=expressions[key_j],
                            )
                            axis2 = hist.axis.Regular(
                                n_bins[key_k],
                                limits[key_k]["min"],
                                limits[key_k]["max"],
                                name=expressions[key_k],
                            )
                            h = Hist(
                                axis0,
                                axis1,
                                axis2,
                                name=f"{key} {expressions[key_i]}/{expressions[key_j]}/{expressions[key_k]}",
                            )
                        result.tree_data[key]["histograms"] += [h]

                    result.tree_data[key]["num_entries"] = 0

                values_obj = {}
                list_expressions = list(expressions.values())
                # Check if the branch is present in the TTree or if the expressions are correctly written
                try:
                    values_obj = obj.arrays(list_expressions, library="np")
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [f"Missing branch in {key!r} with {e!r}"]
                    result.passed = False
                    result.can_combine = False
                    continue

                # Apply blinding
                if blind_ranges is not None:
                    mask_total = []
                    if isinstance(blind_ranges, dict):
                        # Take into account that there could be multiple regions to blind
                        blind_ranges = [blind_ranges]
                    for blind_range in blind_ranges:
                        indexes = []
                        mask = numpy.ones(
                            len(values_obj[list_expressions[0]]), dtype=bool
                        )
                        for ax, range_limits in blind_range.items():
                            lower, upper = range_limits["min"], range_limits["max"]
                            indexes = numpy.where(
                                (
                                    (values_obj[expressions[ax]] < upper)
                                    & (values_obj[expressions[ax]] > lower)
                                )
                            )
                            mask_tmp = numpy.zeros(
                                len(values_obj[list_expressions[0]]), dtype=bool
                            )
                            mask_tmp[indexes] = True
                            mask = numpy.logical_and(mask, mask_tmp)
                        mask_total.append(mask)
                    mask_final = numpy.zeros(
                        len(values_obj[list_expressions[0]]), dtype=bool
                    )
                    for mask in mask_total:
                        mask_final = numpy.logical_or(mask_final, mask)
                    for expr in expressions.values():
                        values_obj[expr] = values_obj[expr][~mask_final]

                # Fill the histograms
                list_keys = list(expressions.keys())
                hist_index = 0
                for key_i, key_j in combinations(list_keys, 2):
                    h = result.tree_data[key]["histograms"][hist_index]
                    h.fill(
                        values_obj[expressions[key_i]], values_obj[expressions[key_j]]
                    )
                    hist_index += 1
                # If more than two variables are given in input, return also 3D histograms
                if length_expr == 3:
                    for key_i, key_j, key_k in combinations(list_keys, 3):
                        h = result.tree_data[key]["histograms"][hist_index]
                        h.fill(
                            values_obj[expressions[key_i]],
                            values_obj[expressions[key_j]],
                            values_obj[expressions[key_k]],
                        )
                        hist_index += 1

                # Add to event counter
                result.tree_data[key]["num_entries"] += values_obj[
                    list_expressions[0]
                ].size

    # If no matches are found the check should be marked as failed, and can return early
    if len(result.tree_data) == 0:
        result.passed = False
        result.can_combine = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
        return result

    # Check the completely filled histograms
    if result.passed:
        for key in result.tree_data:
            for h in result.tree_data[key]["histograms"]:

                # Require at least one event
                if h.sum() == 0:
                    result.passed = False
                    result.messages += [f"No events found in range for Tree {key}"]
                    continue
                # Histogram check successful
                if len(h.axes) == 2:
                    message = f"Histogram of {h.axes[0].name}, {h.axes[1].name} successfully filled"
                    message += f" from TTree {key} (contains {h.sum()} events)"
                    result.messages += [message]
                else:
                    message = f"Histogram of {h.axes[0].name}, {h.axes[1].name}, {h.axes[2].name} successfully filled"
                    message += f" from TTree {key} (contains {h.sum()} events)"
                    result.messages += [message]
    return result


def num_entries_per_invpb(
    filepath_list,
    count_per_invpb,
    tree_pattern,
    lumi_pattern,
):
    """Number of entries per inverse picobarn check.

    Check that the matching TTree objects contain a minimum number of entries per unit luminosity (pb-1).

    Args:
        filepath_list (list[file-like]): List of paths to files to analyse
        count_per_invpb (float): The minimum number of entries per unit luminosity required
        tree_pattern (regex): A regular expression for the TTree objects to check
        lumi_pattern (regex): A regular expression for the TTree object containing the luminosity information

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            num_entries (float): The total number of events in the TTree
            lumi_invpb (float): The total luminosity, in inverse picobarns
            num_entries_per_invpb (float): The total number of events divided by the total luminosity
    """
    result = CheckResult("num_entries_per_invpb", True, True)

    lumi = 0
    for filepath in filepath_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue

                # If object is the decay TTree
                if re.fullmatch(tree_pattern, key):
                    if key in trees_opened:
                        continue
                    trees_opened.append(key)

                    # First time: initialise the CheckResult
                    if key not in result.tree_data:
                        result.tree_data[key] = {}
                        result.tree_data[key]["num_entries"] = 0
                        result.tree_data[key]["lumi_invpb"] = 0
                        result.tree_data[key]["num_entries_per_invpb"] = None

                    # Add number of entries to counter
                    result.tree_data[key]["num_entries"] += obj.num_entries

                # If object is lumi TTree
                if re.fullmatch(lumi_pattern, key):
                    try:
                        lumi_arr = obj["IntegratedLuminosity"].array(library="np")
                        err_lumi_arr = obj["IntegratedLuminosityErr"].array(
                            library="np"
                        )
                    except uproot.exceptions.KeyInFileError as e:
                        result.messages += [
                            f"Missing luminosity branch in {key!r} with error {e!r}"
                        ]
                        result.passed = False
                        result.can_combine = False
                        break

                    err_lumi_quad_sum = math.sqrt(numpy.sum(err_lumi_arr**2))
                    if err_lumi_quad_sum / numpy.sum(lumi_arr) >= 1:
                        result.passed = False
                        result.can_combine = False
                        result.messages += [
                            "Luminosity information is not reliable: 100% or greater relative uncertainty"
                        ]
                        break
                    # Add to luminosity counter
                    lumi += numpy.sum(lumi_arr)

    # If no matches are found the check should be marked as failed, and can return early
    if len(result.tree_data) == 0:
        result.passed = False
        result.can_combine = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
        return result

    if result.passed:
        for key in result.tree_data:
            if lumi == 0:
                result.passed = False
                result.can_combine = False
                result.messages += [
                    "Failed to get luminosity information (total luminosity = 0)"
                ]
                continue

            entries_per_lumi = round(result.tree_data[key]["num_entries"] / lumi, 2)
            result.tree_data[key]["lumi_invpb"] = lumi
            result.tree_data[key]["num_entries_per_invpb"] = entries_per_lumi
            if entries_per_lumi < count_per_invpb:
                result.passed = False
            result.messages += [
                f"Found {entries_per_lumi} entries per unit luminosity (pb-1) in {key} ({count_per_invpb} required)"
            ]

    return result


def range_check_bkg_subtracted(
    filepath_list,
    expression,
    limits,
    expr_for_subtraction,
    mean_sig,
    background_shift,
    background_window,
    signal_window,
    n_bins,
    blind_ranges,
    tree_pattern,
):
    """Range check with background subtraction.

    Check if there is at least one entry in the TTree object with a specific variable falling in a pre-defined range.
    The background-subtracted histogram is then produced as output. Background is subtracted assuming a linear
    distribution. In particular, signal ([m-s, m+s]) and background ([m-b-delta, m-b] U [m+b, m+b+delta]) windows have
    to be defined on a control variable. Then, one histogram is created for events falling in the signal region and
    another histogram is created for events falling in the background region. The subtraction, using the proper scaling
    factor, is finally performed. It is also possible to blind some regions.

    Args:
        filepath_list (list[file-like]): List of paths to files to analyse
        expression (str): Name of the variable (or expression depending on varibales in the TTree) to be checked
        limits (dict): Pre-defined range
        expr_for_subtraction (str): Name of the control variable (or expression depending on varibales in the TTree) to
            be used to perform background subtraction
        mean_sig (float): Expected mean value of expr_for_subtraction variable. The signal window will be centered
            around this value.
        background_shift (float):  Shift, w.r.t the "mean_sig" value, used to define the two background regions.
        background_window (float):  Length of the background windows (of expr_for_subtraction variable).
        signal_window (float): Length of the signal window (of expr_for_subtraction variable) used for background
            subtraction. The window is centered around the value of "mean_sig".
        n_bins (int): Number of bins for the histogram
        blind_ranges (dict): Regions to be blinded in the histogram
        tree_pattern (regex): A regular expression for the TTree object to check

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            histograms: A list of filled 1D histograms,
                Index 0: The control variable used to perform the subtraction
                Index 1: Events in the signal window
                Index 2: Events in the background window
                Index 3: The background-subtracted result
    """
    result = CheckResult("range_bkg_subtracted", True, True)

    for filepath in filepath_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if not re.fullmatch(tree_pattern, key):
                    continue
                if key in trees_opened:
                    continue
                trees_opened.append(key)

                # Calculate the min and max values of each of the two background regions.
                # By construction, the two intervals have the same length
                background_range_low = {
                    "min": mean_sig - background_shift - background_window,
                    "max": mean_sig - background_shift,
                }
                background_range_high = {
                    "min": mean_sig + background_shift,
                    "max": mean_sig + background_shift + background_window,
                }
                # Calculate the min and max values of each of the signal region
                signal_range = {
                    "min": mean_sig - signal_window / 2.0,
                    "max": mean_sig + signal_window / 2.0,
                }
                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}

                    # Create the histogram for the control variable used to perform background subtraction
                    axis0 = hist.axis.Regular(
                        n_bins,
                        background_range_low["min"],
                        background_range_high["max"],
                        name=expr_for_subtraction,
                    )
                    result.tree_data[key]["histograms"] = [
                        Hist(
                            axis0,
                            name=f"{key} {expression}",
                            storage=hist.storage.Weight(),
                        )
                    ]
                    # Add ranges to histogram metadata. Signal and background regions can be then highlighted in the final plot.
                    result.tree_data[key]["histograms"][0].metadata = [
                        background_range_low["min"],
                        background_range_low["max"],
                        background_range_high["min"],
                        background_range_high["max"],
                        signal_range["min"],
                        signal_range["max"],
                    ]

                    # Add signal & background region histograms (using same axis)
                    axis1 = hist.axis.Regular(
                        n_bins, limits["min"], limits["max"], name=expression
                    )
                    result.tree_data[key]["histograms"].append(
                        Hist(
                            axis1,
                            name=f"{key} {expression} signal",
                            storage=hist.storage.Weight(),
                        )
                    )
                    result.tree_data[key]["histograms"].append(
                        Hist(
                            axis1,
                            name=f"{key} {expression} background",
                            storage=hist.storage.Weight(),
                        )
                    )
                    result.tree_data[key]["histograms"].append(
                        Hist(
                            axis1,
                            name=f"{key} {expression} signal after bkg subtraction",
                            storage=hist.storage.Weight(),
                        )
                    )

                values_obj = {}
                # Check if the branch is in the Tree or if the expressions are correctly written
                try:
                    values_obj = obj.arrays(
                        [expr_for_subtraction, expression], library="np"
                    )
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [f"Missing branch in {key!r} with {e!r}"]
                    result.passed = False
                    result.can_combine = False
                    continue

                # Fill control variable histogram
                var_for_bkgsub_array = values_obj[expr_for_subtraction]
                result.tree_data[key]["histograms"][0].fill(var_for_bkgsub_array)

                # Select events in signal region
                cut_string = (
                    "("
                    + expr_for_subtraction
                    + ">"
                    + str(signal_range["min"])
                    + ") & ("
                    + expr_for_subtraction
                    + "<"
                    + str(signal_range["max"])
                    + ")"
                )
                values_sig = obj.arrays([expression], cut_string, library="np")
                test_array_sig = values_sig[expression]
                test_array_sig = test_array_sig[
                    numpy.where(
                        (test_array_sig < limits["max"])
                        & (test_array_sig > limits["min"])
                    )
                ]
                # Select events in background region
                cut_string = (
                    "( ("
                    + expr_for_subtraction
                    + ">"
                    + str(background_range_low["min"])
                    + ") & ("
                    + expr_for_subtraction
                    + "<"
                    + str(background_range_low["max"])
                    + ") ) | ( ("
                    + expr_for_subtraction
                    + ">"
                    + str(background_range_high["min"])
                    + ") & ("
                    + expr_for_subtraction
                    + "<"
                    + str(background_range_high["max"])
                    + ") )"
                )
                values_bkg = obj.arrays([expression], cut_string, library="np")
                test_array_bkg = values_bkg[expression]
                test_array_bkg = test_array_bkg[
                    numpy.where(
                        (test_array_bkg < limits["max"])
                        & (test_array_bkg > limits["min"])
                    )
                ]

                # Apply blinding
                if blind_ranges is not None:
                    if isinstance(blind_ranges, dict):
                        blind_ranges = [blind_ranges]
                        # Take into account that there could be multiple regions to blind
                    for blind_range in blind_ranges:
                        lower, upper = blind_range["min"], blind_range["max"]
                        test_array_sig = test_array_sig[
                            ~((lower < test_array_sig) & (test_array_sig < upper))
                        ]
                        test_array_bkg = test_array_bkg[
                            ~((lower < test_array_bkg) & (test_array_bkg < upper))
                        ]

                # Fill signal & background histograms
                result.tree_data[key]["histograms"][1].fill(test_array_sig)
                result.tree_data[key]["histograms"][2].fill(test_array_bkg)

    # If no matches are found the check should be marked as failed, and can return early
    if len(result.tree_data) == 0:
        result.passed = False
        result.can_combine = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
        return result

    if result.passed:
        for key in result.tree_data:

            # Require events in both signal and background histograms
            if (result.tree_data[key]["histograms"][1].view().value.sum() == 0) or (
                result.tree_data[key]["histograms"][2].view().value.sum() == 0
            ):
                result.passed = False
                result.messages += [
                    f"Not enough events for background subtraction found in range for Tree {key}"
                ]
                continue

            # Assume linear background distribution and evaluate fraction of background in the signal region
            alpha = 2.0 * background_window / signal_window

            # Histogram subtraction
            hsub = (
                result.tree_data[key]["histograms"][1]
                + (-1 * alpha) * result.tree_data[key]["histograms"][2]
            )
            result.tree_data[key]["histograms"][3] = hsub

            result.messages += [
                f"Background subtraction performed successfully for Tree {key}"
            ]

    return result


def branches_exist(
    filepath_list,
    branches,
    tree_pattern,
):
    """Branches exist check.

    Check that all matching TTree objects contain a minimum number of entries.

    Args:
        filepath_list: List of paths to files to analyse
        branches: List of branches that will be required to exist in TTree objects
        tree_pattern: A regular expression for the TTree objects to check

    Returns:
        A CheckResult object, which for each tree contains no tree_data key/values (an empty dict)
    """
    result = CheckResult("branches_exist", True, True)
    for filepath in filepath_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if not re.fullmatch(tree_pattern, key):
                    continue
                if key in trees_opened:
                    continue
                trees_opened.append(key)

                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}

                # Check that branches exist
                if not set(branches).issubset(obj.keys()):
                    missing_branches = list(set(branches) - set(obj.keys()))
                    result.passed = False
                    result.can_combine = False
                    result.messages += [
                        f"Required branches not found in Tree {key}: {missing_branches}"
                    ]

    # If no matches are found the check should be marked as failed, and can return early
    if len(result.tree_data) == 0:
        result.passed = False
        result.can_combine = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
        return result

    if result.passed:
        for key, _data in result.tree_data.items():
            result.messages += [f"All required branches were found in Tree {key}"]

    return result
