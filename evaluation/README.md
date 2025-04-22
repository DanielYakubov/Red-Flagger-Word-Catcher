# Evaluation

Hosts the script to evaluate the abuse_flagger. For the results, see results.txt. The recall consistently scores higher than the precision. This is by design of the software as all positives are meant to be audited in some way when using any keyword detection for abuse detection.
The overall low scores on the Toxic Chat can be attributed to several reasons - 
1) Chat abuse can be more nuanced and harder to detect with keywords alone.
2) The keywords discovered are indicative of human abuse, and less of model abuse, but the dataset is annotated for abuse from both sources.
3) The authors themselves note the difficulty of the dataset.
![](../../../../../var/folders/zc/g0w96sh55bq1w03tz36mmk940000gn/T/TemporaryItems/NSIRD_screencaptureui_BFQZZf/Screenshot 2025-04-22 at 1.21.51 PM.png)