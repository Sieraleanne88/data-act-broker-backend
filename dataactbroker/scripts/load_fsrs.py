import logging
import sys
import argparse
import datetime
import json

from dataactcore.interfaces.db import GlobalDB
from dataactcore.logging import configure_logging
from dataactbroker.fsrs import config_valid, fetch_and_replace_batch, GRANT, PROCUREMENT, config_state_mappings
from dataactvalidator.health_check import create_app

logger = logging.getLogger(__name__)


def log_fsrs_counts(total_awards):
    """ Count the subawards of the awards in this batch.

        Args:
            total_awards: the award objects from this batch of pulls
    """
    no_sub_awards = sum(len(a.subawards) for a in total_awards)
    logger.info("Inserted/Updated %s awards, %s subawards", len(total_awards), no_sub_awards)


def metric_counts(award_list, award_type, metrics):
    """ Adds to the given metric count

        Args:
            award_list: list of award objects that contain subawards
            award_type: procurement or grant for which key to add to
            metrics: the dictionary containing the metrics we need
    """
    metrics[award_type+'_awards'] += len(award_list)
    metrics[award_type+'_subawards'] += sum(len(a.subawards) for a in award_list)


if __name__ == '__main__':
    now = datetime.datetime.now()
    configure_logging()
    parser = argparse.ArgumentParser(description='Pull data from FSRS Feed')
    parser.add_argument('-p', '--procurement', action='store_true', help="Load just procurement awards")
    parser.add_argument('-g', '--grants', action='store_true', help="Load just grant awards")
    parser.add_argument('-i', '--ids', type=int, nargs='+',
                        help="Single or list of FSRS ids to pull from the FSRS API")

    with create_app().app_context():
        logger.info("Begin loading FSRS data from FSRS API")
        sess = GlobalDB.db().session
        args = parser.parse_args()

        metrics_json = {
            'script_name': 'load_fsrs.py',
            'start_time': str(now),
            'procurement_awards': 0,
            'procurement_subawards': 0,
            'grant_awards': 0,
            'grant_subawards': 0
        }

        # Setups state mapping for deriving state name
        config_state_mappings(sess, init=True)

        if not config_valid():
            logger.error("No config for broker/fsrs/[service]/wsdl")
            sys.exit(1)
        elif args.procurement and args.grants and args.ids:
            logger.error("Cannot run both procurement and grant loads when specifying FSRS ids")
        else:
            # Regular FSRS data load, starts where last load left off
            if len(sys.argv) <= 1:
                awards = ['Starting']
                while len(awards) > 0:
                    procs = fetch_and_replace_batch(sess, PROCUREMENT)
                    grants = fetch_and_replace_batch(sess, GRANT)
                    awards = procs + grants
                    log_fsrs_counts(awards)
                    metric_counts(procs, 'procurement', metrics_json)
                    metric_counts(grants, 'grant', metrics_json)

            elif args.procurement and args.ids:
                for procurement_id in args.ids:
                    logger.info('Begin loading FSRS reports for procurement id {}'.format(procurement_id))
                    procs = fetch_and_replace_batch(sess, PROCUREMENT, procurement_id)
                    log_fsrs_counts(procs)
                    metric_counts(procs, 'procurement', metrics_json)

            elif args.grants and args.ids:
                for grant_id in args.ids:
                    logger.info('Begin loading FSRS reports for grant id {}'.format(grant_id))
                    grants = fetch_and_replace_batch(sess, GRANT, grant_id)
                    log_fsrs_counts(grants)
                    metric_counts(grants, 'grant', metrics_json)
            else:
                if not args.ids:
                    logger.error('Missing --ids argument when loading just procurement or grants awards')
                else:
                    logger.error('Missing --procurement or --grants argument when loading specific award ids')

        # Deletes state mapping variable
        config_state_mappings()

        metrics_json['duration'] = str(datetime.datetime.now() - now)

        with open('load_fsrs_metrics.json', 'w+') as metrics_file:
            json.dump(metrics_json, metrics_file)
