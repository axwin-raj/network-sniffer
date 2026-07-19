class PacketAnalyzer:
    @staticmethod
    def summarize(pkt):
        try:
            if hasattr(pkt, 'ip'):
                src = pkt.ip.src
                dst = pkt.ip.dst
                proto = pkt.transport_layer or "TCP"
            elif hasattr(pkt, 'ipv6'):
                src = pkt.ipv6.src
                dst = pkt.ipv6.dst
                proto = pkt.transport_layer or "TCP"
            else:
                return {}

            return {
                "src": src,
                "dst": dst,
                "protocol": proto
            }

        except AttributeError:
            return {}