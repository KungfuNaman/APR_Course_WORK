import matplotlib.pyplot as plt
import numpy as np


# Open the text file
with open("KHeapSortLog.txt", "r", encoding='utf-8') as file:
# with open("dfsOutput", "r") as file:
    inside_parent_variant = False
    parent_info = {}

    def checkInitialVariants(initialProgramVariant):
        # Initialize a variable to track whether all variants are equal
        all_equal = True
        reference_variant = "variant 1"
        reference_data = initialProgramVariant[reference_variant]
        # Iterate through all variants and compare their data with the reference
        for variant, variant_data in initialProgramVariant.items():
            if variant != reference_variant:
                # Compare the data of this variant with the reference data
                if variant_data != reference_data:
                    all_equal = False
                    print(f"Variant {variant} is not equal to the reference variant.")
                    # You can also print the differences if needed
                    # print(f"Differences for variant {variant}: {variant_data}")

        # Check if all variants are equal
        if all_equal:
            printHighlight("All variants of population are equal.")

    def suspiciousLinesGraph(suspicious_lines,suspiciousLinesSize):
        # Convert the values from strings to floats
        suspicious_values = {int(k): float(v) for k, v in suspicious_lines.items()}

        # Extract line numbers and corresponding values
        line_numbers = list(suspicious_values.keys())
        values = list(suspicious_values.values())

        # Create a bar graph
        plt.bar(line_numbers, values, color='red', alpha=0.7)

        # Set labels and title
        plt.xlabel('Line Number')
        plt.ylabel('Suspicios Level (0-1)')
        plt.title('Suspicious Lines(Total='+suspiciousLinesSize+")")
        plt.xticks(line_numbers,rotation=90,fontsize=6)

        # Show the plot
        plt.show()
    
    def fitnessGraph(generationWiseMapping, break_indices=[]):
    # Extract the variant IDs and fitness values
        variants = []
        fitness_values = []
        for generation in generationWiseMapping.values():
            for variant_data in generation.values():
                variants.append(variant_data)
                fitness_values.append(int(float(variant_data.get("fitness", -1))))

        newX=[]
        newY=[]
        i=0
        for value in fitness_values:
            if int(float(value)) >= 0:
                newX.append(i)
                newY.append(int(float(value)))
            else:
                newX.append(np.nan)
                newY.append(np.nan)
            i=i+1
        # Ensure all values are plotted on the x-axis
        # if len(x_values) < 409:
        #     x_values.extend(range(len(x_values), 409))
        #     y_values.extend([0] * (409 - len(x_values)))

        # Create the line plot
        plt.plot(newX, newY,color='red',linewidth=0.9)
        plt.xlabel('Variant')
        plt.ylabel('Fitness Value')
        plt.title('Line Graph for Fitness Values of every Variant')
        if fitness_values:
            plt.yticks(range(max(min(fitness_values),0), max(fitness_values) + 1))

        # Show the plot
        plt.show()
    
    def operationsGraph(generationWiseMapping):
        operation_counts = {}

        # Loop through the data and count operation names
        for generation in generationWiseMapping.values():
            for variant in generation.values():
                operation_name = variant.get("operationName")
                if operation_name:
                    operation_counts[operation_name] = operation_counts.get(operation_name, 0) + 1

        # Extract operation names and their counts
        operation_names = list(operation_counts.keys())
        operation_counts = list(operation_counts.values())

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(operation_names, operation_counts,color='red')
        plt.xlabel("Operation Name")
        plt.ylabel("Count")
        plt.title("Number of Times Each Operation Name is Used")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
        for bar, count in zip(bars, operation_counts):
            plt.text(bar.get_x() + bar.get_width() / 2, count, str(count), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()
    
    def checkDuplicatesInOperations(generationWiseMapping):

        # Initialize a set to track combinations of lineNo, operations, and operationName
        combinations_set = set()

        # Initialize a list to store duplicates
        duplicates = []

        # Loop through the data and check for duplicates
        for generation in generationWiseMapping.values():
            for variantId,variant in generation.items():
                lineNo = variant.get("lineNo")
                operations = variant.get("operations")
                operationName = variant.get("operationName")
                
                # Create a unique identifier for the combination
                combination = (lineNo, operations, operationName)
                
                # Check if the combination is a duplicate
                if combination in combinations_set:
                    variant["variantId"]=variantId
                    duplicates.append(variant)  # Add the duplicate variant to the list
                else:
                    combinations_set.add(combination)

        printHighlight("Total unique operation combinations:"+str(len(combinations_set)))

        # Print duplicates
        if duplicates:
            printHighlight("Total duplicates in operations:"+str(len(duplicates)))
            printHighlight("Duplicate operations combinations found:")
            duplicateIds=[]
            duplicateOperationSet=set()
            for duplicate in duplicates:
                duplicateIds.append(duplicate.get('variantId'))
                duplicateOperationSet.add(duplicate.get("operationName"))

            duplicateNames=[]
            for name in duplicateOperationSet:
                duplicateNames.append(name)

            printHighlight("duplicate operations name:"+str(duplicateNames))


        else:
            printHighlight("No duplicate operations combinations found.")
    
    def checkDuplicatesInSolutions(solutionSummary):
        unique_diff_patches = set()
        # Initialize a list to store duplicates
        duplicates = []

        for variant_name, variant_data in solutionSummary.items():
            diff_patch = variant_data.get("diffPatch")

            if diff_patch in unique_diff_patches:
                duplicates.append(variant_name)
            else:
                unique_diff_patches.add(diff_patch)

        printHighlight("Total unique solutions:"+str(len(unique_diff_patches)))
        if duplicates:
            printHighlight("Duplicates found for the following variants:")
            printHighlight("Total duplicate solutions:" +str(len(duplicates)))
            print(duplicates)
        else:
            printHighlight("No duplicates found.")
    
    def printHighlight(str):
            print("\033[91m" + str + "\033[0m")
    
    def checkIterationFailure(generationWiseMapping):
        for generation in generationWiseMapping.values():
            for variantId,variant_data in generation.items():
                if "lineNo" not in variant_data:
                    printHighlight("This variant in iteration is different :"+variantId)
    
    def checkVariantIterationCount(generationWiseMapping):
        generation_counts = {}
        for generationId,variant in generationWiseMapping.items():
            generation_counts[generationId] = len(variant)

        for generation, count in generation_counts.items():
            print(f"Generation {generation}: {count} variants")
    
    suspiciousLines={}
    suspiciousLinesSize=0
    
    initialProgramVariant={}
    getInitialProgramVariant=0
    presentProgramVariant=0

    originalFitness=0

    generationWiseMapping={}
    getGenerationData=0
    subObj={}
    variantId=""
    getOperations=0
    getOperationName=0

    solutionSummary={}
    getSolutionSummary=0
    currSol=""
    getDiffSol=0
    totalNumberOfSolutions=0


    for line in file:
        # get suspicious lines:
        if line.startswith("Suspicious:"):
           suspiciousLines[line.split(":")[2].split(",")[0].replace(" ","")]=line.split(":")[2].split(",")[1].replace(" susp ","").replace("\n","")
        
        # get suspicious lines size:
        if line.startswith("---- Initial suspicious size:"):
           suspiciousLinesSize=line.split(":")[1].replace(" ","").replace("\n","")
        
        # get initial program variants
        if(line.startswith("Creating variant") or getInitialProgramVariant):
            getInitialProgramVariant=1
            if(line.startswith("Creating variant")):
                presentProgramVariant=line.replace("Creating variant ","").replace("\n","")
            elif(line.startswith("--ModifPoint")):
                if "variant " + presentProgramVariant in initialProgramVariant:
                    obj = initialProgramVariant["variant " + presentProgramVariant]
                else:
                    obj = {}    
                obj[line.split(",")[2].replace(" ","")]=line.split(",")[0].split(":")[1]
                initialProgramVariant["variant "+presentProgramVariant]=obj
            elif(line.startswith("Total suspicious from FL")):
                    obj=initialProgramVariant["variant "+presentProgramVariant]
                    obj["Total suspicious from FL"]=line.split(":")[1].replace("\n","").replace(" ","")
            elif(line.startswith("Total ModPoint created:")):
                initialProgramVariant["variant "+presentProgramVariant]["Total ModPoint created:"]=line.split(":")[1].replace("\n","").replace(" ","")
            # terminating situation for above
            elif(line.startswith("Calculating fitness")):
                getInitialProgramVariant=0
            
        elif(line.startswith("The original fitness")):
            originalFitness= line.split(":")[1].replace(" ","")
        
        #get generation details
        if(line.startswith("***** Generation") or getGenerationData):
            getGenerationData=1
            if(line.startswith("***** Generation")):
                currGeneration=line.split(":")[0].replace("***** Generation ","").replace(" ","")
                variantId=""
            if "generation " + currGeneration in generationWiseMapping:
                obj = generationWiseMapping["generation " + currGeneration]
            else:
                obj = {} 
            if(line.startswith("--Creating new operations")):
                variantId=line.replace("--Creating new operations for variant [","").split(",")[0].split(":")[1]
                if "variantId " + variantId in obj:
                    subObj = generationWiseMapping["generation " + currGeneration]["variantId "+ variantId]
                else:
                    subObj = {} 
                subObj["parent"]=line.replace("--Creating new operations for variant [","").split(",")[3].split(":")[1].replace("]","").replace("\n","")
                subObj["gens"]=line.replace("--Creating new operations for variant [","").split(",")[1].split(":")[1].replace(" ","")
            
            if(line.startswith("location: App.java")):
                subObj["lineNo"]=line.replace("location: App.java","").replace("\n","")
            if(line.startswith("-The child does NOT compile")):
                subObj["childCompiles"]="false"
            if(line.startswith("-The child compiles")):
                subObj["childCompiles"]="true"
            if(line.startswith("--Summary Creation:")):
                getOperations=0
            if(line.startswith("operation: OP_INSTANCE:") or getOperations):
                getOperations=1
                if(line.startswith("operation: OP_INSTANCE:")):
                    getOperationName=1
                text=subObj["operations"] if "operations" in subObj else ""
                subObj["operations"]=text +line
            if(getOperationName==1 and not line.startswith("operation: OP_INSTANCE:")):
                subObj["operationName"]=line.split(":")[0]
                getOperationName=0
            if(line.startswith("-Valid?:")):
                subObj["fitness"]=line.split(",")[1].replace(" fitness ","").replace("\n","")
                
            if(variantId!=""):
                obj["variantId "+variantId]=subObj
                generationWiseMapping["generation "+currGeneration]=obj
        
        #get number of solutions
        if(line.startswith("Number solutions:")):
                totalNumberOfSolutions=line.split(":")[1].replace(" ","")
        #getSolutionSummary
        if(line.startswith(" --SOLUTIONS DESCRIPTION--") or getSolutionSummary):
            getSolutionSummary=1
            if(line.startswith("ProgramVariant")):
                getDiffSol=0
                currSol=line.replace("ProgramVariant ","").replace("\n","")
            if(currSol):
                if "program variant "+ currSol in solutionSummary:
                    obj=solutionSummary["program variant "+ currSol]
                else:
                    obj={}
                if(line.startswith("operation:")):
                    obj["operation"]=line.split(":")[1].replace("\n","")
                if(line.startswith("line=")):
                    obj["lineNo"]=line.split("=")[1].replace("\n","")
                if(line.startswith("buggy kind=")):
                    obj["buggyKind"]=line.split("=")[1].replace("\n","")
                if(line.startswith("Patch kind=")):
                    obj["patchKind"]=line.split("=")[1].replace("\n","")
                if(line.startswith("generation=")):
                    obj["generation"]=line.split("=")[1].replace("\n","")
                if(line.startswith("diffpatchoriginal") or getDiffSol):
                    getDiffSol=1
                    text= obj["diffPatch"] if "diffPatch" in obj else ""
                    obj["diffPatch"]=text.replace("diffpatchoriginal=","")+line
                    
                solutionSummary["program variant "+ currSol]=obj
                if(line.startswith("Astor Output:")):
                    getDiffSol=0
                    getSolutionSummary=0


                    
              



    


        
        

    # printHighlight("suspiciousLines:"+suspiciousLines)
    # print("Initial suspicious size:",suspiciousLinesSize)
    suspiciousLinesGraph(suspiciousLines,suspiciousLinesSize)
    # print("Initial program variants:",initialProgramVariant["variant 1"])
    checkInitialVariants(initialProgramVariant)
    printHighlight("The original fitness is:"+originalFitness)
    # print("Generation mapping : ",generationWiseMapping)
    
    # Call the function with the top-level generation
    fitnessGraph(generationWiseMapping)
    print("solutionSummary:",solutionSummary)
    operationsGraph(generationWiseMapping)
    # checkVariantIterationCount(generationWiseMapping)

    checkIterationFailure(generationWiseMapping)
    checkDuplicatesInOperations(generationWiseMapping)
    checkDuplicatesInSolutions(solutionSummary)
    print("totalNumberOfSolutions:",totalNumberOfSolutions)
    # Specify the file name where you want to save the output
    file_name = "generation_mapping.json"

    # Open the file in write mode (use 'w' for writing, 'a' for appending)
    mapping = str(generationWiseMapping).replace("'", "\"")
    with open(file_name, "w") as file:
        # Write the content to the file
        file.write(mapping)

    printHighlight("Output of each iteration has been written to " +file_name)


    