from pathlib import Path
from qualys_etl.etld_lib import etld_lib_config as etld_lib_config
from qualys_etl.etld_lib import etld_lib_credentials as etld_lib_credentials
from qualys_etl.etld_lib import etld_lib_functions as etld_lib_functions
from qualys_etl.etld_lib import etld_lib_distribution as api_dist


def asset_inventory_dist():
    try:
        file_paths = (
            etld_lib_config.asset_inventory_sqlite_file,
            etld_lib_config.asset_inventory_csv_file,
        )
        api_dist.copy_results_to_external_target(file_paths, etld_lib_config.asset_inventory_export_dir)
    except Exception as e:
        etld_lib_functions.logger.error(f"Program aborted, ensure etld_lib_config_settings.yaml distribution "
                                        f"directory exists or is set to default: Exception: {e}")
        exit(1)


def start_msg_asset_inventory_dist():
    etld_lib_functions.logger.info(f"start")


def end_msg_asset_inventory_dist():
    etld_lib_functions.logger.info(f"end")


def main():
    start_msg_asset_inventory_dist()
    asset_inventory_dist()
    end_msg_asset_inventory_dist()


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='asset_inventory_distribution')
    etld_lib_config.main()
    etld_lib_credentials.main()
    main()
