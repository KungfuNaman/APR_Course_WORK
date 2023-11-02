import matplotlib.pyplot as plt


def extract_file_and_line_from_log(log_file):
    line_attempts_dict = {}

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("location: App.java"):
                line_num_str = line.replace("location: App.java", "").strip()
                line_num = int(line_num_str)

                if line_num in line_attempts_dict:
                    line_attempts_dict[line_num] += 1
                else:
                    line_attempts_dict[line_num] = 1

    line_numbers = list(line_attempts_dict.keys())
    attempts_values = list(line_attempts_dict.values())

    print(line_attempts_dict)
    print(attempts_values)
    return line_numbers, attempts_values



def plot_file_and_line_changes(files_lines, counts):
    plt.figure(figsize=(12, 8))
    plt.bar(files_lines, counts, color='blue')
    plt.ylabel('Number of Changes')
    plt.xlabel('File and Line Number')
    plt.title('Most Frequently Changed Locations in Code')
    plt.xticks(files_lines, rotation=45, ha='right')
    plt.tight_layout()
    plt.show()




def main():
    log_file = 'KHeapSortLog.txt'
    files_lines, counts = extract_file_and_line_from_log(log_file)
    plot_file_and_line_changes(files_lines, counts)


if __name__ == "__main__":
    main()
