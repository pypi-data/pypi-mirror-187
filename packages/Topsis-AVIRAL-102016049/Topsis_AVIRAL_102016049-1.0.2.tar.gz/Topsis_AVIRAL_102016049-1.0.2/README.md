
# Topsis Description

This python package can help you to calculate topsis score and corresponding rank in maximum 2-3 lines of code.

The package will create a csv file corresponding to the input details i.e. dataframe with additional parameters like weights and impacts of those columns present in dataframe.

# Usage

__Step 1:__ Install the topsis package using the following commmand. (pip install Topsis-Anirudh-101916111==2.2)

__Step 2:__ Import the package using the commmand. (tp=\_\_import__("Topsis-AVIRAL-101916111"))

__Step 3:__ Call the Topsis function to generate the csv file in which 1st parameter is your input dataframe, 2nd is weights, 3rd is impacts and last is the name of output csv file. For eg:

tp.topsis('101916111-data.csv',"1,1,1,1,1","+,+,+,+,+","result.csv")

This command will generate a csv file named result.csv.

# Constraints
1) Input dataframe with 1st column as model name and rest are it's features.
2) Weights must be commas seperated and in the form of a string.
3) Impacts must be commas seperated and in the form of a string having only positive and negative sign.
4) Don't forget to put .csv extension otherwise it will throw an error