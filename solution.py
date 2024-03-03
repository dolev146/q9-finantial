from typing import List, Set, Optional, Tuple

def calculate_total_budget_and_share(budget: List[float], n: int) -> Tuple[float, float]:
    total_budget = sum(budget)
    share_per_citizen = total_budget / n if n else 0
    return total_budget, share_per_citizen

def find_interested_citizens(preferences: List[Set[int]], subject_index: int, n: int) -> List[int]:
    return [i for i in range(n) if subject_index in preferences[i]]

def allocate_budget_for_subject(budget: List[float], preferences: List[Set[int]], subject_index: int, share_per_citizen: float, decomposition: List[List[float]]) -> bool:
    """
    Allocates budget for a specific subject across interested citizens based on their preferences.

    Parameters:
    - budget: A list where each element represents the budget for a specific subject.
    - preferences: A list of sets, where each set contains subject indices that a citizen is interested in.
    - subject_index: The index of the subject for which the budget is being allocated.
    - share_per_citizen: The maximum amount of budget that can be allocated to a single citizen.
    - decomposition: A matrix (list of lists) where each element represents the amount of budget
                     allocated to a citizen for each subject.

    Returns:
    - True if the budget for the subject could be allocated successfully, False otherwise.
    """
    subject_budget = budget[subject_index]
    interested_citizens = find_interested_citizens(preferences, subject_index, len(preferences))

    if not interested_citizens and subject_budget > 0:
        # If no one is interested in the subject with a non-zero budget, cannot allocate.
        return False

    total_possible_share = sum(share_per_citizen - sum(decomposition[i]) for i in interested_citizens)
    if total_possible_share < subject_budget:
        # If the total possible share is less than the subject's budget, allocation is impossible.
        return False

    for i in interested_citizens:
        if subject_budget <= 0:
            break

        max_possible_allocation = share_per_citizen - sum(decomposition[i])
        possible_allocation = min(max_possible_allocation, subject_budget)
        decomposition[i][subject_index] += possible_allocation
        subject_budget -= possible_allocation

    return True

def verify_allocation(decomposition: List[List[float]], share_per_citizen: float) -> bool:
    return all(abs(sum(allocation) - share_per_citizen) < 1e-9 for allocation in decomposition)

def is_basic_case_func(budget: List[float], preferences: List[Set[int]]):
    """Determines if the budget allocation scenario represents a basic case.

    A basic case has these conditions:
        * Each citizen prefers a unique subject.
        * The total budget is sufficient to cover all citizen preferences.
    """
    num_subjects = len(budget)
    subjects_interested_count = [0] * num_subjects

    # Track interest in each subject
    for citizen_preferences in preferences:
        for preferred_subject in citizen_preferences:
            subjects_interested_count[preferred_subject] += 1

    # Check conditions for basic case
    has_unique_preferences = all(count == 1 for count in subjects_interested_count)
    has_sufficient_budget = sum(budget) >= len(preferences)

    return has_unique_preferences and has_sufficient_budget

def calc_decomposition_for_basic_case(budget: List[float], preferences: List[Set[int]]):
    """Constructs the decomposition directly for a basic case."""
    num_citizens = len(preferences)
    decomposition = [[0 for _ in range(len(budget))] for _ in range(num_citizens)]

    for citizen_index, citizen_preferences in enumerate(preferences):
        preferred_subject = next(iter(citizen_preferences))  # Get the one preferred subject
        decomposition[citizen_index][preferred_subject] = budget[preferred_subject]

    return decomposition

def check_if_no_pref_then_return_None(preferences: List[Set[int]]) -> bool:
    """
    Checks if any of the citizens have no preferences.
    
    Returns True if at least one citizen has no preferences, otherwise False.
    """
    return any(len(pref) == 0 for pref in preferences)



def find_decomposition(budget: List[float], preferences: List[Set[int]]) -> Optional[List[List[float]]]:
    # Check if any citizen has no preferences. If so, return None.
    if check_if_no_pref_then_return_None(preferences):
        return None

    basic_case = False

    # add a function to handle the case where each citizen prefer different, the basic case test_basic_scenario
    basic_case = is_basic_case_func(budget, preferences)
    if basic_case:
      return calc_decomposition_for_basic_case(budget, preferences)
    else:
      n = len(preferences)
      total_budget, share_per_citizen = calculate_total_budget_and_share(budget, n)
      decomposition = [[0 for _ in range(len(budget))] for _ in range(n)]

      for j in range(len(budget)):
          if not allocate_budget_for_subject(budget, preferences, j, share_per_citizen, decomposition):
              return None  # Adjusted to handle insufficient budget correctly.

      if not verify_allocation(decomposition, share_per_citizen):
          return None  # Ensure verification step is correctly applied.

      return decomposition

# Running the code
budget = [400, 50, 50, 0]
preferences = [{0,1}, {0,2}, {0,3}, {1,2}, {0}]
decomposition = find_decomposition(budget, preferences)

if decomposition is not None:
    print("The budget is decomposable. One possible decomposition is:")
    for i, alloc in enumerate(decomposition):
        print(f"Citizen {i+1}'s allocation: {alloc}")
else:
    print("The budget is not decomposable.")
