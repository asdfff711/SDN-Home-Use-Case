from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
import array
from ryu.lib import dpid
from ryu.lib import hub

UDP = False
TCP = True

# sudo ryu-manager dns_compiling.py ryu.app.ofctl_rest --ofp-tcp-listen-port 55555 --verbose

# LOOK AT, traffic monitor code example, maybe able to learn how to grab stats from there
# https://osrg.github.io/ryu-book/en/html/traffic_monitor.html

# Inherits from ryu.base.app_manager
class TestSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    dp = None

    def __init__(self, *args, **kwargs):
        super(TestSwitch, self).__init__(*args, **kwargs)
        self.monitor_thread = hubspawn

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match = match, instructions = inst)
        datapath.send_msg(mod)

    # Hand shake handler? Called when switch first talks to controller
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Set Datapath of the switch
        dp = datapath

        dpid_ = dpid.dpid_to_str(datapath.id)
        print("Switch found with dipid" + dpid_)
        print(datapath)

        self.generateMatchDST(False, 53, "1.0.0.1", datapath, 10)
        self.generateMatchSRC(False, 53, "1.0.0.1", datapath, 10)

        # Add some dns entries

        # table miss entry
        # match = parser.OFPMatch()
        # actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
        #                                   ofproto.OFPCML_NO_BUFFER)]
        # self.add_flow(datapath, 0, match, actions)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt = packet.Packet(array.array('B', ev.msg.data))

        switchDPID = datapath.id
        dpid_ = dpid.dpid_to_str(datapath.id)
        # print('{} is receiving packets' .format(dpid))

        # print(pkt)

    # upload/send
    def generateMatchDST(self, isTCP, portNum, ip_address, datapath, priority):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        if isTCP:
            match = ofp_parser.OFPMatch(ipv4_src=ip_address, eth_type=0x0800, tcp_dst=portNum, ip_proto=6)
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)]  # Treat as normal
            self.add_flow(datapath, priority, match, actions)
        else:
            match = ofp_parser.OFPMatch(ipv4_src=ip_address, eth_type=0x0800, udp_dst=portNum, ip_proto=17)
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)]  # Treat as normal
            self.add_flow(datapath, priority, match, actions)

    # download/receive
    def generateMatchSRC(self, isTCP, portNum, ip_address, datapath, priority):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        self.logger.info("Pushing flow entry")
        print("Pushing flow entry")
        if isTCP:
            match = ofp_parser.OFPMatch(ipv4_dst=ip_address, eth_type=0x0800, tcp_src=portNum, ip_proto=6)
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)]  # Treat as normal
            self.add_flow(datapath, priority, match, actions)
        else:
            match = ofp_parser.OFPMatch(ipv4_dst=ip_address, eth_type=0x0800, udp_src=portNum, ip_proto=17)
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 0)]  # Treat as normal
            self.add_flow(datapath, priority, match, actions)

    def flow_request(self):
        """Requests flows in a separate thread"""
        datapath = dp
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        while True:
            match = parser.OFPMatchs(ipv4_dst=ip_address, eth_type=0x0800, udp_dst=53, ip_proto=17)
            # Not sure about this?
            stats = parser.OFPFlowStatsRequest(dp, 0, ofp.OFPP_ALL, ofp.OFPP_ANY, 0, 0, match)
            datapath.send_msg(stats)

            # Sleep the thread

    # Handles the reply from switch with information about a flow entry
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _stats_reply_handler(self, ev):
        self.logger.info("Inside the Stats Reply Handler")
        self.logger.info("Print out dns request info")
        for stats in ev.msg.body:
            actions = ofctl_v1_3.actions_to_str(stats.actions)
            match = ofctl_v1_4.match_to_str(stat.match)
            print {'dpid': ev.msg.datapath.id,
                   'priority': stats.priority,
                   'cookie': stats.cookie,
                   'idle_timeout': stats.idle_timeout,
                   'hard_timeout': stats.hard_timeout,
                   'actions': actions,
                   'match': match,
                   'byte_count': stats.byte_count,
                   'duration_sec': stats.duration_sec,
                   'duration_nsec': stats.duration_nsec,
                   'packet_count': stats.packet_count,
                   'table_id': stats.table_id}