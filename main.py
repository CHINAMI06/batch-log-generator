from config import OUTPUT_PATH
from generator import generate_batch_logs
from writer import write_csv


def main():
    logs = generate_batch_logs()
    write_csv(OUTPUT_PATH, logs)


if __name__ == "__main__":
    main()