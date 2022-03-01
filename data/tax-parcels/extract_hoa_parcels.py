#!/usr/bin/env python
# -*- coding: ascii -*-
###############################################################################
# Copyright 2017 Carl Sapp
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""
Wyndham Forest HOA Parcel Data Extraction Tool
==============================================

This module is used to extract Wyndham Forest HOA parcels out of the Henrico County parcel data
CSV file. The input to this script is Henrico County's tax parcel and CAMA data CSV file that can
be obtained from https://data-henrico.opendata.arcgis.com/datasets/tax-parcels-cama-data-2/explore.
"""

import argparse
import csv
import logging

# Set up our logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_console_log_handler = logging.StreamHandler()
logger.addHandler(_console_log_handler)

SUBDIVISION_CODES = [
    1379,  # Wyndham Forest
    1452,  # Chappell Ridge @ Wyndham Forst
    1484,  # Rivers Edge at Wyndham Forest
    1774,  # Holloway at Wyndham Forest
    1817,  # Holloway Townes @ Wynd Forest
]
ADDITIONAL_GPINS = [
    # These two parcels have their subdivision code (possibly incorrectly) set as 0
    '749-772-1022',  # HOLMAN RIDGE RD
    '749-771-2999',  # 9786 HOLMAN RIDGE RD
]
# If the user doesn't specify a data file on the command line, we'll attempt to download the file
# from Henrico County. I'm not sure if this URL changes with new data.
# Update December 2021 - The URL does change over time. So, this code won't work as is. Leaving the
# code here, but commented out, in case someone wants to improve this later.
# DATA_FILE_URL = 'https://opendata.arcgis.com/datasets/fcaf8452b69f4f89aa71d4ddc747694e_102.csv?outSR=%7B%22latestWkid%22%3A2284%2C%22wkid%22%3A102747%7D'

def main(args=None):
    # Parse our command line options
    cmd_line_parser = argparse.ArgumentParser(
        # Text to display before the argument help
        description='This tool is used to extract Wyndham Forest HOA parcels from the Henrico County parcel data file.',
        epilog='Send any questions/concerns to CarlSapp@gmail.com.'
    )
    cmd_line_parser.add_argument(
        dest='input_file',
        help='The Henrico County parcels CSV data file. Obtain the latest version from https://data-henrico.opendata.arcgis.com/datasets/tax-parcels-cama-data.'
            ' If no file is provided, we will attempt to download it from the Henrico County site.',
    )
    cmd_line_parser.add_argument(
        dest='output_file',
        help='The file name to write out to. Defaults to WyndhamForestParcels.csv.',
        default='WyndhamForestParcels.csv',
        nargs='?', # Argument is optional
    )
    cmd_line_args = cmd_line_parser.parse_args(args)
    if (cmd_line_args.input_file is None):
        # Update December 2021 - We don't have a static URL for the data file, so this code isn't
        # sustainable as is. Leaving it here, but commented out if someone wants to improve it
        # later.
        raise NotImplementedError('Unable to pull data automatically. You need to download the file manually.')
        # # Attempt to download the file from Henrico County
        # logger.info('No filename was specified on the command line. Reading data from {}.'.format(DATA_FILE_URL))
        # in_csv_file = codecs.iterdecode(urllib.request.urlopen(DATA_FILE_URL), 'utf-8')
    else:
        in_csv_file = open(cmd_line_args.input_file, newline='')
    rows_parsed = 0
    wyndham_forest_parcels_found = 0
    try:
        with open(cmd_line_args.output_file, 'w', newline='') as out_csv_file:
            reader = csv.DictReader(in_csv_file)
            writer = csv.DictWriter(out_csv_file, reader.fieldnames)
            writer.writeheader()
            for row in reader:
                rows_parsed += 1
                if ((row['SUBDIVISION_CODE'] != '' and int(row['SUBDIVISION_CODE'], base=10) in SUBDIVISION_CODES)
                        or row['GPIN'] in ADDITIONAL_GPINS):
                    wyndham_forest_parcels_found += 1
                    writer.writerow(row)
    except:
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # Always close the input file
        out_csv_file.close()
    logger.info('{} parcels analyzed. {} Wyndham Forest parcels found.'.format(
        rows_parsed,
        wyndham_forest_parcels_found
    ))
    logger.info('Data written to {}.'.format(cmd_line_args.output_file))
    

if __name__ == '__main__':
    main()
