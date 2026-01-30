
"""
Verifier for Hospital-Student Stable Matching
Checks validity and stability of a proposed matching.

"""

import sys


def parse_preferences(filename):
    """
    Parse the preference file.
    Returns: n, hospital_prefs (dict), student_prefs (dict)
    
    hospital_prefs[h] = list of students in order of preference (1-indexed)
    student_prefs[s] = list of hospitals in order of preference (1-indexed)
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    n = int(lines[0])
    
    if n == 0:
        return 0, {}, {}
    
    # Validate we have enough lines
    if len(lines) != 2 * n + 1:
        raise ValueError(f"Expected {2*n + 1} lines, got {len(lines)}")
    
    hospital_prefs = {}
    student_prefs = {}
    
    # Parse hospital preferences (lines 1 to n)
    for i in range(1, n + 1):
        prefs = list(map(int, lines[i].split()))
        if len(prefs) != n:
            raise ValueError(f"Hospital {i} has {len(prefs)} preferences, expected {n}")
        if sorted(prefs) != list(range(1, n + 1)):
            raise ValueError(f"Hospital {i} preferences must be a permutation of 1..{n}")
        hospital_prefs[i] = prefs
    
    # Parse student preferences (lines n+1 to 2n)
    for i in range(n + 1, 2 * n + 1):
        student_id = i - n
        prefs = list(map(int, lines[i].split()))
        if len(prefs) != n:
            raise ValueError(f"Student {student_id} has {len(prefs)} preferences, expected {n}")
        if sorted(prefs) != list(range(1, n + 1)):
            raise ValueError(f"Student {student_id} preferences must be a permutation of 1..{n}")
        student_prefs[student_id] = prefs
    
    return n, hospital_prefs, student_prefs


def parse_matching(filename):
    """
    Parse the matching output file.
    Returns: dict mapping hospital -> student
    """
    matching = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Invalid matching line: {line}")
                hospital, student = int(parts[0]), int(parts[1])
                matching[hospital] = student
    return matching


def check_validity(n, matching):
    """
    Check if the matching is valid:
    - Each hospital 1..n is matched exactly once
    - Each student 1..n is matched exactly once
    - No duplicates
    
    Returns: (is_valid, error_message or None)
    """
    if n == 0:
        if len(matching) == 0:
            return True, None
        else:
            return False, "Expected empty matching for n=0"
    
    # Check all hospitals are present
    hospitals_in_matching = set(matching.keys())
    expected_hospitals = set(range(1, n + 1))
    
    if hospitals_in_matching != expected_hospitals:
        missing = expected_hospitals - hospitals_in_matching
        extra = hospitals_in_matching - expected_hospitals
        msg = ""
        if missing:
            msg += f"Missing hospitals: {missing}. "
        if extra:
            msg += f"Extra hospitals: {extra}."
        return False, msg.strip()
    
    # Check all students are present and no duplicates
    students_in_matching = list(matching.values())
    expected_students = set(range(1, n + 1))
    
    if len(students_in_matching) != len(set(students_in_matching)):
        # Find duplicates
        seen = set()
        duplicates = set()
        for s in students_in_matching:
            if s in seen:
                duplicates.add(s)
            seen.add(s)
        return False, f"Duplicate students in matching: {duplicates}"
    
    if set(students_in_matching) != expected_students:
        missing = expected_students - set(students_in_matching)
        extra = set(students_in_matching) - expected_students
        msg = ""
        if missing:
            msg += f"Missing students: {missing}. "
        if extra:
            msg += f"Extra students: {extra}."
        return False, msg.strip()
    
    return True, None


def get_rank(pref_list, item):
    """
    Get the rank (0-indexed) of item in preference list.
    Lower rank = more preferred.
    """
    return pref_list.index(item)


def check_stability(n, matching, hospital_prefs, student_prefs):
    """
    Check if the matching is stable (no blocking pairs).
    
    """
    if n == 0:
        return True, None
    
    # Create reverse mapping: student -> hospital
    student_to_hospital = {s: h for h, s in matching.items()}
    
    # Check every possible (hospital, student) pair
    for h in range(1, n + 1):
        current_student = matching[h]
        h_current_rank = get_rank(hospital_prefs[h], current_student)
        
        for s in range(1, n + 1):
            if s == current_student:
                continue  # Already matched
            
            # Does h prefer s over current match?
            h_pref_for_s = get_rank(hospital_prefs[h], s)
            if h_pref_for_s >= h_current_rank:
                continue  # h doesn't prefer s over current match
            
            # Does s prefer h over their current match?
            current_hospital = student_to_hospital[s]
            s_current_rank = get_rank(student_prefs[s], current_hospital)
            s_pref_for_h = get_rank(student_prefs[s], h)
            
            if s_pref_for_h < s_current_rank:
                # Blocking pair found!
                return False, (h, s)
    
    return True, None


def verify(pref_file, matching_file):
    """
    Main verification function
    """
    try:
        n, hospital_prefs, student_prefs = parse_preferences(pref_file)
    except Exception as e:
        return f"INVALID: Error parsing preferences - {e}", False, False
    
    try:
        matching = parse_matching(matching_file)
    except Exception as e:
        return f"INVALID: Error parsing matching - {e}", False, False
    
    # Check validity
    is_valid, validity_error = check_validity(n, matching)
    if not is_valid:
        return f"INVALID: {validity_error}", False, False
    
    # Check stability
    is_stable, blocking_pair = check_stability(n, matching, hospital_prefs, student_prefs)
    if not is_stable:
        h, s = blocking_pair
        return f"UNSTABLE: Blocking pair found - Hospital {h} and Student {s}", True, False
    
    return "VALID STABLE", True, True


def main():
    if len(sys.argv) != 3:
        print("Usage: python verifier.py <preferences_file> <matching_file>")
        print("  preferences_file: Input file with n, hospital prefs, student prefs")
        print("  matching_file: Output file with hospital-student pairs")
        sys.exit(1)
    
    pref_file = sys.argv[1]
    matching_file = sys.argv[2]
    
    result, is_valid, is_stable = verify(pref_file, matching_file)
    print(result)
    
    # Exit code: 0 if valid and stable, 1 otherwise
    sys.exit(0 if (is_valid and is_stable) else 1)


if __name__ == "__main__":
    main()