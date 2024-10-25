from method_obj import file
import os

'''
This code is to me what the Black Paintings were to Francisco De Goya.
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


    
def create_tree(root_path, include_inside_method):
    '''Initializes the tree structure from the point of a given file'''
    

    if os.path.isfile(root_path):#If the element in question is a file
        if root_path.endswith('.py'):
            #Handles python files
            file_to_add = file(os.path.basename(root_path), 'file', root_path)
            file_to_add.calc_mean(include_inside_method) #calculates all relevant values for the file
            return file_to_add
        else: return None #ignores all other files
    elif os.path.isdir(root_path):#If the element in question is a directory
   
        folder = file(os.path.basename(root_path), 'folder', root_path)
        
        for item in os.listdir(root_path): #Performs all relative actions for the elements in the folder
            item_path = os.path.join(root_path, item)
            child = create_tree(item_path, include_inside_method) 
            if child: folder.add_child(child)
        
        folder.calc_mean() #calculates all relevant values for the folder

        return folder

if __name__ == "__main__":
    include_inside_method = True
    match EXCECUTE_TESTS:
        case False:
                file_path = r"" #path to Keras here
                root = create_tree(file_path, include_inside_method)

                root.print_structure(0, None, True, True, True, True, True, True, True)
        case True:
                #Some simple test cases
                expected_list = {
                     "Test_case1": {"Type": "folder", "mean method size": 2, "weight": 9, "level": 0},
                     "Test_case1/test_case1-1.py": {"Type": "file", "mean method size": 2.67, "weight": 3, "level": 1},
                     "Test_case1/test_case1-2.py": {"Type": "file", "mean method size": 1.5, "weight": 2, "level": 1},
                     "Test_case1/test_case1-empty": {"Type": "folder", "mean method size": 0, "weight": 0, "level": 1},
                     "Test_case1/test_case1-nestled": {"Type": "folder", "mean method size": 1.75, "weight": 4, "level": 1},
                     "Test_case1/test_case1-nestled/test_case1-3.py": {"Type": "file", "mean method size": 1.75, "weight": 4, "level": 2},
                }
                file_path = "Test_case1" 

                current_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = current_dir +"/"+file_path

                root = create_tree(file_path, include_inside_method)

                print(root)
                root.print_structure(0, None, True, True, True, True, True, True, True)

                test_list = {}
                root.retrieve_data(test_list)


                print("Performing tests...") #checks all the tests
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
                




            