import subprocess
import os
import itertools
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Run an executable with varying parameters and set OMP_NUM_THREADS.")
    parser.add_argument("executable", help="Path to the executable to run.")
    parser.add_argument("-r", type=int, nargs=2, metavar=('start', 'end'), required=True,
                        help="Range for the -r argument (start and end inclusive).")
    parser.add_argument("-e", type=int, nargs=2, metavar=('start', 'end'), required=True,
                        help="Range for the -e argument (start and end inclusive).")
    parser.add_argument("--threads", type=int, nargs=2, metavar=('min', 'max'), required=True,
                        help="Range for the number of threads (min and max inclusive).")
    parser.add_argument("--log", type=str, default="execution_log.txt", help="Log file to save execution details.")
    
    args = parser.parse_args()
    
    executable = args.executable
    r_start, r_end = args.r
    e_start, e_end = args.e
    threads_min, threads_max = args.threads
    log_file = args.log

    with open(log_file, "w") as log:
        log.write(f"Execution Log - {datetime.now()}\n")
        log.write(f"Executable: {executable}\n")
        log.write(f"Ranges: -r [{r_start}, {r_end}], -e [{e_start}, {e_end}], Threads [{threads_min}, {threads_max}]\n\n")
        
        for r in range(r_start, r_end + 1):
            for e in range(e_start, e_end + 1):
                for threads in range(threads_min, threads_max + 1):
                    env = os.environ.copy()
                    env['OMP_NUM_THREADS'] = str(threads)  # Set the OMP_NUM_THREADS environment variable
            
                    cmd = ["/bin/bash", "-c", f"OMP_NUM_THREADS={threads} {executable} -r {r} -e {e} --last"]
                    log.write(f"Running command: {' '.join(cmd)}\n")
                    log.write(f"Environment: OMP_NUM_THREADS={threads}\n")
            
                    try:
                        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
                        log.write(f"Exit Code: {result.returncode}\n")
                        log.write(f"Output:\n{result.stdout}\n")
                        log.write(f"Errors:\n{result.stderr}\n")
                    except Exception as ex:
                        log.write(f"Error executing command: {ex}\n")
            
                    log.write("\n" + "="*40 + "\n\n")

if __name__ == "__main__":
    main()

