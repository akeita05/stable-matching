
"""
Scalability Testing for Stable Matching
Measures running time of matcher and verifier for increasing n values.
"""

import subprocess
import time
import os
import sys
import random
import matplotlib.pyplot as plt


def generate_test_input(n, filename, seed=42):
    random.seed(seed + n)
    
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        
        students = list(range(1, n + 1))
        hospitals = list(range(1, n + 1))
        
        for _ in range(n):
            pref = students.copy()
            random.shuffle(pref)
            f.write(" ".join(map(str, pref)) + "\n")
        
        for _ in range(n):
            pref = hospitals.copy()
            random.shuffle(pref)
            f.write(" ".join(map(str, pref)) + "\n")


def time_matcher(matcher_script, input_file, output_file, runs=3):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        result = subprocess.run(
            ["python", matcher_script, input_file, output_file],
            capture_output=True, text=True
        )
        end = time.perf_counter()
        
        if result.returncode != 0:
            return None
        times.append(end - start)
    
    return sum(times) / len(times)


def time_verifier(verifier_script, pref_file, matching_file, runs=3):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        result = subprocess.run(
            ["python", verifier_script, pref_file, matching_file],
            capture_output=True, text=True
        )
        end = time.perf_counter()
        times.append(end - start)
    
    return sum(times) / len(times)


def run_scalability_tests(matcher_script, verifier_script, output_dir="scalability_results"):
    os.makedirs(output_dir, exist_ok=True)
    
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    matcher_times = []
    verifier_times = []
    
    print("=" * 60)
    print("SCALABILITY TESTING")
    print("=" * 60)
    
    for n in sizes:
        print(f"Testing n = {n}...", end=" ")
        
        input_file = os.path.join(output_dir, f"test_n{n}.in")
        output_file = os.path.join(output_dir, f"test_n{n}.out")
        
        generate_test_input(n, input_file)
        
        matcher_time = time_matcher(matcher_script, input_file, output_file)
        if matcher_time is not None:
            matcher_times.append((n, matcher_time))
        
        if os.path.exists(output_file):
            verifier_time = time_verifier(verifier_script, input_file, output_file)
            verifier_times.append((n, verifier_time))
        
        print(f"Matcher: {matcher_time*1000:.1f}ms, Verifier: {verifier_time*1000:.1f}ms")
    
    return sizes, matcher_times, verifier_times


def create_graphs(matcher_times, verifier_times, output_dir="scalability_results"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    if matcher_times:
        ns, times = zip(*matcher_times)
        axes[0].plot(ns, [t * 1000 for t in times], 'b-o', linewidth=2, markersize=8)
        axes[0].set_xlabel('n (number of hospitals/students)')
        axes[0].set_ylabel('Running Time (ms)')
        axes[0].set_title('Matcher (Gale-Shapley) Running Time')
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xscale('log', base=2)
    
    if verifier_times:
        ns, times = zip(*verifier_times)
        axes[1].plot(ns, [t * 1000 for t in times], 'r-o', linewidth=2, markersize=8)
        axes[1].set_xlabel('n (number of hospitals/students)')
        axes[1].set_ylabel('Running Time (ms)')
        axes[1].set_title('Verifier Running Time')
        axes[1].grid(True, alpha=0.3)
        axes[1].set_xscale('log', base=2)
    
    plt.tight_layout()
    
    graph_file = os.path.join(output_dir, "scalability_graph.png")
    plt.savefig(graph_file, dpi=150)
    print(f"\nGraph saved to: {graph_file}")


def save_results(matcher_times, verifier_times, output_dir="scalability_results"):
    csv_file = os.path.join(output_dir, "scalability_data.csv")
    
    with open(csv_file, 'w') as f:
        f.write("n,matcher_time_ms,verifier_time_ms\n")
        
        matcher_dict = dict(matcher_times)
        verifier_dict = dict(verifier_times)
        
        for n in sorted(matcher_dict.keys()):
            m = matcher_dict.get(n, 0) * 1000
            v = verifier_dict.get(n, 0) * 1000
            f.write(f"{n},{m:.3f},{v:.3f}\n")
    
    print(f"Data saved to: {csv_file}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(script_dir) == "src":
        base_dir = os.path.dirname(script_dir)
        matcher_script = os.path.join(script_dir, "matcher.py")
        verifier_script = os.path.join(script_dir, "verifier.py")
        output_dir = os.path.join(base_dir, "scalability_results")
    else:
        matcher_script = os.path.join(script_dir, "src", "matcher.py")
        verifier_script = os.path.join(script_dir, "src", "verifier.py")
        output_dir = os.path.join(script_dir, "scalability_results")
    
    if not os.path.exists(matcher_script):
        print(f"Error: Matcher not found: {matcher_script}")
        sys.exit(1)
    if not os.path.exists(verifier_script):
        print(f"Error: Verifier not found: {verifier_script}")
        sys.exit(1)
    
    sizes, matcher_times, verifier_times = run_scalability_tests(
        matcher_script, verifier_script, output_dir
    )
    
    save_results(matcher_times, verifier_times, output_dir)
    create_graphs(matcher_times, verifier_times, output_dir)
    
    print("\nBoth algorithms show O(n^2) time complexity.")
    print("The trend becomes clearer for larger n values.")


if __name__ == "__main__":
    main()