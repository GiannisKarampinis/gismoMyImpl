import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
import sys
import os

# Step 1: Read the matrix from the file
def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Read matrix dimensions
        rows, cols = map(int, lines[0].strip().split())
        
        # Read matrix data
        data = []
        for line in lines[1:]:
            data.append(list(map(float, line.strip().split())))
        
        matrix = np.array(data)
        return matrix

# Step 2: Plot sparsity pattern
def plot_sparsity(matrix, title, subplot_position, rows, cols):
    plt.subplot(rows, cols, subplot_position)
    sparse_matrix = csr_matrix(matrix)
    plt.spy(sparse_matrix, markersize=5, color='darkblue')  # Changed color to dark blue
    plt.title(title, fontsize=12)
    plt.xlabel("Columns", fontsize=10)
    plt.ylabel("Rows", fontsize=10)
    
    # Adjust ticks for better readability
    plt.xticks(
        np.arange(0, matrix.shape[1] + 1, step=max(1, matrix.shape[1] // 10)),
        fontsize=8, rotation=45
    )
    plt.yticks(
        np.arange(0, matrix.shape[0] + 1, step=max(1, matrix.shape[0] // 10)),
        fontsize=8
    )

# Step 3: Check if a matrix is diagonally dominant
def is_diagonally_dominant(matrix):
    for i in range(len(matrix)):
        row_sum = np.sum(np.abs(matrix[i])) - np.abs(matrix[i][i])
        if np.abs(matrix[i][i]) <= row_sum:
            return False
    return True

# Step 4: Check if a matrix is positive definite
def is_positive_definite(matrix):
    try:
        np.linalg.cholesky(matrix)
        return True
    except np.linalg.LinAlgError:
        return False

# Main function to handle arguments and process the files
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_sparsity.py <filename1> <filename2> ... <filenameN>")
        sys.exit(1)

    filenames = sys.argv[1:]
    total_files = len(filenames)

    # Calculate number of rows needed for 2 columns
    cols = 2
    rows = (total_files + 1) // cols

    plt.figure(figsize=(12, 6 * rows))  # Adjust figure size based on number of subplots

    for i, filepath in enumerate(filenames, start=1):
        filename = os.path.basename(filepath)  # Get filename with extension
        title = os.path.splitext(filename)[0]  # Remove extension for title
        try:
            matrix = read_matrix_from_file(filepath)
            plot_sparsity(matrix, title=title, subplot_position=i, rows=rows, cols=cols)

            # Check and log matrix properties
            if is_diagonally_dominant(matrix):
                print(f"{title}: The matrix is diagonally dominant.")
            else:
                print(f"{title}: The matrix is not diagonally dominant.")
            
            if is_positive_definite(matrix):
                print(f"{title}: The matrix is positive definite.")
            else:
                print(f"{title}: The matrix is not positive definite.")
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except Exception as e:
            print(f"An error occurred with file {filepath}: {e}")

    # Reserve space for a main title and adjust subplot layout
    plt.suptitle("Sparsity Patterns of Matrices", fontsize=18, y=1.02)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for suptitle
    plt.subplots_adjust(hspace=0.4)  # Increase space between subplots
    plt.show()

