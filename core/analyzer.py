import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger("Analyzer")


class PacketAnalyzer:
    """Extract summary and detailed information from packets."""

    @staticmethod
    def summarize(packet: Any) -> Dict[str, str]:
        """Return basic info for table display."""
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        info = {
            "timestamp": ts,
            "src": "",
            "dst": "",
            "protocol": getattr(packet, "highest_layer", "N/A"),
            "info": ""
        }
        try:
            ip = getattr(packet, "ip", None)
            if ip:
                info["src"] = ip.src
                info["dst"] = ip.dst

            if hasattr(packet, "tcp"):
                tcp = packet.tcp
                info["protocol"] = "TCP"
                info["info"] = f"{tcp.srcport}→{tcp.dstport}"
            elif hasattr(packet, "udp"):
                udp = packet.udp
                info["protocol"] = "UDP"
                info["info"] = f"{udp.srcport}→{udp.dstport}"
            elif hasattr(packet, "icmp"):
                icmp = packet.icmp
                info["protocol"] = "ICMP"
                info["info"] = f"Type {icmp.type}"
            elif hasattr(packet, "arp"):
                arp = packet.arp
                info["protocol"] = "ARP"
                info["info"] = f"Who has {arp.dst_proto_ipv4}?"
        except Exception as e:
            logger.error("Summarize error: %s", e)

        return info

    @staticmethod
    def details(packet: Any) -> str:
        """Return multiline, layer-by-layer details and raw data preview."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lines = [
            f"=== PACKET DETAILS ({ts}) ===",
            f"Highest Layer: {getattr(packet, 'highest_layer', 'N/A')}",
            f"Length: {getattr(packet, 'length', 'N/A')} bytes",
            ""
        ]

        try:
            eth = getattr(packet, "eth", None)
            if eth:
                lines += [
                    "--- Ethernet Layer ---",
                    f"Source MAC: {eth.src}",
                    f"Destination MAC: {eth.dst}",
                    ""
                ]

            ip = getattr(packet, "ip", None)
            if ip:
                lines += [
                    "--- IP Layer ---",
                    f"Version: {ip.version}",
                    f"Source IP: {ip.src}",
                    f"Destination IP: {ip.dst}",
                    ""
                ]

            tcp = getattr(packet, "tcp", None)
            if tcp:
                lines += [
                    "--- TCP Layer ---",
                    f"Source Port: {tcp.srcport}",
                    f"Destination Port: {tcp.dstport}",
                    f"Flags: {tcp.flags}",
                    ""
                ]

            udp = getattr(packet, "udp", None)
            if udp:
                lines += [
                    "--- UDP Layer ---",
                    f"Source Port: {udp.srcport}",
                    f"Destination Port: {udp.dstport}",
                    ""
                ]

            icmp = getattr(packet, "icmp", None)
            if icmp:
                lines += [
                    "--- ICMP Layer ---",
                    f"Type: {icmp.type}",
                    f"Code: {icmp.code}",
                    ""
                ]

            arp = getattr(packet, "arp", None)
            if arp:
                lines += [
                    "--- ARP Layer ---",
                    f"Src IP: {arp.src_proto_ipv4}",
                    f"Dst IP: {arp.dst_proto_ipv4}",
                    ""
                ]

            # Raw data preview
            raw = str(packet)
            lines += ["--- Raw Data ---", raw[:500]]

        except Exception as e:
            logger.error("Details error: %s", e)
            return f"Error generating details: {e}"

        return "\n".join(lines)