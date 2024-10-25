import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dataclasses import dataclass

# Directory to search for Python files
search_dir = "/home/oliver/Github/keras"

# Initialize frequency array, sum, max, and max_statements
@dataclass
class Frequnecy:
    array: list
    max_indentation: int = 0
    max_statement: str = ""
    max_file: str = ""

    def output(self):
        print("---Frequnecy---")
        print(f"{self.array=}")
        print(f"{self.max_indentation=}")
        print(f"{self.max_statement=}")
        print(f"{self.max_file=}")
        print("---------------")

frequency_if = Frequnecy([0] * 8)
frequency_for = Frequnecy([0] * 8)
frequency_while = Frequnecy([0] * 8)

# Find all Python files in the specified directory
python_files = []
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith(".py"):
            python_files.append(os.path.join(root, file))

# Process each Python file
def get_nesting_list(frequency: Frequnecy, file: str, all_statements):
    for statement in all_statements:
        indentation_level = re.match(r"^ +", statement) # Count the number of tabs at the beginning
        if indentation_level is None:
            indentation_level = 0
        else:
            indentation_level = int(indentation_level.regs[0][1]/4)

        frequency.array[indentation_level] += 1

        if indentation_level >= frequency.max_indentation:
            frequency.max_indentation = indentation_level
            frequency.max_statement = statement
            frequency.max_file = file

for file in python_files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Search for lines containing 'if' statements using regex
    if_statements = [line for line in lines if re.search(r"^\s*if .*:", line, re.IGNORECASE)]
    for_statements = [line for line in lines if re.search(r"^\s*for .*:", line, re.IGNORECASE)]
    while_statements = [line for line in lines if re.search(r"^\s*while .*:", line, re.IGNORECASE)]
    # Count occurrences and measure indentation
    get_nesting_list(frequency_if, file, if_statements)
    get_nesting_list(frequency_for, file, for_statements)
    get_nesting_list(frequency_while, file, while_statements)

frequency_if.output()
frequency_for.output()
frequency_while.output()

frequency_df = pd.DataFrame({"if":frequency_if.array, 
                             "for":frequency_for.array,
                             "while":frequency_while.array})
fig, ax = plt.subplots()
ax.set_xlabel("Nesting Level")
ax.set_ylabel("Instances Found")
ax.set_title("Frequency over nested statments by nesting level")
frequency_df.plot(kind='bar', stacked=True, color=sns.palettes.color_palette("bright", n_colors=3), ax=ax)
ax.set_xticklabels(ax.get_xticks(), rotation=0)
plt.show()

frequency_sum = [0]*8
for i in range(0, 8):
    frequency_sum[i] = frequency_if.array[i] \
                        + frequency_for.array[i] \
                        + frequency_while.array[i]
print(sum(frequency_sum))
print(sum(frequency_sum[0:4]), sum(frequency_sum[4:]))
