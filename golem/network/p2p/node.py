import jsonobject
import logging
from typing import Optional

from golem.core.hostaddress import get_host_address, get_external_address, get_host_addresses

logger = logging.getLogger(__name__)


class Node(jsonobject.JsonObject):

    node_name = jsonobject.StringProperty()
    key = jsonobject.StringProperty()

    # task server ports
    prv_port = jsonobject.IntegerProperty()
    pub_port = jsonobject.IntegerProperty()
    # p2p server ports
    p2p_prv_port = jsonobject.IntegerProperty()
    p2p_pub_port = jsonobject.IntegerProperty()
    # addresses

    prv_addr = jsonobject.StringProperty()
    pub_addr = jsonobject.StringProperty()
    prv_addresses = jsonobject.ListProperty()

    nat_type = jsonobject.StringProperty()
    port_status = jsonobject.StringProperty()

    def collect_network_info(self, seed_host=None, use_ipv6=False):
        if not self.pub_addr:
            if self.prv_port:
                self.pub_addr, self.pub_port, self.nat_type = get_external_address(self.prv_port)
            else:
                self.pub_addr, _, self.nat_type = get_external_address()

        self.prv_addresses = get_host_addresses(use_ipv6)

        if not self.prv_addr:
            if self.pub_addr in self.prv_addresses:
                self.prv_addr = self.pub_addr
            else:
                self.prv_addr = get_host_address(seed_host, use_ipv6)

        if self.prv_addr not in self.prv_addresses:
            logger.warn("Specified node address {} is not among detected "
                        "network addresses: {}".format(self.prv_addr,
                                                       self.prv_addresses))

    def is_super_node(self):
        if self.pub_addr is None or self.prv_addr is None:
            return False
        return self.pub_addr == self.prv_addr

    def __str__(self):
        return "Node {}, (key: {})".format(self.node_name, self.key)
