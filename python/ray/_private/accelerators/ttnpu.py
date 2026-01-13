import glob
import logging
import os
from typing import List, Optional, Tuple

from ray._private.accelerators.accelerator import AcceleratorManager

logger = logging.getLogger(__name__)

TENSTORRENT_VISIBLE_DEVICES_ENV_VAR = "TT_VISIBLE_DEVICES"


class TTNPUAcceleratorManager(AcceleratorManager):
    """Tenstorrent NPU accelerators."""

    @staticmethod
    def get_resource_name() -> str:
        return "TTNPU"

    @staticmethod
    def get_visible_accelerator_ids_env_var() -> str:
        return TENSTORRENT_VISIBLE_DEVICES_ENV_VAR

    @staticmethod
    def get_current_process_visible_accelerator_ids() -> Optional[List[str]]:
        tenstorrent_visible_devices = os.environ.get(
            TTNPUAcceleratorManager.get_visible_accelerator_ids_env_var(), None
        )

        if tenstorrent_visible_devices is None:
            return None

        if tenstorrent_visible_devices == "":
            return []

        if tenstorrent_visible_devices == "NoDevFiles":
            return []

        return list(tenstorrent_visible_devices.split(","))

    @staticmethod
    def get_current_node_num_accelerators() -> int:
        """Attempt to detect the number of NPUs on this machine.

        NPU chips are represented as devices within `/dev/`, either as `/dev/davinci?`.

        Returns:
            The number of NPUs if any were detected, otherwise 0.
        """

        try:
            npu_files = glob.glob("/dev/tenstorrent/*")
            return len(npu_files)
        except Exception as e:
            logger.debug("Failed to detect number of NPUs: %s", e)
        return 0

    @staticmethod
    def validate_resource_request_quantity(
        quantity: float,
    ) -> Tuple[bool, Optional[str]]:
        return (True, None)


    @staticmethod
    def set_current_process_visible_accelerator_ids(
        visible_npu_devices: List[str],
    ) -> None:
        os.environ[
            TTNPUAcceleratorManager.get_visible_accelerator_ids_env_var()
        ] = ",".join([str(i) for i in visible_npu_devices])
