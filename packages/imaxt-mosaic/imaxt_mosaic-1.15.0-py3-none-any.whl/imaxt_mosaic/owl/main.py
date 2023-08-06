import importlib
from pathlib import Path
from typing import List

import imaxt_mosaic.plugins
from distributed import WorkerPlugin, get_client
from imaxt_mosaic.settings import Settings
from owl_dev import pipeline
from owl_dev.logging import logger

from ..utils import cleanup, initialize, update_config


class SettingsPlugin(WorkerPlugin):
    def __init__(self, stitcher, config):
        self.stitcher = stitcher
        self.config = config

    def setup(self, worker):

        func = imaxt_mosaic.plugins.get_plugin(self.stitcher)
        mod = importlib.import_module(func.__module__)
        this = mod.__config.copy()
        this.update(self.config)
        Settings.set_config(this)


@pipeline
def main(  # noqa: C901
    *,
    input_path: Path,
    output_path: Path,
    recipes: List[str],
    stitcher: str,
    overwrite: bool,
    config: dict,
):
    """
    Main entry point for the pipeline.
    """
    logger.info("Starting pipeline")

    client = get_client()
    client.register_worker_plugin(SettingsPlugin(stitcher, config))
    update_config(stitcher, config)
    logger.info("Using settings %s", Settings.__repr__())

    initialize(output_path)

    try:
        if "raw2zarr" in recipes:
            if stitcher == "stpt":
                from stpt2zarr import stpt2zarr as raw2zarr
            elif stitcher == "axio":
                from axio2zarr import axio2zarr as raw2zarr

            raw2zarr(
                input_path, output_path / "raw", local_cluster=False, append_name=False
            )

        input_path = output_path / "raw"

        if overwrite:
            if not (output_path / "OVERWRITE").exists():
                logger.warn("Setting overwrite to false")
                overwrite = False

        if "calibration" in recipes:
            logger.info("Running calibration recipe")
            from ..calibration import compute_calibrations

            compute_calibrations(input_path, output_path, overwrite)

        if "mosaic" in recipes:
            logger.info("Running mosaic recipe")
            from ..stitchlib import imaxt_stitch

            imaxt_stitch(input_path, output_path, stitcher, overwrite)

        if "mosaic_preview" in recipes:
            logger.info("Running mosaic preview recipe")
            from ..tileset import create_tileset

            create_tileset(output_path, "tileset")

        if "bead_detect" in recipes:
            logger.info("Running bead_detection recipe")
            from ..bead_detect.runner import bead_detect

            bead_detect(output_path, overwrite=overwrite, fig=False)

        if "bead_detect_alt" in recipes:
            logger.info("Running bead_detection recipe")
            from ..beadlib import beads

            beads(output_path, overwrite=overwrite)

    finally:
        cleanup(output_path)

    logger.info("Finished pipeline")
