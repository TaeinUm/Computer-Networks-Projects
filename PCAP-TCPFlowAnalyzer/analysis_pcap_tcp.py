import dpkt
import socket


# Reads pcap file and returns packets with their timestamps
def read_pcap_file(file_path):
    with open(file_path, 'rb') as file:
        pcap = dpkt.pcap.Reader(file)
        packets = [(ts, pkt) for ts, pkt in pcap]
    return packets


# Filters out TCP packets from the pcap data
def filter_tcp_packets(packets):
    tcp_packets = []
    for ts, packet in packets:
        eth = dpkt.ethernet.Ethernet(packet)
        if isinstance(eth.data, dpkt.ip.IP) and isinstance(eth.data.data, dpkt.tcp.TCP):
            tcp_packets.append((ts, eth))
    return tcp_packets


# Estimates the cwnd sizes
def estimate_cwnd(tcp_packets):
    cwnd = 1460  # Initial cwnd is set to one MSS
    ssthresh = 65536  # Slow start threshold is set high initially
    acked_bytes = 0
    estimated_cwnds = [cwnd]  # Keeps track of estimated cwnd sizes
    last_ack = 0
    duplicate_acks = 0

    # Iterates through each TCP packet to adjust cwnd based on ACKs received
    for _, eth in tcp_packets:
        ip = eth.data
        tcp = ip.data

        # Increases cwnd based on new ACKs received
        if tcp.flags & dpkt.tcp.TH_ACK and tcp.ack > last_ack:
            ack_increment = tcp.ack - last_ack
            last_ack = tcp.ack
            acked_bytes += ack_increment

            # Adjusts cwnd size based on current phase (Slow Start or Congestion Avoidance)
            if cwnd < ssthresh:
                cwnd += ack_increment
                estimated_cwnds.append(cwnd)
            else:
                while acked_bytes >= cwnd:
                    acked_bytes -= cwnd
                    cwnd += 1460  # Increment cwnd by one MSS
                    estimated_cwnds.append(cwnd)

        # Detects triple duplicate ACKs and reduces cwnd and ssthresh
        elif tcp.ack == last_ack:
            duplicate_acks += 1
            if duplicate_acks == 3:
                ssthresh = max(cwnd // 2, 2 * 1460)  # Halves the cwnd
                cwnd = ssthresh
                estimated_cwnds.append(cwnd)

    return estimated_cwnds[:3]  # Returns the first three cwnd sizes


# Detects retransmissions within a TCP flow
def detect_retransmissions(tcp_flow_packets):
    sent_packets = {}  # Records when each sequence number was sent
    acks = {}  # Counts occurrences of each ACK number
    triple_duplicate_acks_detected = 0
    timeouts_detected = 0
    SOME_TIMEOUT_THRESHOLD = 1.0  # Example threshold for detecting timeouts

    for ts, eth in tcp_flow_packets:
        tcp = eth.data.data

        # Tracks when a sequence number is sent for the first time
        if tcp.seq not in sent_packets:
            sent_packets[tcp.seq] = ts

        # Counts ACKs for triple duplicate ACK detection
        if tcp.flags & dpkt.tcp.TH_ACK:
            acks[tcp.ack] = acks.get(tcp.ack, 0) + 1
            if acks[tcp.ack] == 3:
                triple_duplicate_acks_detected += 1

        # Detects timeouts based on the threshold
        if tcp.seq in sent_packets and ts - sent_packets[tcp.seq] > SOME_TIMEOUT_THRESHOLD:
            timeouts_detected += 1
            sent_packets[tcp.seq] = ts  # Updates the timestamp for potential retransmission

    return triple_duplicate_acks_detected, timeouts_detected


# Identify and analyze TCP flows within the pcap data
def identify_and_analyze_tcp_flows(tcp_packets):
    flows = {}  # Stores information about each TCP flow

    for ts, eth in tcp_packets:
        ip = eth.data
        tcp = ip.data
        flow_id = (socket.inet_ntoa(ip.src), tcp.sport, socket.inet_ntoa(ip.dst), tcp.dport)

        # Initializes or updates flow information
        if flow_id not in flows:
            flows[flow_id] = {
                'start_time': ts,
                'end_time': ts,
                'total_bytes': len(tcp.data),
                'packets_tcp': [(ts, tcp)],
                'packets_eth': [(ts, eth)],
                'sequence_numbers': {tcp.seq},
                'syn_seen': tcp.flags & dpkt.tcp.TH_SYN != 0,
                'fin_seen': False,
            }
        else:
            flow = flows[flow_id]
            flow['end_time'] = ts
            flow['total_bytes'] += len(tcp.data)
            flow['packets_tcp'].append((ts, tcp))
            flow['packets_eth'].append((ts, eth))
            flow['sequence_numbers'].add(tcp.seq)
            if tcp.flags & dpkt.tcp.TH_FIN:
                flow['fin_seen'] = True

    # Analyzes each flow for throughput, transactions, and cwnd size
    for flow_id, flow in flows.items():
        if flow['total_bytes'] > 0:
            duration = flow['end_time'] - flow['start_time']
            throughput = flow['total_bytes'] / duration if duration > 0 else 0
            print(f"TCP Flow: {flow_id}")
            print(f"\tDuration: {duration:.2f} seconds")
            print(f"\tTotal TCP Data Bytes: {flow['total_bytes']}")
            print(f"\tThroughput: {throughput:.2f} bytes/sec")
            transactions = [pkt for ts, pkt in flow['packets_tcp'] if len(pkt.data) > 0]
            if len(transactions) >= 2:
                first_tran = transactions[0]
                second_tran = transactions[1]
                print(f"\tFirst Transaction - Seq: {first_tran.seq}, Ack: {first_tran.ack}, Win: {first_tran.win}")
                print(f"\tSecond Transaction - Seq: {second_tran.seq}, Ack: {second_tran.ack}, Win: {second_tran.win}")
            triple_dup_acks, timeouts = detect_retransmissions(flow['packets_eth'])
            print(f"\tTriple Duplicate ACKs Detected: {triple_dup_acks}")
            print(f"\tTimeouts Detected: {timeouts}")
            estimated_cwnds = estimate_cwnd(flow['packets_eth'])
            print(f"\tEstimated cwnd Sizes (in bytes, first three significant changes): {estimated_cwnds}")
            print()


def main():
    pcap_file_path = "assignment2.pcap" # Adjust the path as needed
    packets = read_pcap_file(pcap_file_path)
    tcp_packets = filter_tcp_packets(packets)
    identify_and_analyze_tcp_flows(tcp_packets)


if __name__ == "__main__":
    main()
