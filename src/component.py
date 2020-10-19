import logging
import os
import sys
import datetime
from pathlib import Path

from kbc.env_handler import KBCEnvHandler

# #### Keep for debug
KEY_DEBUG = 'debug'

MANDATORY_PARS = []
MANDATORY_IMAGE_PARS = []


class Component(KBCEnvHandler):

    def __init__(self, debug=False):
        # for easier local project setup
        default_data_dir = Path(__file__).resolve().parent.parent.joinpath('data').as_posix() \
            if not os.environ.get('KBC_DATADIR') else None

        KBCEnvHandler.__init__(
            self,
            MANDATORY_PARS,
            log_level=logging.DEBUG if debug else logging.INFO,
            data_path=default_data_dir
        )

        # override debug from config
        if self.cfg_params.get(KEY_DEBUG):
            logging.getLogger().setLevel(logging.DEBUG)

        logging.info('Loading configuration...')

        try:
            self.validate_config(MANDATORY_PARS)
            self.validate_image_parameters(MANDATORY_IMAGE_PARS)
        except ValueError as e:
            logging.exception(e)
            exit(1)

    def run(self):

        # get config params
        params = self.cfg_params
        logging.info(f"params: {params}")

        # get input table path
        input_table_defs = self.get_input_tables_definitions()
        first_table = input_table_defs[0]
        source_file_path = first_table.full_path
        logging.info(f"Source file path: {source_file_path}")

        # get output table path
        result_file_path = os.path.join(self.tables_out_path, "output.csv")
        logging.info(f"Result file path: {result_file_path}")

        self.configuration.write_table_manifest(
            file_name=result_file_path,
            primary_key=["row_number"],
            incremental=True,
        )

        # get state file and print last update
        state = self.get_state_file()
        logging.info(f"Last update: {state.get('last_update')}")

        # store new state
        now = datetime.datetime.now()
        self.write_state_file({"last_update": now.strftime("%d/%m/%Y %H:%M:%S")})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_arg = sys.argv[1]
    else:
        debug_arg = False
    try:
        comp = Component(debug_arg)
        comp.run()
    except Exception as exc:
        logging.exception(exc)
        exit(1)
