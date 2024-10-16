import sys
import re
from method_obj import method, file
import os
import unittest

'''
This code is to me what the Black Paintings were to Francisco Goya.
Here, late in the night in my dark, empty and cold apartment, I work tirelessly.
The Python file, my canvas.
My despair, the paint.
And my brush, be it with madness, be it with genius, furiously strokes every line of code,
Shapes them,
Forms them,
Distorts them,
All with intent and purpose.

What war and a failing body did to the mind of Goya, regex and recursive functions have done to mine.
'''

EXCECUTE_TESTS = False

    
def create_tree(root_path):
    """Recursively create a tree structure starting from root_path."""
 
    if os.path.isfile(root_path):
        
        if root_path.endswith('.py'):
            file_to_add = file(os.path.basename(root_path), 'file', root_path)
            file_to_add.calc_mean()
            # print(f"Vad jag far ar: {file_to_add.get_mean_method_size()}")
            # print(f"Weight: {file_to_add.get_weight()}")
            return file_to_add
        else: return None
    elif os.path.isdir(root_path):
   
        folder = file(os.path.basename(root_path), 'folder', root_path)
        
        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            child = create_tree(item_path) 
            if child: folder.add_child(child)
        
        folder.calc_mean()

        return folder

def main():
    # Check if there are enough arguments passed
    if len(sys.argv) < 3:
        print("Usage: python myscript.py my_method parameter")
        sys.exit(1)

    # Get the method and parameter from the command-line arguments
    method = sys.argv[1]  # First argument (after script name)
    parameter = sys.argv[2]  # Second argument

    # Call the method based on the arguments

    # if method == "my_method":
    #     my_method(parameter)
    # else:
    #     print(f"Unknown method: {method}")


if __name__ == "__main__":
    match EXCECUTE_TESTS:
        case False:
                file_path = r"c:\Users\Sebastian Johansson\Desktop\Keras\keras-master" 
                # file_path = r"c:\Users\Sebastian Johansson\Desktop\Keras\keras-master\keras\src\backend\common\dtypes_test.py"
                root = create_tree(file_path)

                root.print_structure(0, None, True, True, True, True, True, True)
        case True:
                expected_list = {
                     "Test_case1": {"Type": "folder", "mean method size": 2, "weight": 9, "level": 0},
                     "Test_case1/test_case1-1.py": {"Type": "file", "mean method size": 2.67, "weight": 3, "level": 1},
                     "Test_case1/test_case1-2.py": {"Type": "file", "mean method size": 1.5, "weight": 2, "level": 1},
                     "Test_case1/test_case1-empty": {"Type": "folder", "mean method size": 0, "weight": 0, "level": 1},
                     "Test_case1/test_case1-nestled": {"Type": "folder", "mean method size": 1.75, "weight": 4, "level": 1},
                     "Test_case1/test_case1-nestled/test_case1-3.py": {"Type": "file", "mean method size": 1.75, "weight": 4, "level": 2},
                }
                file_path = "Test_case1" 
                #file_path = "C:/Users/Sebastian Johansson/Desktop/Keras/keras-master/benchmarks/layer_benchmark/core_benchmark.py"

                root = create_tree(file_path)

                test_list = {}
                root.retrieve_data(test_list)

                root.print_structure(0, None, True, True, True, True, True, True)

                print("Performing tests...")
                test_fail = False

                for i in list(expected_list.keys()):
                    if i not in list(test_list.keys()):
                        print(f"{i} was not found in the test list")
                        test_fail = True

                for i in list(test_list.keys()):
                    if i not in list(expected_list.keys()):
                        print(f"{i} was not found in the expected list")
                        test_fail = True
                    else:
                         for j in list(test_list[i].keys()):
                              test_val = test_list[i][j]
                              expected_val = expected_list[i][j]
                              if test_val != expected_val:
                                   print(f"{j} did not match for {i}\n\tExpected: {expected_val}\n\tActual: {test_val}")
                                   test_fail = True
                
                if not test_fail:
                     print("All tests cleared!")
                




            