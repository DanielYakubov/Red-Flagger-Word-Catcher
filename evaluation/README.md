# Evaluation

Hosts the script to evaluate the abuse_flagger. For the results, see results.txt. The recall consistently scores higher than the precision. This is by design of the software as all positives are meant to be audited in some way when using any keyword detection for abuse detection.
The overall low scores on the Toxic Chat can be attributed to several reasons - 
1) Chat abuse can be more nuanced and harder to detect with keywords alone.
2) The keywords discovered are indicative of human abuse, and less of model abuse, but the dataset is annotated for abuse from both sources.
3) The authors themselves show the difficulty of the dataset (note the low results of OpenAI's moderation):
![eval](https://github.com/user-attachments/assets/c360a426-3782-46cd-83b5-d4f26a9c1e70)
