# CSE 310 Programming Assignment 2
#### Taein Um
#### 1112348159


## External Libraries Used
- `socket`: For TCP connection handling.
- `dpkt`: For pcap libraries.


## Instructions on Running the Programs
1. Make sure the dpkt library is installed. If not, you can install dpkt using `pip install dpkt`
2. Prepare pcap file
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
