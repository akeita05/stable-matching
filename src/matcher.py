import sys

def parse_input(filename):
	try:
		with open(filename, 'r') as f:
			lines = f.readlines()

		#strip whitespace and remove empty lines
		lines = [line.strip() for line in lines if line.strip()]

		if len(lines) == 0:
			raise ValueError("Input file is empty")

		#first line: integer n
		n = int(lines[0])

		if n < 0:
			raise ValueError("n must be non-negative")

		if n == 0:
			return 0, [], []

		#check if there is enough lines
		if len(lines) < 1 + 2 * n:
			raise ValueError(f"Expected {1 + 2*n} lines, but got {len(lines)}")

		#next n lines: hospital preference lists
		hospital_prefs = []
		for i in range(1, n+1):
			prefs = list(map(int, lines[i].split()))
			if len(prefs) != n:
				raise ValueError(f"Hospital {i} preference list expected {n} students, but has {len(prefs)}")

			#validate that list is a permutation of 1..n
			if sorted(prefs) != list(range(1, n+1)):
				raise ValueError(f"Hospital {1} preference list is not a valid permutation of 1..{n}")

			hospital_prefs.append(prefs)

		#next n lines: student preference lists
		student_prefs = []
		for i in range(n+1, 2*n+1):
			prefs = list(map(int, lines[i].split()))
			if len(prefs) != n:
				raise ValueError(f"Student {i-n} preference list expected {n}, but has {len(prefs)}")

			#validate that list is permutation of 1..n
			if sorted(prefs) != list(range(1, n+1)):
				raise ValueError(f"Students {i-n} preference list is not a valid permutation of 1..{n}")

			student_prefs.append(prefs)

		return n, hospital_prefs, student_prefs
	except FileNotFoundError:
		raise FileNotFoundError(f"Input file '{filename}' not found")
	except ValueError as e:
		raise ValueError(f"Invalid input format: {e}")
	except Exception as e:
		raise Exception(f"Error parsing input: {e}")

def write_output(matching, filename):
	try:
		with open(filename, 'w') as f:
			#sort by hospital number
			for hospital in sorted(matching.keys()):
				f.write(f"{hospital} {matching[hospital]}\n")
		print(f"Output written to {filename}")
	except Exception as e:
		raise Exception(f"Error writing output: {e}")

def gale_shapley(hospital_prefs, student_prefs):
	#TO DO: full gale-shapley algorithm
	n = len(hospital_prefs)
	matching = {}

	for i in range(1, n+1):
		matching[i] = i

	return matching, 0

def main():
	if len(sys.argv) != 3:
		print("Usage: python matcher.py <input_file <output_file>")
		sys.exit(1)

	input_file = sys.argv[1]
	output_file = sys.argv[2]

	try:
		#parse input
		n, hospital_prefs, student_prefs = parse_input(input_file)
		print(f"Parsed input: n = {n}")

		#run gale-shapley
		matching, num_proposals = gale_shapley(hospital_prefs, student_prefs)

		#write output
		write_output(matching, output_file)
		print(f"Matching complete! Total proposals: {num_proposals}")
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)

if __name__ == "__main__":
	main() 

