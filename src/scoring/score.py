import re
import sys

def parse_log_scores(log_file_path):
    """
    Parses a log file to extract scores and calculate the average.

    Args:
        log_file_path (str): The path to the log file.
    """
    scores = []

    # Regular expression to find "Score: N/10" and capture N
    # This pattern looks for the literal string "Score: ",
    # captures one or more digits (\d+), and then looks for "/10"
    score_pattern = re.compile(r"[Score|Evaluation]: (\d+)/10")

    try:
        with open(log_file_path, 'r') as f:
            content = f.read()

            # Find all matches of the pattern in the file content
            found_scores = score_pattern.findall(content)

            # Convert found scores (which are strings) to integers
            scores = [int(score) for score in found_scores]

        # Check if we found any scores
        if scores:
            average_score = sum(scores) / len(scores)

            print(f"--- Score Analysis for {log_file_path} ---")
            print(f"\nFound scores: {scores}")
            print(f"Total scores found: {len(scores)}")
            print(f"Average score: {average_score:.2f} / 10")
        else:
            print(f"No scores matching the 'Score: N/10' format were found in {log_file_path}.")

    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The script expects the log file name as an argument.
    # If no argument is given, it defaults to 'scores.log'.
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = "scores.log"

    parse_log_scores(log_file)

