# TCP Flow Analyzer
#### Taein Um



## Overview
This project, part of the CSE 310 coursework at Stony Brook University, involves developing a comprehensive TCP flow analyzer using PCAP files. The analyzer parses PCAP files to extract and characterize TCP flows, providing detailed insights into TCP connections, throughput, and congestion control mechanisms. The tool is instrumental for network diagnostics and performance analysis.



## Features
- **TCP Flow Identification**: Identifies and characterizes TCP flows based on the SYN and FIN packets, detailing each flow's lifecycle from initiation to termination.
- **Flow Details Extraction**: Extracts key details such as source and destination IPs, port numbers, and sequence numbers for the first two transactions after a connection is established.
- **Throughput Calculation**: Computes the sender throughput in bytes/sec, considering only the data packets excluding headers and ACKs.
- **Congestion Analysis**: Empirically estimates the congestion window sizes and provides insights into TCP congestion control behavior over time.
- **Retransmission Metrics**: Tracks retransmissions triggered by triple duplicate ACKs and timeouts to assess the reliability of the connection.



## Technologies Used
- **Language**: `Python`
- **Libraries**: 
    - `socket` for TCP connection handling.
    - `dpkt` for pcap libraries.
- **Tools**: Wireshark for verifying and comparing results



## Instructions on Running the Programs
1. Make sure the dpkt library is installed. If not, you can install dpkt using `pip install dpkt`
2. Prepare pcap file. The sample file is attached.
3. In the `main` function, adjust the file name and path as needed.
4. Run `python analysis_pcap_tcp.py`



## Summary Of The Program

### Part A
1. **Reading and Filtering**: The script starts by reading a pcap file and filtering out TCP packets.
2. **Flow Identification**: Packets are then grouped by their TCP flow identifiers (source IP, source port, destination IP, destination port), facilitating flow-level analysis.
3. **Throughput Calculation**: The script calculates the throughput for each TCP flow by dividing the total bytes by the flow duration, providing a measure of network performance.


### Part B
1. **Triple Duplicate ACKs**: By counting duplicate ACKs for the same sequence number, the script identifies potential packet loss events and infers fast retransmit actions.
2. **Timeout Detection**: The script estimates timeouts by monitoring the time elapsed since the last packet was sent without receiving an ACK, indicating possible network congestion or issues.
3. **CWND Estimation**: For each flow, the script estimates cwnd sizes by tracking ACK progression. It identifies new ACKs and their impact on the cwnd size, distinguishing between slow start and congestion avoidance phases.



## Contact Information
- Name: Taein Um
- Email: taeindev@gmail.com
- LinkedIn: https://www.linkedin.com/in/taein-um-00b14916b/

