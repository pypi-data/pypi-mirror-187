"""Script to simulate an Ecological Momentary Assessment (EMA) study.
Collects all simulated EMA records in files,
as if the data had been gathered in a real experiment,
and runs the analysis.

A simulated experiment may include
one or more Groups of participants randomly drawn from separate Population(s),
with each participant performing several simulated EMA recordings.
Each EMA record includes
(1) a nominal SITUATION, specified in one or more Situation Dimensions,
(2) ordinal ratings of zero, one or more perceptual ATTRIBUTE(s).


*** Usage:
For first demo: Just run this script and look at the generated data files and the results.

For planning an EMA study:
Copy and edit this script and run it for any desired simulation.

Given some anticipated true effect-sizes in the patterns of population characteristics,
the simulation will indicate whether these effects can be reliably demonstrated
in a planned study, given the limited number of participants,
and the limited number of EMA recordings by each participant.


*** Version history:
* Version 0.9.3:
2022-08-17, minor cleanup adapting to minor changes in some package modules.

* Version 0.9.1:
2022-04-04, all result tables generated and saved as Pandas DataFrame instances
2022-03-27, NAP and mean-grades results directly from raw data in ema_data.EmaDataSet
2022-03-21, using Pandas DataFrame format in EmaDataSet, allowing many input file formats

* Version 0.7.1:
2022-01-19, allow set_random_seed for exactly reproducible results

* Version 0.7: minor update to include new calculation and display functions

* Version 0.6:
2021-12-08, tested methods for restrict_attribute, restrict_threshold

* Version 0.5:
2021-11-16, first functional version
2021-11-21, cleaned and tested beta version
"""
# -------- __main__ check to prevent multiprocessor sub-tasks to re-run this script
if __name__ == '__main__':
    import numpy as np
    from pathlib import Path
    import logging
    import pickle

    from EmaCalc.ema_simulation import EmaSimPopulation, EmaSimExperiment
    from EmaCalc.ema_simulation import SubjectThurstone, SubjectBradley

    from EmaCalc.ema_data import EmaFrame, EmaDataSet
    from EmaCalc.ema_model import EmaModel
    from EmaCalc.ema_display import EmaDisplaySet
    from EmaCalc import ema_logging, __version__
    from EmaCalc.ema_display_format import harmonize_ylim

    # ------------ Set simulator random seed for reproducible results
    # from EmaCalc.ema_simulation import set_sim_seed
    # set_sim_seed(12345)  # for reproducible results. ONLY FOR TEST OR DEMO

    # ------------------------ Set up working directory and result logging:
    work_path = Path.home() / 'Documents' / 'EMA_sim'  # or whatever...
    data_path = work_path / 'data'  # or whatever
    result_path = work_path / 'result'  # or whatever

    model_file = 'test_ema_model.pkl'  # saved model file
    experiment_file = 'test_ema_experiment.pkl'  # saved EmaSimExperiment

    ema_logging.setup(save_path=result_path,
                      log_file='run_sim_log.txt')  # to save the log file

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logger.info(f'*** Running EmaCalc version {__version__} ***')

    # --------------- Define Experimental Framework: Situations, Attributes, and Grades

    emf = EmaFrame.setup(situations={'Phase': ('',),  # Test phase(s), only one unlabelled
                                     'HA': ('A', 'B'),  # two Hearing-aid programs
                                     'CoSS': [f'C{i}' for i in range(1, 8)],  # Seven CoSS categories
                                     },
                         phase_key='Phase',
                         attributes={'Speech': ['Very Hard',
                                                'Hard',
                                                'Easy',
                                                'Very Easy',
                                                'Perfect'],
                                     'Comfort': ['Bad',
                                                 'Not Good',
                                                 'Not Bad',
                                                 'Good']}
                         )
    # NOTE: situations and attributes keys will be parts of result file names,
    # so they can include only characters allowed in file names.

    # NOTE: situations and attributes always analyzed as Categorical variables,
    # even if the categories / grades are defined by numeric values.
    # The rank order of attribute grades is defined by the order as listed here,
    # not by, e.g., alphabetical or numerical order of the grade labels.

    # NOTE: if EQUAL grades are used for more than one attribute,
    # the model still assumes separate rating scales for each attribute.
    # However, if grade sequences are IDENTICAL objects for more than one attribute,
    # the model uses the SAME rating scale for those attributes.

    # Response thresholds are always estimated separately for each participant.

    # --------------- Define Population(s) to be simulated:

    # Not necessarily normalized probability-mass arrays
    pop0_situation_prob = np.ones((2, 7))  # with HA = A, B

    # pop0_situation_prob.shape == emf.situation_shape
    # OR == emf.situation_shape[1:] if emf.situation_shape[0] == 1, i.e., only one phase

    # --------- Population mean for Attribute 'Speech', in subject_class scale units

    pop0_speech_mean = np.array([[0., 0., 0., 0., 0., 0., 0.],     # with 'HA' = 'A'
                                 [3., 3., 3., 0., -3., -3., -3]])  # with 'HA' = 'B'
    pop0_speech_mean[1] += 0.5  # add fixed difference between HA (B - A)
    pop0_comfort_mean = pop0_speech_mean[[1, 0], :]  # opposite pattern to 'Speech'

    pop_0 = EmaSimPopulation(emf,
                             situation_prob=pop0_situation_prob,
                             attribute_mean={'Speech': pop0_speech_mean,
                                             'Comfort': pop0_comfort_mean},
                             log_situation_std=0.,  # inter-individual standard deviation of log prob
                             attribute_std=0.5,  # inter-individual standard deviation of attribute locations
                             response_width_mean=1.5,  # response interval width in subject_class units
                             log_response_width_std=0.3,  # inter-individual random threshold variations
                             # subject_class=SubjectBradley,  # default
                             id='Pop0'
                             )
    # Optionally, define other populations here,
    pop1_situation_prob = pop0_situation_prob
    pop1_speech_mean = np.array([[0., 0., 0., 0., 0., 0., 0.],     # with 'HA' = 'A'
                                 [0., 0., 0., 0., 0., 0., 0.]])  # with 'HA' = 'B'
    pop1_speech_mean[0] -= 1.  # add fixed difference between HA (B - A)
    pop1_speech_mean[1] += 1.  # add fixed difference between HA (B - A)
    pop1_comfort_mean = pop1_speech_mean[[1, 0], :]  # opposite pattern to 'Speech'
    # pop1_comfort_mean = pop0_comfort_mean  # SAME as pop0
    pop_1 = EmaSimPopulation(emf,
                             situation_prob=pop1_situation_prob,
                             attribute_mean={'Speech': pop1_speech_mean,
                                             'Comfort': pop1_comfort_mean},
                             log_situation_std=0.,  # inter-individual standard deviation of log prob
                             attribute_std=0.5,  # inter-individual standard deviation of attribute traits
                             response_width_mean=1.5,  # response interval width in subject_class units
                             log_response_width_std=0.3,  # inter-individual random threshold variations
                             # subject_class=SubjectBradley,  # default
                             id='Pop1'
                             )
    # with SAME EmaFrame, but different situation_prob and/or mean Attribute values

    # ------------------ Generate Experiment with one Group of participants sampled from each Population:
    ema_exp = EmaSimExperiment(emf,
                               groups={(('Age', 'old'),): pop_0.gen_group(n_participants=20),
                                       (('Age', 'young'),): pop_1.gen_group(n_participants=15)
                                       })
    # NOTE: group keys MUST be a tuple of one or more PAIRS (g_factor, g_category)
    # because groups may be defined hiearchically
    #
    logger.info(f'ema_exp= {ema_exp}')
    # ema_exp defines true parameter values for Population(s) and all participants in each Group

    # -------- (Optional) Save EmaSimExperiment instance with true parameter values
    with (work_path / experiment_file).open('wb') as f:
        pickle.dump(ema_exp, f)

    # ------------------------- Generate EMA data for all participants in all Groups:

    ds = ema_exp.gen_dataset(min_ema=30,    # min n of EMA records per participant
                             max_ema=70)    # max n of EMA records per participant
    # = a complete EmaDataSet instance with simulated EMA records for all participants

    # Optionally, save all data in a set of data files, one for each participant
    file_format = 'csv'  # 'xlsx', or other format that Pandas can handle
    ds.save(data_path, allow_over_write=True, fmt=file_format,
            # participant='file',  # default for all file formats
            # participant='sheet',  # participant ID can be stored in xlsx sheet title
            )
    logging.info('Simulated EMA data saved in ' + str(data_path) + f' as {file_format} files')

    # ----------------- (Optional) show mean grades and NAP results for all participants

    mean_grades = ds.attribute_grade_mean(group_by=('HA', 'CoSS'))
    mean_grades.save(result_path / 'Attribute_mean_grades.txt', float_format='%.2f')
    # mean_grades.save(result_path / 'Attribute_mean_grades.csv')  # for input to other analysis
    logger.info(f'Attribute_mean_grades saved in {result_path}')

    # nap = ds.nap_table(sc='HA', nap_cat=['A', 'B'], grouping=('CoSS',))  # grouped results
    nap = ds.nap_table(sit='HA', nap_cat=['A', 'B'], p=0.95)
    # default aggregated across other situation dimensions
    nap.save(result_path / 'NAP.txt')
    # nap.save(result_path / 'NAP.csv')  # for input to other analysis
    logger.info(f'NAP results saved in {result_path}')

    # ------------------------------- Learn Analysis Model from simulated data set:

    # -------- Test re-loading simulated data from saved files (optional):
    logging.info('Simulated EMA data re-loaded from ' + str(data_path) + f' as {file_format} files')
    ds = EmaDataSet.load(emf, data_path,
                         fmt=file_format,
                         # grouping=None,  # default: include all participants as ONE unnamed group
                         grouping={'Age': ('old',),  # analyze only Age=old
                                   },
                         # grouping={'Age': ('young','old')},  # analyze both Age groups separately
                         participant='file',  # 'sheet' only for Excel-style file formats
                         )

    logger.info(f'Using data ds=\n{ds}')

    # Model ordinal-regression effects of situations on each Attribute:
    # regression_effects = ['HA',     # main linear regression effect only
    #                       'CoSS',   # main linear regression effect only
    #                       # 'Phase',  # if there are several phase categories
    #                       ]
    regression_effects = [('HA', 'CoSS')  # joint effects, main AND interaction
                          # 'Phase',  # if there are several phase categories
                          ]
    # NOTE: regression effects may include any combination of situation dimensions, but
    # including ALL interactions -> MANY model parameters,
    # possibly -> less precise estimation for each parameter.

    # In this example: ['HA', 'CoSS'] -> 2 + (7 - 1) = 8 regression-effect parameters
    #                ['CoSS', 'HA'] -> 7 + (2 - 1) = 8 regression-effect parameters
    #                [('HA', 'CoSS')] -> 2 * 7 = 14 regression-effect parameters

    emm = EmaModel.initialize(ds,
                              effects=regression_effects,
                              max_n_comp=10,
                              restrict_attribute=False,  # default
                              restrict_threshold=True,   # default
                              # seed=12345  # ONLY if reproducible results are required
                              )
    # max_n_comp = max number of mixture components in population model
    # restrict_attribute=True -> force attribute mean values centered at zero
    # restrict_threshold=True -> force response thresholds centered at zero
    # for each respondent and each sample of each attribute

    ll = emm.learn(max_hours=2., max_minutes=0.)
    logger.info('ll= ' + np.array2string(np.array(ll), precision=5))
    emm.prune()  # keep only active mixture components

    # -------- Save learned EmaModel instance (optional):
    with (work_path / model_file).open('wb') as f:
        pickle.dump(emm, f)

    # ------------------------------- generate all result displays:

    emd = EmaDisplaySet.show(emm,
                             situations=['CoSS',  # CoSS profile, aggregated across HA
                                         ('CoSS', 'HA'),  # CoSS profiles, conditional on HA
                                         ('HA', 'CoSS'),  # HA profiles, conditional on CoSS
                                         ],
                             attributes=[('Speech', 'CoSS'),     # Speech, main effect of CoSS
                                         ('Speech', 'HA'),       # Speech, main effect of HA
                                         ('Speech', ('CoSS', 'HA')),    # joint effect of both
                                         ('Comfort', ('CoSS', 'HA'))],  # joint effect of both
                             random_individual=True,  # random individual in the population
                             population_mean=True,  # population mean
                             participants=False,  # individual results: True -> MANY plots and tables
                             grade_thresholds=True,  # response thresholds in attribute plots
                             percentiles=[2.5, 25, 50, 75, 97.5],  # in profile plots and tables
                             credibility_limit=0.7,  # minimum credibility in difference tables
                             mpl_params={'figure.max_open_warning': 0,
                                         'axes.labelsize': 'x-large'},  # -> matplotlib.rcParam
                             # mpl_style='my_style_sheet',
                             # ... any other ema_display.FMT settings
                             )
    # NOTE: joint (=interaction) effects are correct only if included in EmaModel regression effects

    # ------------------------------- (optionally) edit display elements, if desired
    # for g_disp in emd.groups.values():
    #     harmonize_ylim([g_disp.population_mean.attributes[('Speech', ('CoSS', 'HA'))].plot.ax,
    #                     g_disp.random_individual.attributes[('Speech', ('CoSS', 'HA'))].plot.ax,
    #                     g_disp.population_mean.attributes[('Comfort', ('CoSS', 'HA'))].plot.ax,
    #                     g_disp.random_individual.attributes[('Comfort', ('CoSS', 'HA'))].plot.ax
    #                     ])
    # -> matching y-axis limits: nice if plots are to be shown side by side

    # ------------------------------- save all result displays
    emd.save(result_path,
             figure_format='pdf',  # or any other format allowed by Matplotlib
             table_format='txt',  # or any other format allowed by Pandas
             float_format='%.2f',  # any other parameters for Pandas table-writer function
             )
    # (optionally) save in other format(s), too:
    # emd.save(result_path,
    #          table_format='csv',  # for input to other package
    #          float_format='%.4f',  # any other parameters for Pandas table-writer function
    #          # sep='\t'  # -> tab-delimited
    #          )

    logging.info(f'All result displays saved in {result_path}')

    logging.shutdown()
