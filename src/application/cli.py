import argparse
import os

from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(
        description="Process input files using ReadManager, SplitManager, and \
            ChunkManager to produce chunks."
    )
    parser.add_argument(
        "config_file",
        nargs="?",
        default="src/config.yaml",
        help="Path to the YAML configuration file (default: src/config.yaml)",
    )
    args = parser.parse_args()

    # Use the current working directory to resolve relative paths.
    cwd = os.getcwd()

    # --- Step 1: Initialize ReadManager ---
    from src.reader.read_manager import ReadManager

    read_manager = ReadManager(config_path=args.config_file)
    config = read_manager.config
    input_path = config.get("file_io", {}).get("input_path", "data/input")
    if not os.path.isabs(input_path):
        input_path = os.path.join(cwd, input_path)

    try:
        files = os.listdir(input_path)
    except FileNotFoundError:
        print(f"Input directory not found: {input_path}")
        return

    if not files:
        print(f"No files found in input directory: {input_path}")
        return

    # --- Initialize SplitManager and ChunkManager ---
    from src.splitter.split_manager import SplitManager

    splitter_manager = SplitManager(config_path=args.config_file)
    from src.chunker.chunk_manager import ChunkManager

    chunk_manager = ChunkManager(config_path=args.config_file)

    # Get the splitter method from the configuration.
    splitter_method = config.get("splitter", {}).get("method", "unknown")

    # Process each file with a tqdm progress bar.
    for file in tqdm(files, desc="Processing files", unit="file"):
        input_file = os.path.join(input_path, file)
        if not os.path.isfile(input_file):
            continue

        print(f"\nProcessing file: {input_file}")
        try:
            # read_file expects just the filename relative to the input
            # directory.
            markdown_text = read_manager.read_file(os.path.basename(input_file))
        except Exception as e:
            print(f"Error reading file {input_file}: {e}")
            continue

        # --- Step 2: Split the Markdown text ---
        chunks = splitter_manager.split_text(markdown_text)
        print(f"Generated {len(chunks)} chunks from the file.")

        # --- Step 3: Save the chunks in a dedicated folder ---
        basename = os.path.basename(input_file)
        base_filename, original_extension = os.path.splitext(basename)
        saved_files = chunk_manager.save_chunks(
            chunks, base_filename, original_extension, splitter_method
        )

        print("Chunks saved to:")
        for f in saved_files:
            print(f)


if __name__ == "__main__":
    main()
