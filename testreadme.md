🔹 RAC Claim Data Processing – End-to-End Jobs
________________________________________
Job 1 – Data Preparation, QC & Send to RAC (Automatic – Wednesday 10 AM)
1.	Extract claim data from different source tables and SNAP-CMS external APIs.
2.	Normalize/map all fields into a canonical RAC claim structure.
3.	Run QC checks:
o	Required fields present .
o	Duplicate detection .
4.	If pass QC → insert into RAC_DATA with status = READY.
5.	If fail QC → insert into RAC_DATA with status = ERROR and store error details (rule, message, field).
6.	Pick all records in RAC_DATA with status = READY.
7.	Generate RAC upload payload (flat file / API JSON/XML) with unique batch ID.
8.	Transmit file securely via SFTP to RAC.
9.	Update submitted claims in RAC_DATA to status = SENT.
10.	Send all RAC_DATA with status = ERROR to Ops team for review/fix.
11.	Log every file generated and transmitted into RAC_FILE_TRANSFER .
________________________________________
Job 2 – Process RAC Acknowledgments (Automatic – OnDemand whenever we received ACK)
12.	Ingest RAC acknowledgment file(s) from SFTP.
13.	Write acknowledgment details into RAC_ACK table 
14.	Send acknowledgment details to Ops team with a daily summary (accepted, rejected, errors).
15.	Based on acknowledgment results:
1.	If program fix needed → IT/Dev team adjusts code.
2.	If data fix needed → Business team corrects data.
3.	If file layout/structural issue → Ops manually uploads corrected file (see Job 3).
16.	Once fixes are applied → claims can re-enter processing (automatic or manual).
________________________________________
Job 3 – Manual Process (On-Demand by Ops, Mainframe FTP Upload)
17.	When errors exist in RAC_DATA (status = ERROR) or in RAC_ACK (rejected claims), Ops may manually prepare corrected files.
18.	Place corrected file in Mainframe FTP location for transmission.
19.	Once transmitted → update impacted records in RAC_DATA with status = MANUALLY_SEND.
20.	File metadata still logged into RAC_FILE_TRANSFER for full audit trail.
________________________________________
Job 4 – Retry Error Data (Automatic – Friday 10 AM)
21.	Pick all error records from RAC_DATA (status = ERROR) and RAC_ACK (rejected).
22.	Re-run QC checks.
23.	If QC passes → prepare and transmit retry batch to RAC.
24.	Update records to status = RETRY_SENT.
25.	If errors remain → send details back to Ops team for fix.
26.	Log retry file details into RAC_FILE_TRANSFER.
________________________________________
🔹 Tables in Use
•	RAC_DATA → Central claim table with lifecycle statuses (READY, SENT, ERROR, MANUALLY_SEND, RETRY_SENT).
•	RAC_ACK → Stores acknowledgment feedback from RAC (accepted/rejected + errors).
•	RAC_FILE_TRANSFER → Audit trail of every file sent/received ________________________________________


🔹 Weekly Timeline
•	Wednesday 10 AM → Job 1 (Prep + QC + Send).
•	On-Demand (Anytime) → Job 2 (Ack ingestion).
•	On-Demand (Anytime) → Job 3 (Manual upload by Ops).
•	Friday 10 AM → Job 4 (Retry automation for error claims).
✅ This flow ensures:
•	Automation first (Wed + Fri jobs).
•	Ops visibility (error reports + manual upload fallback).
•	Audit trail (all files logged).
•	Continuous loop until all claims are accepted/finalized.


