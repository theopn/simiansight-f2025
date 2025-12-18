import re
import sys

def parse_log_evaluation(log_file_path): # Renamed function
    """
    Parses a log file to find "Yes" or "No" evaluations and calculates
    the accuracy (percentage of "Yes" answers).

    Args:
        log_file_path (str): The path to the log file.
    """
    total_evaluations = 0 # Renamed
    yes_count = 0         # Renamed

    # Regex to find "text=..." and then capture "Yes" or "No" on the same line.
    # [^\n]* matches any character except a newline, finding the last "Yes" or "No"
    # on the same line as "text=". Case-insensitive.
    evaluation_pattern = re.compile(r"text=[^\n]*(Yes|No)\b", re.IGNORECASE)

    try:
        with open(log_file_path, 'r') as f:
            content = f.read()

        # Split the entire log file into individual entries
        # The delimiter is '------------------------'
        log_entries = content.split('------------------------')

        print(f"--- Evaluation Analysis for {log_file_path} ---")

        for i, entry in enumerate(log_entries):
            entry_text = entry.strip()
            if not entry_text:  # Skip empty blocks (e.g., from the start/end)
                continue

            # Search for the evaluation pattern in the current entry
            evaluation_match = evaluation_pattern.search(entry_text)

            # Ensure an evaluation was found
            if evaluation_match:
                total_evaluations += 1
                try:
                    # Extract the captured group ("Yes" or "No")
                    result = evaluation_match.group(1).lower()

                    is_correct_str = "No"
                    # Check if the result is "yes"
                    if result == "yes":
                        yes_count += 1
                        is_correct_str = "Yes"

                    print(f"Entry {total_evaluations}: Found evaluation -> {is_correct_str}")

                except Exception as e:
                    print(f"Warning: Could not parse evaluation in entry {total_evaluations}: {e}\nEntry:\n{entry_text[:200]}...")

            elif entry_text: # Avoid warning for empty blocks
                # This helps debug if the pattern isn't matching
                print(f"Warning: Entry {total_evaluations + 1} is invalid. Could not find evaluation pattern.")
                print(f"  Entry snippet:\n{entry_text[:200]}...\n")


        # Check if we found any entries
        if total_evaluations > 0:
            accuracy = (yes_count / total_evaluations) * 100

            print("\n--- Summary ---")
            print(f"Total valid entries found: {total_evaluations}")
            print(f"Total 'Yes' answers: {yes_count}")
            print(f"Accuracy: {accuracy:.2f}% ({yes_count} / {total_evaluations})")
        else:
            print(f"No valid evaluations (Yes/No) were found in {log_file_path}.")

    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The script expects the log file name as an argument.
    # If no argument is given, it defaults to 'evaluation.log'.
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = "evaluation.log" # Default to new log file name

    parse_log_evaluation(log_file) # Call renamed function


