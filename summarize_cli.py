from  src.model.negative_summarizer import NegativeSummarizer, SummarizerType
import sys
sys.path.append("./")
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

header = """
      ::::::::   ::::::::              :::           ::::::::   ::::::::  :::    :::     :::       :::::::: 
    :+:    :+: :+:    :+:           :+: :+:        :+:    :+: :+:    :+: :+:    :+:   :+: :+::   :+:    :+: 
   +:+        +:+    +:+          +:+   +:+       +:+        +:+        +:+    +:+  +:+   +:++  +:+         
  +#++:++#++ +#+    +:+         +#++:++#++:      +#++:++#++ +#+        +#++:++#++ +#++:++#++:: +#++:++#++   
        +#+ +#+    +#+         +#+     +#+             +#+ +#+        +#+    +#+ +#+     +#+         +#+    
#+#    #+# #+#    #+#         #+#     #+#      #+#    #+# #+#    #+# #+#    #+# #+#     #+#  #+#    #+#     
########   ########          ###     ###       ########   ########  ###    ### ###     ###   #######  
"""

print(f"{bcolors.OKGREEN}{header}{bcolors.ENDC}")

location = input(f"{bcolors.HEADER}Über welchen wiener Ort willst du mehr erfahren?{bcolors.ENDC}\n")

# init summarizer with wished type
summarizer = NegativeSummarizer(location, SummarizerType.EXTRACTIVE)

count = int(input(f"{bcolors.HEADER}Wieviele Informationen willst du haben?{bcolors.ENDC}\n"))

print(f"{bcolors.OKGREEN}Berechne Informationen...{bcolors.ENDC}\n")

# summerize values
summaries = summarizer.summarize(count)

print(f"\n{bcolors.OKCYAN}{location} is a schaas, weil...{bcolors.ENDC}\n")

for summary in summaries:
    print(f"\t-{bcolors.OKCYAN}{summary}{bcolors.ENDC}\n")
    




