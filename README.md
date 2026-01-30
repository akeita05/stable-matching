# Stable Matching - Gale-Shapley Algorithm

## Team Members
- Person A: Aicha Keita (66149226)
- Person B:

## Project Description
Implementation of the Gale-Shapley algorithm for the hospital-student stable matching problem. Including a verifier to check validity and stability of matchings.

## File Structure
```

stable-matching/
	README.md
	src/
		matcher.py	# Hospital-proposing Gale-Shapley implementation
		verifier.py	# Validity and stability checker
	examples/
		example.in	# Sample input file
		example.out
	tests/			# Additional test cases
		test_empty.in
		test1.in
		test2.in
		test4.in
		test_invalid.in
		test_invalid2.in		
```		
		
## How to Run

### Prerequisites
- Python 3.x

### Running the Matcher
```bash
python src/matcher.py
```

Example:
```bash
python src/matcher.py examples/example.in examples/example.out
```

## Input Format
- First line: integer `n` (number of hospitals and students)
- Next `n` lines: hospital preference lists (space-separated integers 1 to n)
- Next `n` lines: student preference lists (space-separated integers 1 to n)

Each preference list is a permutation of 1..n.

## Output Format

### Matcher Output
`n` lines, one per hospital:
```

hospital_id student_id
```

## Algorithm Details

### Gale-Shapley (Hospital-Proposing)
1. Initially, all hospitals are unmatched
2. While there exsists an unmatched hospital with students left to propose to:
	- Hospitals proposes to next student on its preference list
	- Student tentatively accepts best hospital between current match and new proposer
	- Other hospital is rejected
3. Terminates when all hospitals are matched

## Assumptions
- Input files are well-formed
- Preference lists are complete permutations of 1..n
- 1-indexed hospital and students
