from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
import array

# sudo ryu-manager dnsryu.py ryu.app.ofctl_rest

# Inherits from ryu.base.app_manager
class TestSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TestSwitch, self).__init__(*args, **kwargs)

    # Hand shake handler? Called when switch first talks to controller
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        print("A switch was found")
        pass
        # # todo: add rule for DNS, packet-in handle DNS packets
        #
        # match = parser.OFPMatch(ipv4_dst=10.0.0.1, eth_type=0x0800, udp_dst=53, ip_proto=6);
        # actions = [parser.OFPActionOutput(,ofproto.OFPCML_NO_BUFFER)]
        # actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)]
        #
        # match = parse.OFPMatch(eth_type=0x0800, ip_proto=6, ipv4_dst=server_ip, tcp_src=tcp_pkt.src_port)
        #
        # self.add_flow(datapath, 10, match, actions)
        #
        # # Table miss entry
        # match = parser.OFPMatch()
        #
        # # Packet in controller
        # actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
        # ofproto.OFPCML_NO_BUFFER)]
        # self.add_flow(datapath, 0, match, actions)
        #
        # return

    def generateMatchDST(self, isTCP, portNum, ip_address, datapath, priority):
        if (isTCP):
            match = parser.OFPMatch(ipv4_dst=ip_address, eth_type=0x0800, tcp_dst=portNum, ip_proto=6);
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)] # Treat as normal
            self.add_flow(datapath, priority, match, actions)
        else:
            match = parser.OFPMatch(ipv4_dst=ip_address, eth_type=0x0800, udp_dst=portNum, ip_proto=6);
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)] # Treat as normal
            self.add_flow(datapath, priority, match, actions)


    def generateMatchSRC(self, isTCP, portNum, ip_address, datapath, priority):
        if (!isTCP):
            match = parser.OFPMatch(ipv4_src=ip_address, eth_type=0x0800, udp_src=portNum, ip_proto=6);
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)] # Treat as normal
            self.add_flow(datapath, priority, match, actions)
        else:
            match = parser.OFPMatch(ipv4_src=ip_address, eth_type=0x0800, tcp_src=portNum, ip_proto=6);
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)] # Treat as normal
            self.add_flow(datapath, priority, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        pass

        # Check if it is DNS

        # Get the address and ip mapping for DNS
        # Push flow rule

        #
        # msg = ev.msg
        # dp = msg.datapath
        # ofp = dp.ofproto
        # ofp_parser = dp.ofproto_parser
        #
        # actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        # out = ofp_parser.OFPPacketOut(
        #     datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,
        #     actions=actions)
        # dp.send_msg(out)
