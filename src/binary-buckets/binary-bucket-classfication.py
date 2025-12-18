import re
import pprint
from typing import Set, Dict, List


"""
For the binary bucket testing, VLM analyzes the video and gives the output in the form of:
    - Individual OR group: Individual
    - Aggressive OR not aggressive: Not aggressive

    or simply:
    - Individual
    - Not aggressive

This function parses the log file and returns the dictionary in the form of:
    {
        "scene_001.mp4" : [
            "individual",
            "Aggressive",
        ],
        "scene_002.mp4" : [
            "group",
            "not aggressive",
        ],
    }
"""
def process_scene_logs(filepath: str) -> Dict[str, List[str]]:
    """
    Parses a log file from the given path, maps scene filenames to their
    categories, and validates those categories against an internal master list.

    This version handles formats with a "Categories:" header AND formats
    where categories are listed directly after "text=".

    Args:
        filepath: The path to the log file to be processed.

    Returns:
        A dictionary where keys are filenames (e.g., "scene_004.mp4")
        and values are a list of *validated* string categories.
    """

    # --- 1. Master Category List ---
    # Define all valid category options here.
    VALID_CATEGORIES = [
            "Individual", "Group",
            "Aggressive", "Not aggressive",
            "High energy", "Low energy",
            "Object", "No object",
            "Adult", "Child",
            "Feeding", "Not feeding"
            # Add future categories here, e.g., "Indoor", "Outdoor"
            ]

    # Create a lowercase set for efficient, case-insensitive lookup
    valid_categories_set: Set[str] = {c.lower() for c in VALID_CATEGORIES}

    # --- 2. Parsing Logic ---
    results: Dict[str, List[str]] = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return {}
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        return {}

    # Split the entire file content into individual entries
    entries = content.split('------------------------')

    # Regex to find the filename
    filename_regex = re.compile(r"Output for .*/(scene_[\d_]+\.mp4):")

    # Regex to find a bolded value (e.g., **Individual**)
    bold_value_regex = re.compile(r"\*\*(.*?)\*\*")

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        # 1. Find the filename
        filename_match = filename_regex.search(entry)
        if not filename_match:
            continue  # Skip entries without a valid filename

        filename = filename_match.group(1)

        # 2. Find the block of text containing categories
        categories_block = ""
        categories_start = entry.find("Categories:")

        # --- MODIFIED LOGIC ---
        if categories_start != -1:
            # Case 1: "Categories:" header exists (Old format)
            start_index = categories_start
            categories_end = entry.find("generate_token_len=", start_index)

            if categories_end == -1:
                categories_block = entry[start_index:]
            else:
                categories_block = entry[start_index:categories_end]
        else:
            # Case 2: No "Categories:" header. (New format)
            # Use the "text=" block as the source.
            text_start = entry.find("text=")
            if text_start != -1:
                start_index = text_start + 5  # Move past "text="
                categories_end = entry.find("generate_token_len=", start_index)

                if categories_end == -1:
                    categories_block = entry[start_index:]
                else:
                    categories_block = entry[start_index:categories_end]
            else:
                # No "Categories:" and no "text=", so no data
                results[filename] = []
                continue
        # --- END MODIFIED LOGIC ---

        if not categories_block.strip():
            results[filename] = []
            continue

        # 3. Extract each category from the block
        categories_list: List[str] = []
        for line in categories_block.splitlines():
            line = line.strip()
            if not line: # Skip empty lines
                continue

            # --- MODIFIED LOGIC ---
            # Strip leading hyphen or space, then strip whitespace again.
            # This handles "- Individual" and "Individual"
            clean_line = line.lstrip(" -").strip()
            # --- END MODIFIED LOGIC ---

            category = ""

            if ":" in clean_line:
                # Complex format (e.g., "Key: Value" or "Caption: ...")
                try:
                    key, value = clean_line.split(":", 1)
                    value = value.strip()

                    bold_match = bold_value_regex.search(value)
                    if bold_match:
                        category = bold_match.group(1).strip()
                    else:
                        category = value.split("(", 1)[0].strip()

                except ValueError:
                    # This filters out "text=- Caption" lines
                    continue
            else:
                # Simple format (e.g., "Individual" or "Not aggressive")
                category = clean_line

            # 4. VALIDATION STEP:
            if category and category.lower() in valid_categories_set:
                categories_list.append(category)
            # else:
            #    The category is discarded (e.g., "Caption" is ignored)

        results[filename] = categories_list

    return results

def compare_accuracies(ground_truth: Dict[str, List[str]],
                       model_output: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Compares two dictionaries of scene categories to calculate
    per-category-pair accuracy.

    Args:
        ground_truth: The dictionary of correct answers.
        model_output: The dictionary of answers to be tested.

    Returns:
        A dictionary reporting the accuracy for each category pair.
    """

    # --- 1. Define the Semantic Category Pairs ---
    # This is the "brain" of the comparison. It groups opposing
    # categories. All strings are lowercase for comparison.
    CATEGORY_PAIRS = {
        "Group Size (Individual/Group)": {"individual", "group"},
        "Aggression (Aggressive/Not aggressive)": {"aggressive", "not aggressive"},
        "Energy (High energy/Low energy)": {"high energy", "low energy"},
        "Object (Object/No object)": {"object", "no object"},
        "Age (Adult/Child)": {"adult", "child"},
        "Activity (Feeding/Not feeding)": {"feeding", "not feeding"}
        # Add future pairs here, e.g.:
        # "Location (Indoor/Outdoor)": {"indoor", "outdoor"}
    }

    # Initialize a dictionary to store stats (correct, total_comparisons)
    stats = {group_name: {"correct": 0, "total": 0}
             for group_name in CATEGORY_PAIRS}

    # --- 2. Compare Dictionaries ---

    # Loop over every scene in the ground truth
    for scene, gt_list in ground_truth.items():

        # Only compare scenes that are also in the model's output
        if scene not in model_output:
            continue

        model_list = model_output[scene]

        # Convert lists to lowercase sets for easy and fast lookup
        gt_set = {category.lower() for category in gt_list}
        model_set = {category.lower() for category in model_list}

        # Now, check each semantic category pair
        for group_name, group_options in CATEGORY_PAIRS.items():

            # Find the answer from each set for this specific group
            gt_answer_for_group = gt_set.intersection(group_options)
            model_answer_for_group = model_set.intersection(group_options)

            # We can only make a comparison if *both* dicts provided
            # exactly one valid answer for this group.
            if len(gt_answer_for_group) == 1 and len(model_answer_for_group) == 1:

                # A comparison is possible
                stats[group_name]["total"] += 1

                # Extract the single answer from each set
                gt_answer = list(gt_answer_for_group)[0]
                model_answer = list(model_answer_for_group)[0]

                # Check if they match
                if gt_answer == model_answer:
                    stats[group_name]["correct"] += 1

    # --- 3. Format the Final Report ---
    accuracies = {}
    for group_name, data in stats.items():
        if data["total"] > 0:
            acc = (data["correct"] / data["total"]) * 100
            # Format: "90.00% (9/10)"
            accuracies[group_name] = f"{acc:.2f}% ({data['correct']}/{data['total']})"
        else:
            # No comparisons were possible for this group
            accuracies[group_name] = "N/A (0 comparisons)"

    return accuracies

path = "/home/park1361/verification-log-bb-bullet-points-guideline-20251112-094106.txt"  # soft guideline (bullet points)
#path = "/home/park1361/verification-log-bb-specific-example-20251112-093708.txt"  # one that gave specific example
path = "/home/park1361/verification-log-bb-no-guideline-20251106-154332.txt"   # no constrait
llm_ground_truth = process_scene_logs(path)

path = "/home/park1361/chimp-log-bb-bullet-points-guideline-20251112-094105.txt"
#path = "/home/park1361/chimp-log-bb-specific-example-20251112-093727.txt"
vlm_hypothesis = process_scene_logs(path)

print(compare_accuracies(llm_ground_truth, vlm_hypothesis))

