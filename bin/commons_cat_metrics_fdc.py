"""
The following line computes metrics for files in "Media supported by Wikimedia France"
and for the FDC report of year 2012-2013 round 2 quarter 3

python commons_cat_metrics_fdc.py --year 2012-2013 --round 2 --quarter 3 --category "Media supported by Wikimedia France"

Please use python commons_cat_metrics_fdc.py -h for more information

"""
from argparse import ArgumentParser

from wm_metrics.commons_cat_metrics import CommonsCatMetrics
from wm_metrics.fdc.round import Round


def _parse_years(arg_years):
    return [int(y) for y in arg_years.split('-')]


def main():
    """Commons Cat Metrics."""
    parser = ArgumentParser(description="Commons Cat Metrics")

    parser.add_argument("-c", "--category",
                        type=str,
                        dest="category",
                        metavar="CAT",
                        required=True,
                        help="The Commons category without Category:")
    parser.add_argument("-y", "--year",
                        type=str,
                        dest="years",
                        metavar="YEAR",
                        required=True,
                        help="The FDC year, e.g 2011-2012")
    parser.add_argument("-r", "--round",
                        type=int,
                        dest="round",
                        metavar="ROUND",
                        required=True,
                        help="The FDC round, i.e. 1 or 2")
    parser.add_argument("-q", "--quarter",
                        type=int,
                        dest="quarter",
                        metavar="QUARTER",
                        required=True,
                        help="The reporting quarter")
    # FDC round
    args = parser.parse_args()
    category = args.category.decode('utf-8')
    years = _parse_years(args.years)

    fdc_round = Round(years[0], years[1], args.round)

    time_period = fdc_round.to_period_for_quarter(args.quarter)

    metrics = CommonsCatMetrics(category, time_period)
    text_report = metrics.make_report()
    metrics.close()
    print text_report


if __name__ == "__main__":
    main()
