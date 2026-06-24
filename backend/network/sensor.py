import socket
import struct
from typing import Dict, Any, Optional, List
from datetime import datetime
from collections import defaultdict
import threading
import time


class PacketNormalizer:
    """Normalize and standardize packet data."""
    
    @staticmethod
    def normalize_packet(packet_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize packet to standard format."""
        return {
            "timestamp": packet_dict.get("timestamp", datetime.utcnow().isoformat()),
            "source_ip": PacketNormalizer._normalize_ip(packet_dict.get("src", "")),
            "destination_ip": PacketNormalizer._normalize_ip(packet_dict.get("dst", "")),
            "source_port": packet_dict.get("sport", 0),
            "destination_port": packet_dict.get("dport", 0),
            "protocol": PacketNormalizer._normalize_protocol(packet_dict.get("protocol", "TCP")),
            "size": packet_dict.get("size", 0),
            "flags": packet_dict.get("flags", 0),
            "ttl": packet_dict.get("ttl", 64),
            "payload": packet_dict.get("payload", ""),
            "flow_id": PacketNormalizer._generate_flow_id(
                packet_dict.get("src", ""),
                packet_dict.get("dst", ""),
                packet_dict.get("sport", 0),
                packet_dict.get("dport", 0),
                packet_dict.get("protocol", "TCP"),
            ),
        }

    @staticmethod
    def _normalize_ip(ip: str) -> str:
        """Normalize IP address."""
        try:
            socket.inet_aton(ip)
            return ip
        except:
            return "0.0.0.0"

    @staticmethod
    def _normalize_protocol(protocol: str) -> str:
        """Normalize protocol name."""
        protocol_map = {
            "6": "TCP",
            "17": "UDP",
            "1": "ICMP",
            "TCP": "TCP",
            "UDP": "UDP",
            "ICMP": "ICMP",
            "HTTP": "HTTP",
            "HTTPS": "HTTPS",
            "DNS": "DNS",
            "SSH": "SSH",
            "FTP": "FTP",
            "SMTP": "SMTP",
        }
        return protocol_map.get(str(protocol).upper(), "OTHER")

    @staticmethod
    def _generate_flow_id(src_ip: str, dst_ip: str, src_port: int, dst_port: int, protocol: str) -> str:
        """Generate unique flow identifier."""
        ips = tuple(sorted([src_ip, dst_ip]))
        ports = tuple(sorted([src_port, dst_port]))
        return f"{ips[0]}_{ips[1]}_{ports[0]}_{ports[1]}_{protocol}"


class FlowAggregator:
    """Aggregate packets into flows."""
    
    def __init__(self, timeout: int = 300):
        self.flows = defaultdict(lambda: {
            "start_time": None,
            "end_time": None,
            "packets": [],
            "bytes_sent": 0,
            "bytes_received": 0,
            "packet_count": 0,
        })
        self.timeout = timeout
        self.lock = threading.Lock()

    def add_packet(self, packet: Dict[str, Any]) -> None:
        """Add normalized packet to flow."""
        flow_id = packet.get("flow_id")
        if not flow_id:
            return
        
        with self.lock:
            flow = self.flows[flow_id]
            
            if not flow["start_time"]:
                flow["start_time"] = packet.get("timestamp")
            
            flow["end_time"] = packet.get("timestamp")
            flow["packets"].append(packet)
            flow["packet_count"] += 1
            flow["bytes_sent"] += packet.get("size", 0)
            flow["packet_count"] += 1

    def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get flow data."""
        with self.lock:
            return self.flows.get(flow_id)

    def get_active_flows(self) -> List[Dict[str, Any]]:
        """Get all active flows."""
        with self.lock:
            return list(self.flows.values())

    def cleanup_old_flows(self) -> None:
        """Remove expired flows."""
        current_time = time.time()
        with self.lock:
            expired_flows = [
                flow_id for flow_id, flow in self.flows.items()
                if flow["end_time"] and (current_time - float(flow["end_time"])) > self.timeout
            ]
            for flow_id in expired_flows:
                del self.flows[flow_id]

    def finalize_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Finalize and return flow data."""
        with self.lock:
            if flow_id not in self.flows:
                return None
            
            flow = self.flows[flow_id]
            packet = flow["packets"][0] if flow["packets"] else {}
            
            # Calculate duration
            start = flow["start_time"]
            end = flow["end_time"]
            duration = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() if start and end else 0
            
            finalized = {
                "source_ip": packet.get("source_ip", ""),
                "destination_ip": packet.get("destination_ip", ""),
                "source_port": packet.get("source_port", 0),
                "destination_port": packet.get("destination_port", 0),
                "protocol": packet.get("protocol", "TCP"),
                "packet_count": flow["packet_count"],
                "bytes_sent": flow["bytes_sent"],
                "bytes_received": flow["bytes_received"],
                "duration": duration,
                "start_time": flow["start_time"],
                "end_time": flow["end_time"],
            }
            
            del self.flows[flow_id]
            return finalized


class NetworkSensor:
    """Network packet capture and processing sensor."""
    
    def __init__(self):
        self.packet_normalizer = PacketNormalizer()
        self.flow_aggregator = FlowAggregator(timeout=300)
        self.packet_buffer = []
        self.flow_buffer = []
        self.lock = threading.Lock()
        self.is_capturing = False

    def process_raw_packet(self, packet_data: Dict[str, Any]) -> None:
        """Process raw packet data."""
        # Normalize packet
        normalized = self.packet_normalizer.normalize_packet(packet_data)
        
        with self.lock:
            self.packet_buffer.append(normalized)
        
        # Add to flow aggregator
        self.flow_aggregator.add_packet(normalized)

    def get_buffered_packets(self, max_count: int = 1000) -> List[Dict[str, Any]]:
        """Get and clear packet buffer."""
        with self.lock:
            packets = self.packet_buffer[:max_count]
            self.packet_buffer = self.packet_buffer[max_count:]
            return packets

    def finalize_and_get_flows(self) -> List[Dict[str, Any]]:
        """Get finalized flows."""
        self.flow_aggregator.cleanup_old_flows()
        flows = self.flow_aggregator.get_active_flows()
        
        finalized = []
        for flow in flows:
            if flow["packet_count"] >= 5:  # Only finalize flows with at least 5 packets
                finalized.append(flow)
        
        return finalized

    def get_sensor_stats(self) -> Dict[str, Any]:
        """Get sensor statistics."""
        with self.lock:
            packet_count = len(self.packet_buffer)
        
        return {
            "packets_buffered": packet_count,
            "active_flows": len(self.flow_aggregator.get_active_flows()),
            "is_capturing": self.is_capturing,
            "timestamp": datetime.utcnow().isoformat(),
        }


class PacketCapture:
    """Mock packet capture (can integrate with Scapy)."""
    
    @staticmethod
    def capture_packets(interface: str = None, packet_count: int = 100) -> List[Dict[str, Any]]:
        """
        Capture packets from network interface.
        In production, integrate with Scapy:
        from scapy.all import sniff, IP, TCP, UDP
        """
        packets = []
        # This is a placeholder for Scapy integration
        # In production:
        # def packet_callback(packet):
        #     if IP in packet:
        #         packets.append({...})
        # sniff(iface=interface, prn=packet_callback, count=packet_count)
        return packets
