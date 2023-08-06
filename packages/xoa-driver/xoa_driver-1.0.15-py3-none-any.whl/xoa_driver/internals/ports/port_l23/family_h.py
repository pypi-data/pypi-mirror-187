import functools
from typing import TYPE_CHECKING
from .bases.port_l23_genuine import BasePortL23Genuine
from xoa_driver.internals.core.commands import (
    P_FAULTSIGNALING,
    P_FAULTSTATUS,
    P_DYNAMIC,
)
from xoa_driver.internals.utils import attributes as utils
if TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf

from .pcs_pma_ghijkl import (
    PcsPma,
    SerDes,
)
class Fault:
    """L23 port fault settings."""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        self.signaling = P_FAULTSIGNALING(conn, module_id, port_id)
        """L23 port fault signaling.
        Representation of P_FAULTSIGNALING
        """
        
        self.status = P_FAULTSTATUS(conn, module_id, port_id)
        """L23 port fault status.
        Representation of P_FAULTSTATUS
        """
        
        self.pcs_pma = PcsPma(conn, self)
        """PCS/PMA settings."""

class FamilyH(BasePortL23Genuine):
    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        super().__init__(conn, module_id, port_id)
        self.dynamic = P_DYNAMIC(conn, module_id, port_id)
        """L23 port's dynamic traffic change.
        Representation of P_DYNAMIC
        """

    async def _setup(self):
        await super()._setup()
        self.ser_des = tuple(
            SerDes(self._conn, *self.kind, serdes_xindex=serdes_xindex)
            for serdes_xindex in range(self.info.capabilities.serdes_count)
        )
        return self

    on_fault_signaling_change = functools.partialmethod(utils.on_event, P_FAULTSIGNALING)
    """Register a callback to the event that the port's fault signalling changes."""
    
    on_dynamic_change = functools.partialmethod(utils.on_event, P_DYNAMIC)
    """Register a callback to the event that the port's dynamic traffic setting changes."""
    
class PLoki100G5S1P(FamilyH):
    """L23 port on Loki-100G-5S-1P module.
    """
    ...
