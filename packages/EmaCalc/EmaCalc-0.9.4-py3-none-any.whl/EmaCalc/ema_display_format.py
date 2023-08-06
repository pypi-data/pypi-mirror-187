"""This module includes functions to format output displays of
EmaModel results, in graphic and textual form.

Plot properties may be controlled by
1: specifying matplotlib style sheet(s) by keyword argument mpl_style
2: setting specific matplotlib parameters at runtime by keyword argument mpl_params
3: setting specific parameters in FMT, e.g., 'colors' and 'markers'

*** Version History:
* Version 0.9.4:
2023-01-22, Bug fix in output file name creation, to avoid problem under Windows.
            Added 'interaction_sep' and 'condition_sep' in FMT dict, for user control.
            Added try...catch for any errors in ResultPlot.save() and ResultTable.save()

* Version 0.9.3:
2022-07-27, allow setting matplotlib style sheet(s) and individual matplotlib params
2022-07-12, Special DiffTable class to suppress numerical index in save.
2022-07-12, Simplified header in tab_credible_diff.

* Version 0.9.2:
2022-06-17, fig_percentiles: allow caller to set y_min, y_max
2022-06-04, suppress integer index column in Table.save. New support function harmonize_ylim
2022-06-03, tab_credible_diff with clarified header

* Version 0.9.1:
2022-04-10, fig_percentiles using DataFrame table as input
2022-03-30, make all tables as pandas DataFrame objects

* Version 0.8:
2022-02-15, minor cleanup of tab_percentile: allow cdf=None, header percentile format .1f

* Version 0.7.1:
2022-01-21, minor fix in tab_cred_diff to avoid credibility == 100.0%
2022-01-08, set_tight_layout for all ResultPlot objects
2022-01-13, changed EmaDisplaySet.show format argument: show_intervals -> grade_thresholds

* Version 0.7:
2021-12-19, function nap_table to format NAP results

2021-11-07, copied and modified PairedCompCalc -> EmaCalc
"""
# *** AVOID explicit plot-style commands, rely on rcParams or style sheets instead
# *** Try package pathvalidate to check that result filenames are allowed ? ***
# *** Or just try...catch ?

import numpy as np
from itertools import cycle, product
import matplotlib.pyplot as plt
import logging
import pandas as pd

from .ema_file import Table

# plt.rcParams.update({'figure.max_open_warning': 0})
# suppress warning for many open figures
# plt.rcParams.update({'axes.labelsize': 'x-large'})  # use kwarg mpl_params instead
# plt.rcParams.update({'axes.labelweight': 'bold'})

logger = logging.getLogger(__name__)


FMT = {'colors': 'rbgk',  # to distinguish results in plots, cyclic use
       'markers': 'oxs*_',  # corresponding markers, cyclic use
       'interaction_sep': '\u00D7',  # mult.sign. separating situation labels in result file names
       'condition_sep': '_',  # separating attribute and its conditioning situation(s) in file names
       }

# NOTE: FMT['colors'] and FMT['markers'] override matplotlib.rcParams.axes.prop_cycle,
#   because prop_cycle allows only equal lengths of 'colors' and 'markers'.
#   The FMT['colors'] and FMT['markers'] are used cyclically,
#   so the default sequences with unequal lengths will combine
#   into a sequence with many combinations, before repeating itself.


def set_format_param(mpl_style=None, mpl_params=None, **kwargs):
    """Set / modify format parameters.
    Called before any displays are generated.
    :param mpl_style: (optional) matplotlib style sheet, or list of style sheets
    :param mpl_params: (optional) dict with matplotlib (k, v) rcParam settings
    :param kwargs: dict with any formatting variables
    :return: None
    """
    if mpl_style is not None:
        plt.style.use(mpl_style)
    if mpl_params is not None:
        plt.rcParams.update(mpl_params)
    other_fmt = dict()
    for (k, v) in kwargs.items():
        k = k.lower()
        if k in FMT:
            FMT[k] = v
        else:
            other_fmt[k] = v
    if len(other_fmt) > 0:
        logger.warning(f'Parameters {other_fmt} unknown, not used.')


# ---------------------------- Basic Result Classes

class ResultPlot:
    """Container for a single graph instance
    """
    def __init__(self, ax, name):
        """
        :param ax: matplotlib Axes instance containing the graph
        :param name: string identifying the plot; used as file name
        """
        self.ax = ax
        self.name = name

    @property
    def fig(self):
        return self.ax.figure

    def save(self, path,
             figure_format,
             **kwargs):
        """Save figure to given path
        :param path: Path to directory where figure has been saved
        :param figure_format: figure-format string code -> file-name suffix
        :param kwargs (optional) any additional kwargs, *** NOT USED ***
        :return: None
        """
        # *** select subset of kwargs allowed by savefig() ?
        # NO, depends on Matplotlib backend!
        f = (path / self.name).with_suffix('.' + figure_format)
        try:
            self.fig.savefig(f)
        except Exception as e:  # any error, just warn and continue
            logger.warning(f'Could not save plot to {f}. Error: {e}')


class ResultTable(Table):
    """A pd.DataFrame table subclass, with a name and special save method
    """
    def __init__(self, df, name):
        """
        :param df: a Table(pd.DataFrame) instance
        :param name: file name for saving the table
        """
        super().__init__(df)
        self.name = name

    def save(self, path,
             table_format='txt',
             **kwargs):
        """Save table to file.
        :param path: Path to directory for saving self.
            suffix is determined by FMT['table_format'] anyway
        :param table_format: table-format string code -> file-name suffix
        :param kwargs: (optional) any additional arguments to pandas writer function
        :return: None
        """
        f = (path / self.name).with_suffix('.' + table_format)
        try:
            super().save(f, **kwargs)
        except Exception as e:  # any error, just warn and continue
            logger.warning(f'Could not save result table. Error: {e}')


class DiffTable(ResultTable):
    """Special subclass suppressing index in save method
    """
    def save(self, path,
             **kwargs):
        """Save table to file.
        :param path: Path to directory for saving self.
            suffix is determined by FMT['table_format'] anyway
        :param table_format: table-format string code -> file-name suffix
        :param kwargs: (optional) any additional arguments to pandas writer function
        :return: None
        """
        if 'index' not in kwargs:
            kwargs['index'] = False  # override Pandas default = True
        super().save(path, **kwargs)


# ---------------------------------------- Formatting functions:

def fig_percentiles(df,
                    case_labels,
                    y_label='',
                    file_label='',
                    cat_limits=None,
                    x_space=0.3,
                    colors=FMT['colors'],
                    markers=FMT['markers'],
                    y_min=None,
                    y_max=None,
                    **kwargs):
    """create a figure with percentile results
    as defined in a given pd.DataFrame instance
    :param df: pd.DataFrame instance with primary percentile data, with
        one row for each case category, as defined in df.index elements
        one column for each percentile value.
    :param case_labels: dict with elements (case_factor_i, case_labels_i),
        that were used to construct table df, with
        case_factor_i = key string for i-th case dimension,
            = name of i-th level of df.index
        case_labels_i = list of labels for i-th case dimension
            = categories in df.index.levels[i]
        df.n_rows == prod_i len(case_labels_i)
    :param y_label: (optional) string for y-axis label
    :param cat_limits: 1D array with response-interval limits (medians)
    :param file_label: (optional) string as first part of file name
    :param x_space: (optional) min space outside min and max x_tick values
    :param colors: (optional) sequence of color codes to separate results in plots
    :param markers: (optional) sequence of marker codes to separate results in plots
        len(colors) != len(markers) -> many different combinations
    :param y_min: (optional) enforced lower limit of vertical axis
    :param y_max: (optional) enforced upper limit of vertical axis
    :param kwargs: (optional) dict with any additional keyword arguments for plot commands.
    :return: ResultPlot instance with plot axis with all results
    NOTE: plot will use df.index.level[0] categories as x-axis labels,
    and index.level[1:] as plot labels in the legend
    """
    def plot_one_case(case_i, x, y_i, c, m):
        """
        :param case_i: case label
        :param x: 1D array with x values
        :param y_i: 2D array with y values
            y_i[p, i] = p-th percentile value for x[i]
            len(x) == y_i.shape[-1]
        :param c: color code
        :param m: marker code
        :return: None
        """
        n_perc = y_i.shape[0]
        if n_perc == 1:  # only marker
            line = ax.plot(x, y_i[0],
                           linestyle='', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        elif n_perc == 2:  # only vertical range, no markers
            line = ax.plot(np.tile(x, (2, 1)),
                           y_i,
                           linestyle='solid', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        else:  # vertical range, and markers for intermediate percentiles
            ax.plot(np.tile(x, (2, 1)),
                    [y_i[0], y_i[-1]],
                    linestyle='solid', color=c,
                    **kwargs)
            line = ax.plot(np.tile(x, (y_i.shape[0] - 2, 1)),
                           y_i[1:-1],
                           linestyle='solid', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        line[0].set_label(str(case_head) + '=' + str(case_i))
    # ----------------------------------------------------------

    case_keys = [*case_labels.keys()]
    case_cats = [*case_labels.values()]
    # *** df.index.levels are NOT used because they are sorted alphabetically, NOT in tabulated order
    assert df.shape[0] == np.prod([len(cc_i) for cc_i in case_cats]), 'case_labels must match df size'
    x_label = case_keys[0]
    x_tick_labels = list(case_cats[0])
    if len(case_keys) == 1:
        (case_head, case_list) = ('', [''])  # make ONE empty sub-case to facilitate indexing
    elif len(case_keys) == 2:
        (case_head, case_list) = (case_keys[1], case_cats[1])
    else:
        (case_head, case_list) = (case_keys[1:], [*product(*case_cats[1:])])
    n_cases = len(case_list)
    # ------------------------------------------------------------------
    fig, ax = plt.subplots()
    dx = (1. - x_space) / n_cases
    # = x step between range plots for separate cases
    x = np.arange(len(x_tick_labels)) - (n_cases - 1) * dx / 2
    # = x position for first case
    if df.index.nlevels == 1:
        plot_one_case('', x, df.loc[x_tick_labels].values.T,
                      colors[0], markers[0])
    else:
        for (case_i, c, m) in zip(case_list,
                                  cycle(colors),
                                  cycle(markers)):
            y_i = df.xs(case_i, level=case_head)
            y_i = y_i.loc[x_tick_labels].values.T
            plot_one_case(case_i, x, y_i, c, m)
            x += dx
    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -x_space)
    x_max = max(x_max, len(x_tick_labels) - 1 + x_space)
    ax.set_xlim(x_min, x_max)
    if cat_limits is not None:
        _plot_response_intervals(ax, cat_limits)
    ax.set_xticks(np.arange(len(x_tick_labels)))
    xticks = [str(c) for c in x_tick_labels]
    ax.set_xticklabels(xticks,
                       **_x_tick_style(xticks))
    (y0, y1) = ax.get_ylim()
    if y_min is not None:
        y0 = y_min
    if y_max is not None:
        y1 = y_max
    ax.set_ylim(y0, y1)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if len(case_list) > 1:
        ax.legend(loc='best')
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(df.index.names)
    fig.set_tight_layout(tight=True)  # **** let rcParams control this ? ****
    return ResultPlot(ax, name=f_name)


def _plot_response_intervals(ax, c_lim):
    """plot horizontal lines to indicate response-category intervals
    :param ax: axis object
    :param c_lim: 1D array with scalar interval limits
    :return: None
    """
    (x_min, x_max) = ax.get_xlim()
    return ax.hlines(c_lim, x_min, x_max,
                     colors=plt.rcParams['axes.edgecolor'],
                     linewidth=0.2 * plt.rcParams['lines.linewidth'])


def fig_category_barplot(df,
                         x_label,
                         y_label,
                         file_label='',
                         colors=FMT['colors'],
                         y_min=None,
                         y_max=None,
                         mpl_params=None,
                         **kwargs
                         ):
    """Bar plot of DataFrame values,
    to be displayed with one sequence of vertical bars along x-axis for each row,
    with one bar for each column,
    suitable, e.g., for plotting attribute_grade_counts
    :param df: a DataFrame instance
    :param x_label: x-axis label string
    :param y_label: y-axis label string
    :param file_label: plot name for saving file
    :param colors: (optional) color sequence
    :param y_min: (optional) enforced lower limit of vertical axis *** NOT USED
    :param y_max: (optional) enforced upper limit of vertical axis *** NOT USED
    :param mpl_param: (optional) dict with matplotlib rcParam settings
    :param kwargs: (optional) dict with keyword arguments for plot commands *** NOT USED
    :return: a ResultPlot instance
    """
    if mpl_params is not None:
        plt.rcParams.update(mpl_params)
    fig, ax = plt.subplots()
    (n_cases, n_x) = df.shape
    x = np.arange(n_x)
    w = 0.8 / n_cases
    if len(df.index.names) > 1:
        case_head = tuple(df.index.names)
    else:
        case_head = df.index.name
    x_dev = w * (np.arange(n_cases) - (n_cases - 1) / 2)
    for (y, d, c, case) in zip(df.to_numpy(),
                               x_dev,
                               cycle(colors),
                               df.index.values):
        ax.bar(x + d, height=y,
               width=w, color=c,
               label=str(case_head) + '= ' + str(case))
    ax.set_xticks(np.arange(n_x))
    xticks = [str(c) for c in df.columns.values]
    ax.set_xticklabels(xticks,
                       **_x_tick_style(xticks))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if n_cases > 1:
        ax.legend(loc='best')
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(df.index.names)
    fig.set_tight_layout(tight=True)
    return ResultPlot(ax, name=f_name)


# ----------------------------------------- table displays:

def tab_percentiles(q_perc,
                    perc,
                    case_labels,
                    file_label=''
                    ):
    """Create pd.DataFrame with all percentile results.
    This function is general and can handle any dimensionality of the data.
    :param q_perc: 2D or mD array with quality percentiles, stored as
        q_perc[p, c0,...] = p-th percentile in (c0,...)-th case condition
    :param perc: sequence of percentage values in range 0-100
        len(perc) == q_perc.shape[0]
    :param case_labels: (sequence OR ???) dict with elements (case_factor_i, case_labels_i), where
        case_factor_i is key string for i-th case dimension,
        case_labels_i is list of labels for i-th case dimension
        in the same order as the index order of q_perc, i.e.,
        len(case_labels_i) == q_perc.shape[i+1].
        Thus, q_perc[p, ...,c_i,...] = p-th percentile for case_labels_i[c_i], i = 0,...,
    :param file_label: (optional) string as first part of file name
    :return: a ResultTable(pd.DataFrame) instance,
        with one column for each percentile,
        and one row for each combination product of case labels.
        Number of table rows == prod q_perc.shape[1:] == prod_i len(case_labels_i)
    """
    case_labels = dict(case_labels)  # if not already dict, *** require dict ? ******
    case_shape = tuple(len(c_labels) for c_labels in case_labels.values())
    n_rows = np.prod(case_shape, dtype=int)
    # = number of table rows as defined by case_labels
    n_perc = len(perc)
    assert n_perc == q_perc.shape[0], 'Incompatible q_perc.shape[0] != n of percentiles'
    assert n_rows == np.prod(q_perc.shape[1:], dtype=int), 'Incompatible size of case_list and q_perc'
    assert case_shape == q_perc.shape[1:], 'Incompatible shape of q_perc and case_labels'
    df = pd.DataFrame({f'{p_i:.1f}%': q_i
                       for (p_i, q_i) in zip(perc,
                                             q_perc.reshape((n_perc, -1)))},
                      index=pd.MultiIndex.from_product([*case_labels.values()],
                                                       names=[*case_labels.keys()]))
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(case_labels.keys())
    return ResultTable(df, name=f_name)


def tab_credible_diff(diff,
                      diff_labels,
                      diff_head,
                      cred_head,
                      case_labels=(),
                      case_head=(),
                      y_label='',
                      file_label='',
                      and_label='and',  # label in And column
                      and_head=('', '')
                      ):
    """Create table with credible differences among results
    :param diff: list of tuples ((i,j), p) OR ((i,j,c), p),
        defining jointly credible differences, indicating that
        prob{ quality of diff_labels[i] > quality of diff_labels[j]}, OR
        prob{ quality of diff_labels[i] > quality of diff_labels[j] | case_labels[c] }
        AND all previous pairs } == p
    :param diff_labels: list of tuples with labels of compared random-vector elements
        diff_labels[i] = (label_0,...)
        diff[...] == ((i,j, c), p) <=> diff_labels[i] > diff_labels[j] with prob p,
            at case_labels[c], if case_labels are defined.
        len(diff_labels) == max possible diff category index (i, j)
    :param diff_head: tuple of keys for heading of diff_labels column in table
        len(diff_head) == len(diff_labels[i]) for all i
    :param cred_head: string for header of Credibility column
    :param case_labels: (optional) sequence of tuples
        case_labels[c] == (case_label1, case_label2, ...), such that
        diff[...] == ((i,j, c), p) <=> diff[...] is valid given case_labels[c]
        len(case_labels) == max possible case index c in diff
    :param case_head: (optional) tuple of case keys, one for each case-dimension table column
        len(case_head) == len(case_labels[c]) for any c
    :param y_label: (optional) string with label of tabulated attribute
    :param file_label: (optional) string for first part of file name
    :param and_label: (optional) joining AND label in first column
    :param and_head: (optional) tuple with two strings for head first column
    :return: ResultTable object with header lines + one line for each credible difference
    """
    if len(diff) == 0:
        return None
    y_head_i = y_label + ' >'
    y_head_j = y_label
    # --------------------- table columns as dicts:
    col = {and_head:  [' '] + [and_label] * (len(diff) - 1)}  # first column with only AND flags
    # --------- column(s) for higher results:
    diff_i = [diff_labels[d[0][0]]
              for d in diff]
    col |= {(y_head_i, d_head_k): [d_val[k] for d_val in diff_i]
            for (k, d_head_k) in enumerate(diff_head)}
    # --------- column(s) for lower results:
    diff_j = [diff_labels[d[0][1]]
              for d in diff]
    col |= {(y_head_j, d_head_k): [d_val[k] for d_val in diff_j]
            for (k, d_head_k) in enumerate(diff_head)}  # cols for lesser results
    # --------- column(s) for optional case labels:
    if len(case_head) > 0:
        diff_c = [case_labels[d[0][2]]
                  for d in diff]
        col |= {('', c_head_k): [c_val[k] for c_val in diff_c]
                for (k, c_head_k) in enumerate(case_head)}
    # --------- credibility column:
    col |= {('', cred_head): [d[1] for d in diff]}
    df = pd.DataFrame(col)
    # each column name is a tuple with two elements -> MultiIndex with two levels
    df = df.reindex(columns=pd.MultiIndex.from_tuples(df.columns))
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(diff_head) + '-diff'
    if len(case_head) > 0:
        f_name += FMT['condition_sep'] + FMT['interaction_sep'].join(case_head)
    return DiffTable(df, name=f_name)


# -------------------------------------- display adjustment functions

def harmonize_ylim(axes_list, y_min=None, y_max=None):
    """Adjust several plots to equal vertical range
    :param axes_list: sequence of plt.Axes instances
    :param y_min: (optional) extra user-defined minimum
    :param y_max: (optional) extra user-defined maximum
    :return: None
    """
    y0 = min(*(ax.get_ylim()[0]
               for ax in axes_list))
    if y_min is not None:
        y0 = min(y0, y_min)
    y1 = max(*(ax.get_ylim()[1]
               for ax in axes_list))
    if y_max is not None:
        y1 = max(y1, y_max)
    for ax in axes_list:
        ax.set_ylim(y0, y1)


# -------------------------------------- private help functions
def _x_tick_style(labels):
    """Select xtick properties to avoid tick-label clutter
    :param labels: list of tick label strings
    :return: dict with keyword arguments for set_xticklabels
    """
    maxL = max(len(l) for l in labels)
    rotate_x_label = maxL * len(labels) > 75  # ad hoc criterion
    if rotate_x_label:
         style = dict(rotation=15, horizontalalignment='right')
    else:
        style = dict(rotation='horizontal', horizontalalignment='center')
    return style
