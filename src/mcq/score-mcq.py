import re
import sys

def parse_log_accuracy(log_file_path):
    """
    Parses a log file to extract correct choices and program choices,
    compares them, and calculates the accuracy.

    Args:
        log_file_path (str): The path to the log file.
    """
    total_entries = 0
    correct_matches = 0

    # Regex to find the correct answer number
    correct_pattern = re.compile(r"Correct: (\d+)")

    # Regex to find the program's answer number (from the 'text=' line)
    program_choice_pattern = re.compile(r"text=(\d+)\.")

    try:
        with open(log_file_path, 'r') as f:
            content = f.read()

        # Split the entire log file into individual entries
        # The delimiter is '------------------------'
        log_entries = content.split('------------------------')

        print(f"--- Accuracy Analysis for {log_file_path} ---")

        for i, entry in enumerate(log_entries):
            entry_text = entry.strip()
            if not entry_text:  # Skip empty blocks (e.g., from the start/end)
                continue

            # Search for both patterns in the current entry
            correct_match = correct_pattern.search(entry_text)
            program_choice_match = program_choice_pattern.search(entry_text)

            # Ensure both the correct answer and the program's choice were found
            if correct_match and program_choice_match:
                total_entries += 1
                try:
                    # Extract the captured numbers (as strings)
                    correct_choice = correct_match.group(1)
                    program_choice = program_choice_match.group(1)

                    is_correct = "No"
                    # Compare the choices
                    if correct_choice == program_choice:
                        correct_matches += 1
                        is_correct = "Yes"

                    print(f"Entry {total_entries}: Correct={correct_choice}, Program={program_choice} -> Match: {is_correct}")

                except Exception as e:
                    print(f"Warning: Could not parse choices in entry {total_entries}: {e}\nEntry:\n{entry_text[:200]}...")

            elif entry_text: # Avoid warning for empty blocks
                # This helps debug if one of the patterns isn't matching
                print(f"Warning: Entry {total_entries + 1} is invalid. Could not find both patterns.")
                print(f"  Found 'Correct:': {'Yes' if correct_match else 'No'}")
                print(f"  Found 'text=...': {'Yes' if program_choice_match else 'No'}")
                print(f"  Entry snippet:\n{entry_text[:200]}...\n")


        # Check if we found any entries
        if total_entries > 0:
            accuracy = (correct_matches / total_entries) * 100

            print("\n--- Summary ---")
            print(f"Total valid entries found: {total_entries}")
            print(f"Correct matches: {correct_matches}")
            print(f"Accuracy: {accuracy:.2f}% ({correct_matches} / {total_entries})")
        else:
            print(f"No valid log entries were found in {log_file_path}.")

    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The script expects the log file name as an argument.
    # If no argument is given, it defaults to 'accuracy.log'.
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = "accuracy.log" # Default to new log file name

    parse_log_accuracy(log_file)


