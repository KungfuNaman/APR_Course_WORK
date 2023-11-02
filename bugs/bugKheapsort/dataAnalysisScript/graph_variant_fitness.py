import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def extract_variant_id_and_fitness_from_log(log_file):
    variant_fitness_dict = {}
    last_variant_id = None

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            if "--Summary Creation: for variant [Variant id:" in line:
                variant_id_str = line.split("[Variant id:")[1].split(",")[0].strip()
                current_variant_id = int(variant_id_str)

                if last_variant_id is not None and last_variant_id != current_variant_id:
                    if last_variant_id not in variant_fitness_dict:
                        variant_fitness_dict[last_variant_id] = 0

                last_variant_id = current_variant_id

            elif ", fitness " in line and last_variant_id is not None:
                fitness_str = line.split(", fitness ")[1].strip()
                fitness_value = round(float(fitness_str), 2)

                if last_variant_id in variant_fitness_dict:
                    variant_fitness_dict[last_variant_id] = max(variant_fitness_dict[last_variant_id], fitness_value)
                else:
                    variant_fitness_dict[last_variant_id] = fitness_value

                last_variant_id = None

    if last_variant_id is not None and last_variant_id not in variant_fitness_dict:
        variant_fitness_dict[last_variant_id] = 0

    variant_ids = list(variant_fitness_dict.keys())
    fitness_values = list(variant_fitness_dict.values())

    print(variant_fitness_dict)
    print(fitness_values)
    return variant_ids, fitness_values


def merge_variant_id_and_fitness(variant_ids, fitness_values):
    merged_data = {}

    for variant_id, fitness in zip(variant_ids, fitness_values):
        if variant_id in merged_data:
            merged_data[variant_id] = max(merged_data[variant_id], fitness)
        else:
            merged_data[variant_id] = fitness

    merged_variant_ids = sorted(merged_data.keys())
    merged_fitness_values = [merged_data[variant_id] for variant_id in merged_variant_ids]

    print(merged_variant_ids)
    print(merged_fitness_values)

    return merged_variant_ids, merged_fitness_values


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_data(variant_ids, fitness_values):
    plt.figure(figsize=(10, 6))
    plt.plot(variant_ids, fitness_values, color='red')
    plt.xlabel('Variant')
    plt.ylabel('Fitness Value')
    plt.title('Fitness Value by Variant')

    # Set custom x-axis tick labels
    x_ticks = [0, 30, 50, 70, 100,130,150,170,200,230,250,270,300,330,350,370,400,430,450,470,500]
    plt.xticks(x_ticks, labels=x_ticks)

    plt.tight_layout()

    plt.ylim(0, 4.1)
    # Adjust y-axis tick labels to show two decimal places
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    plt.xlim(0, max(variant_ids) + 2)

    plt.show()


def main():
    log_file = 'KHeapSortLog.txt'
    variant_ids, fitness_values = extract_variant_id_and_fitness_from_log(log_file)
    variant_ids, merged_fitness_values = merge_variant_id_and_fitness(variant_ids, fitness_values)
    merged_fitness_values = ["{:.2f}".format(float(value)) for value in merged_fitness_values]
    merged_fitness_values = [float(value) for value in merged_fitness_values]

    plot_data(variant_ids, merged_fitness_values)


if __name__ == "__main__":
    main()
