# Business Insight Report
## Customer and Lead Exploratory Data Analysis

**Prepared by:** Rajendra Prasad V  
**Internship:** Cynaris – Data Analyst Intern, Project 1

### Objective
Explore customer segments, lead acquisition sources, geographic distribution and conversion outcomes to identify patterns that can support business follow-up and marketing decisions.

### Dataset and quality
The dataset contains 250 customer/lead records and 16 columns. It includes customer segment, city, preferred locality, budget range, lead source, inquiry activity, completed site visits, conversion status, signup date and recorded spend. Missing cells: 0. Duplicate customer IDs: 0.

### Five key findings
1. **Overall conversion:** 56 records are marked Closed Won, giving a closed-won rate of 22.4%.
2. **Segment differences:** Luxury Upgrader leads the segment comparison at 34.2%, while Channel Partner / Broker is lowest at 15.0%. The business could review the needs and follow-up journeys of lower-converting groups.
3. **Lead-source pattern:** Organic Search has the highest observed closed-won rate (25.5%). Review lead quality and cost per acquisition before shifting marketing budgets.
4. **Geographic concentration:** Bengaluru is the largest city group (205 records). Bengaluru contributes 205 of 250 records, so operational reporting should account for this concentration.
5. **Engagement and conversion:** Closed-Won records average 3.00 completed site visits; other statuses average 2.93. This suggests site-visit activity is worth monitoring, but the dataset alone cannot prove it causes conversion.

### Recommendations
- Compare lead quality, conversion and acquisition cost by source before changing channel spend.
- Create segment-specific follow-up plans, especially for segments with lower observed conversion.
- Track lead stage changes and time-to-conversion in future datasets.
- Collect marketing cost and transaction-level revenue to enable ROI and revenue analysis.

### Methodology
Pandas was used for loading, cleaning checks, date parsing, derived fields and group-by analysis. Matplotlib was used for bar charts and a box plot. Conversion was defined as `conversion_status == "Closed Won"`. Budget midpoint was calculated as the average of the minimum and maximum budget fields and is used only as an exploratory estimate.

### Limitations
This is a 250-record real-estate customer/lead dataset, not an e-commerce order dataset. Results are descriptive, not causal. Small geographic groups may have volatile rates. Recorded spend is not assumed to equal property sale value or company revenue.
