# schedule-risk-analysis
SRA Python Code (previous work project)
I wrote the sra.py code, a path-organizing linker.py code, and a visualization supporting_Dist.py code for a SRA project I did in a former job. The goal was to get a statistically sound estimate of a contractors schedule flow that was at high risk of falling behind. It uses standard SRA Monte Carlo methods like the tri-point estimate, and a rectangular beta distribution to determine how likely a schedule is to slip.

I wrote several versions over a few months, and adding more complicated sample schedules that include forks, numerous paths, and adding deeper critical path analysis and overall schedule task importance to a schedule.

SRA.py is the main code, which handles file i/o and the math
Linker.py is the code I wrote to determine all possible unique paths through a schedule. This was difficult for me since I only had base python and no access to the open internet. It took some wacky if statements and while loops that seemed to stretch my working memory pretty hard
Mock schedule data is stored in the attached Excel sheet, with real life data following the same spreadsheet format

This code gave me an accurate estimate of project completion date that I felt I was able to throw my weight behind!
