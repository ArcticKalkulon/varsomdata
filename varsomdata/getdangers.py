# -*- coding: utf-8 -*-
"""Contains methods for retrieving avalanche danger regardless source (regObs or forecastAPI or version/year
the data is from.)"""

import datetime as dt
from varsomdata import getobservations as go
from varsomdata import getforecastapi as gfa
from varsomdata import varsomclasses as vc
import setenvironment as env

__author__ = 'raek'


def _make_eval1_conform(evaluations_1):
    """Maps the AvalancheEvaluation to the conformity of a common AvalancheDanger object.

    :param evaluations_1:   [list of AvalancheEvaluation] These are the classes used on getobservations.py
    :return:                [list of AvalancheDanger]
    """

    dangers = []

    for e in evaluations_1:
        region_id = e.ForecastRegionTID
        region_name = e.ForecastRegionName
        data_table = 'AvalancheEvaluation'
        date = e.DtObsTime
        danger_level = e.AvalancheDangerTID
        danger_level_name = e.AvalancheDangerName

        danger = vc.AvalancheDanger(region_id, region_name, data_table, date, danger_level, danger_level_name)

        danger.set_avalanche_nowcast(e.AvalancheEvaluation)

        danger.set_regid(e.RegID)
        danger.set_source('Observation')
        danger.set_url('{0}{1}'.format(env.registration_basestring, e.RegID))
        danger.set_registration_time(e.DtRegTime)
        danger.set_municipal(e.MunicipalName)
        danger.set_nick(e.NickName)
        danger.set_competence_level(e.CompetenceLevelName)
        danger.add_metadata('Original data', e)

        dangers.append(danger)

    return dangers


def _make_eval2_conform(evaluations_2):
    """Maps the AvalancheEvaluation2 to the conformity of a common AvalancheDanger object.

    :param evaluations_2:   [list of AvalancheEvaluation2] These are the classes used on getobservations.py
    :return:                [list of AvalancheDanger]
    """

    dangers = []

    for e in evaluations_2:
        region_id = e.ForecastRegionTID
        region_name = e.ForecastRegionName
        data_table = 'AvalancheEvaluation2'
        date = e.DtObsTime
        danger_level = e.AvalancheDangerTID
        danger_level_name = e.AvalancheDangerName


        danger = vc.AvalancheDanger(region_id, region_name, data_table, date, danger_level, danger_level_name)

        danger.set_avalanche_nowcast(e.AvalancheEvaluation)
        danger.set_avalanche_forecast(e.AvalancheDevelopment)

        danger.set_regid(e.RegID)
        danger.set_source('Observation')
        danger.set_url('{0}{1}'.format(env.registration_basestring, e.RegID))
        danger.set_registration_time(e.DtRegTime)
        danger.set_municipal(e.MunicipalName)
        danger.set_nick(e.NickName)
        danger.set_competence_level(e.CompetenceLevelName)
        danger.add_metadata('Original data', e)

        dangers.append(danger)

    return dangers


def _make_eval3_conform(evaluations_3):
    """Maps the AvalancheEvaluation3 to the conformity of a common AvalancheDanger object.

    :param evaluations_3:   [list of AvalancheEvaluation3] These are the classes used on getobservations.py
    :return:                [list of AvalancheDanger]
    """

    dangers = []

    for e in evaluations_3:
        region_id = e.ForecastRegionTID
        region_name = e.ForecastRegionName
        data_table = 'AvalancheEvaluation3'
        date = e.DtObsTime
        danger_level = e.AvalancheDangerTID
        danger_level_name = e.AvalancheDangerName

        danger = vc.AvalancheDanger(region_id, region_name, data_table, date, danger_level, danger_level_name)

        danger.set_avalanche_nowcast(e.AvalancheEvaluation)
        danger.set_avalanche_forecast(e.AvalancheDevelopment)
        danger.set_forecast_correct(e.ForecastCorrectName, e.ForecastCorrectTID)
        danger.set_forecast_comment(e.ForecastComment)

        danger.set_regid(e.RegID)
        danger.set_source('Observation')
        danger.set_url('{0}{1}'.format(env.registration_basestring, e.RegID))
        danger.set_registration_time(e.DtRegTime)
        danger.set_municipal(e.MunicipalName)
        danger.set_nick(e.NickName)
        danger.set_competence_level(e.CompetenceLevelName)
        danger.add_metadata('Original data', e)

        dangers.append(danger)

    return dangers


def get_observed_dangers(region_ids, from_date, to_date, lang_key=1):
    """Gets observed avalanche dangers from AvalancheEvaluationV, AvalancheEvaluation2V and AvalancheEvaluation3V.

    :param region_ids:          [int or list of ints] ForecastRegionTID
    :param from_date:           [date or string as "YYYY-MM-DD"]
    :param to_date:             [date or string as "YYYY-MM-DD"]

    :return:
    """

    evaluations_1 = go.get_avalanche_evaluation(region_ids=region_ids, from_date=from_date, to_date=to_date, lang_key=lang_key)
    evaluations_2 = go.get_avalanche_evaluation_2(region_ids=region_ids, from_date=from_date, to_date=to_date, lang_key=lang_key)
    evaluations_3 = go.get_avalanche_evaluation_3(region_ids=region_ids, from_date=from_date, to_date=to_date, lang_key=lang_key)

    conform_evals_1 = _make_eval1_conform(evaluations_1)
    conform_evals_2 = _make_eval2_conform(evaluations_2)
    conform_evals_3 = _make_eval3_conform(evaluations_3)

    evaluations = conform_evals_1 + conform_evals_2 + conform_evals_3

    # sort list by date
    evaluations = sorted(evaluations, key=lambda AvalancheEvaluation: AvalancheEvaluation.date)

    return evaluations


def get_forecasted_dangers(region_ids, from_date, to_date, include_ikke_vurdert=False, lang_key=1):
    """Gets forecasted dangers for multiple regions.

    :param region_id:               [int] only one region. ID as given in regObs
    :param from_date:               [date or string as yyyy-mm-dd] gets dates [from, to>
    :param to_date:                 [date or string as yyyy-mm-dd] gets dates [from, to>
    :param include_ikke_vurdert:    [bool] if true, it includes forecasts where danger_level = 0

    :return:
    """

    # get all warning and problems for this region and then loop though them joining them where dates match.
    region_warnings = gfa.get_avalanche_warnings(region_ids, from_date, to_date, lang_key=lang_key)

    if not include_ikke_vurdert:
        all_non_zero_warnings = []

        for w in region_warnings:
            if w.danger_level != 0:
                all_non_zero_warnings.append(w)

        region_warnings = all_non_zero_warnings

    return region_warnings


def get_all_dangers(region_ids, from_date, to_date, lang_key=1):
    """Method does NOT include avalanche problems. Gets all avalanche dangers dangers, both forecasted and
    observed in given regions for a given time period.

    :param region_ids:          [int or list of ints]
    :param from_date:           [date or string as "YYYY-MM-DD"]
    :param to_date:             [date or string as "YYYY-MM-DD"]

    :return:
    """

    warnings = get_forecasted_dangers(region_ids, from_date, to_date, lang_key=lang_key)
    observed = get_observed_dangers(region_ids, from_date, to_date, lang_key=lang_key)

    all_dangers = warnings + observed

    # Sort by date
    all_dangers = sorted(all_dangers, key=lambda AvalancheDanger: AvalancheDanger.date)

    return all_dangers


if __name__ == "__main__":

    region_ids = [3010, 3011]   # Lyngen, Tromsø

    from_date = dt.date(2018, 1, 1)
    to_date = dt.date(2018, 1, 20)

    observed_dangers = get_observed_dangers(region_ids, from_date, to_date)
    forecasted_dangers = get_forecasted_dangers(region_ids, from_date, to_date)

    all = get_all_dangers(region_ids, from_date, to_date)

