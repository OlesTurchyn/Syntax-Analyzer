import sys

# Check if the user provided the file name as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python read_file.py <file_name>")
    sys.exit(1)

# Get the file name from the command-line argument
file_name = sys.argv[1]

try:
    # Open and read the specified text file
    with open(file_name, 'r') as file:
        contents = file.read()
        print("File contents:")
        print(contents)
except FileNotFoundError:
    print(f"File '{file_name}' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")