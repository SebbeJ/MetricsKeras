from collections import defaultdict
import matplotlib.pyplot as plt

def read_folder_counts(file_path):
    folder_counts = {}
    with open(file_path, 'r') as f:
        for line in f:
            folder_name, count = line.strip().split(': ')
            folder_counts[folder_name] = int(count)
    return folder_counts

def parse_test_file(file_path):
    # Dictionary to store the number of tests per module (script)
    test_counts = defaultdict(int)
    current_module = None
    total_tests = 0  # Counter for total tests

    # Open and read the file
    with open(file_path, 'r', encoding='utf-16') as file:
        lines = file.readlines()
        for line in lines:
            # Modify the line: replace tabs and strip whitespace
            line = line.replace("\t", " ").strip()
            
            # Check if the line is a module
            if line.startswith("<Package"):
                current_module = line.split()[1].strip(">")
                test_counts[current_module] = 0
                continue

            # Check if the line is a test case function
            if line.startswith("<TestCaseFunction") and current_module:
                test_counts[current_module] += 1
                total_tests += 1  # Increment the total tests count

    return sorted(test_counts.items(), key=lambda x: x[1], reverse=True), total_tests

def compare_tests_and_lines(test_counts, line_counts):
    comparison_results = {}
    
    for module, test_count in test_counts:
        # Remove '.py' if present to match the folder counts
        module_name = module.replace('.py', '')
        lines = line_counts.get(module_name, 0)
        percentage = (test_count / lines * 100) if lines > 0 else 0
        comparison_results[module_name] = {
            'tests': test_count,
            'lines': lines,
            'percentage': percentage,
            'difference': test_count - lines
        }

    return comparison_results

def plot_distribution(test_counts, total_tests):
    # Prepare data for the pie chart with all modules
    all_modules = [module for module, _ in test_counts]
    all_counts = [count for _, count in test_counts]

    # Calculate percentages for the pie chart and legend
    percentages = [(count / total_tests) * 100 for count in all_counts]

    # Create a pie chart
    plt.figure(figsize=(12, 7))  # Increased figure size for better spacing
    wedges, texts, autotexts = plt.pie(all_counts, labels=all_modules, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Tests for All Modules', pad=20)  # Title with padding
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Create a legend with counts and percentages
    legend_labels = [f"{module}: {count} tests ({percentage:.1f}%)" for module, count, percentage in zip(all_modules, all_counts, percentages)]
    plt.legend(wedges, legend_labels, title="Modules", loc="upper left", bbox_to_anchor=(1, 1), ncol=1)

    # Adjust the title position to the bottom
    plt.subplots_adjust(right=0.75)  # Adjust the right side to prevent cut-off

    plt.show()


def plot_tests_per_lines(comparison_results):
    # Prepare data for the bar plot
    modules = list(comparison_results.keys())
    percentages = [data['percentage'] for data in comparison_results.values()]

    # Sort the data by percentage
    sorted_data = sorted(zip(modules, percentages), key=lambda x: x[1], reverse=True)
    sorted_modules, sorted_percentages = zip(*sorted_data)  # Unzip sorted data

    # Create a bar plot
    plt.figure(figsize=(12, 6))
    plt.barh(sorted_modules, sorted_percentages, color='skyblue')
    plt.xlabel('Percentage of Tests per Lines of Code (%)')
    plt.title('Percentage of Tests per Lines of Code for Each Module')
    plt.axvline(x=100, color='red', linestyle='--')  # Add a line at 100% for reference
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.show()

# Example usage:
test_file = 'test_list.txt'  # Path to your test list file
line_file = 'folder_counts.txt'  # Path to the line counts file

line_counts = read_folder_counts(line_file)  # Read line counts
sorted_test_counts, total_tests = parse_test_file(test_file)  # Read test counts
comparison_results = compare_tests_and_lines(sorted_test_counts, line_counts)  # Compare tests and lines

# Print comparison results
print("\nComparison of Tests and Lines:")
for module, data in comparison_results.items():
    print(f"{module}: {data['tests']} tests, {data['lines']} lines, percentage: {data['percentage']:.2f}%, difference: {data['difference']}")

# Plot distribution of tests for all modules
plot_distribution(sorted_test_counts, total_tests)

# Plot the percentage of tests per lines of code
plot_tests_per_lines(comparison_results)
