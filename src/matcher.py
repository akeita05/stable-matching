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
	n = len(hospital_prefs)

	#edge case: n = 0
	if n == 0:
		return {}, 0

	#hospital_match[h] = student that hospital h is matched to (none if unmatched)
	hospital_match = {h: None for h in range(1, n+1)}

	#student_match[s] = hospital that student s is matched to (none if unmatched)
	student_match = {s: None for s in range(1, n+1)}

	#next_proposal[h] = index of next student on hospital h's list to propose to
	next_proposal = {h: 0 for h in range(1, n+1)}

	#ranking dictionary for effective lookup
	#student_ranking[s][h] = rank of hospital h in student s's preference list (lower is better)
	student_ranking = {}
	for s in range(1, n+1):
		student_ranking[s] = {}
		for rank, hospital in enumerate(student_prefs[s-1]):
			student_ranking[s][hospital] = rank

	#track proposals
	num_proposals = 0

	#while there is hospitals with students to propose to
	while True:
		#find an unmatched hospital
		free_hospital = None
		for h in range(1, n+1):
			if hospital_match[h] is None and next_proposal[h] < n:
				free_hospital = h
				break

		#if no unmatched hospitals, we're done
		if free_hospital is None:
			break

		#get the next student the hospital should propose to
		student = hospital_prefs[free_hospital - 1][next_proposal[free_hospital]]
		next_proposal[free_hospital] += 1
		num_proposals += 1

		#if student is unmatched, accept
		if student_match[student] is None:
			hospital_match[free_hospital] = student
			student_match[student] = free_hospital
		else:
			#if student is matched, compare current match with the new proposer
			current_hospital = student_match[student]

			#if student prefers the hospital with lower rank in their preference list
			if student_ranking[student][free_hospital] < student_ranking[student][current_hospital]:
				#swap matches
				hospital_match[current_hospital] = None #reject current match
				hospital_match[free_hospital] = student
				student_match[student] = free_hospital
			#else: student prefers current match, reject the new proposer (do nothing)

	return hospital_match, num_proposals

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

