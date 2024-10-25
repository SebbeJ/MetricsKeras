import pytest
import cProfile as cp
import pstats
import io

if __name__ == "__main__":
    print("Profiling")
    folder = "profiling/profile_results"
    test_files = [  
        #"examples/demo_functional.py",
        #"examples/demo_mnist_convnet.py",
        #"integration_tests/basic_full_flow.py"
    ]
    
    for tf in test_files:
        print(f"Profiling {tf}")
        
        #Enable the profiler. Run the program. Disable the profiler.
        profiler = cp.Profile()
        profiler.enable()
        if "test" in tf:
            pytest.main([tf])
        else:
            exec(open(tf).read())
        profiler.disable()

        #Dump the profiling output to a .prof file
        with open(folder + '/' + tf.split("/")[1] + '.prof', 'w') as f:
            profiler.dump_stats(f.name)

        # .csv convertion
        result = io.StringIO()
        pstats.Stats(profiler, stream=result).print_stats()

        result = result.getvalue()

        result = 'ncalls' + result.split('ncalls')[-1]
        result = '\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])
        
        with open(folder + '/' + tf.split("/")[1] + '.csv', 'w') as f:
            f.write(result)
        
