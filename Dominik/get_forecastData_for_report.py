import sys
sys.path.insert(0, '/home/hans/Desktop/varsomdata')
#import dangerlevelsandproblems as dlp
from varsomdata import getforecastapi as gfa
from varsomscripts import dangerlevelsandproblems as dlp

a = gfa.get_avalanche_warnings(3003,"2020-10-01","2021-04-01", lang_key=2)
b = dlp._save_danger_and_problem_to_file(a, "my_own_warnings.csv")

print(a[0])
print(type(a[0]))
