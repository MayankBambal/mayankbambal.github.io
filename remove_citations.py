import re
import os
from pathlib import Path

def remove_citations_from_file(input_filepath, output_filepath):
    """
    Reads a markdown file, removes citation numbers in the format "non numeric text".1 ,
    and writes the cleaned content to a new file.

    The regex targets '1' when immediately preceded by a dot and followed by a space,
    ensuring it's a citation and not part of a version number.
    """
    # Regex to find citation numbers and remove only the "1" part
    # (?<![\d]) - negative lookbehind to ensure the character before the dot is not a digit
    # (?<=\.) - positive lookbehind to ensure there's a dot immediately before the "1"
    # 1 - matches the literal "1"
    # (?=\s) - positive lookahead to ensure there's a space after the "1"
    # This will match "text.1 " but avoid "1.1. " since it requires space after 1
    citation_regex = r'(?<![\d])(?<=\.)1(?=\s)'
    
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        cleaned_content = re.sub(citation_regex, '', content)
        
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(cleaned_content)
        
        print(f"Cleaned content written to {output_filepath}")
        
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except Exception as e:
        print(f"An error occurred processing {input_filepath}: {e}")

def remove_citations_from_folder(folder_path):
    """
    Process all files in a folder, removing citations and saving cleaned versions.
    """
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        print(f"Error: Folder not found at {folder_path}")
        return
    
    # Get all files in the folder (you can filter by extension if needed)
    files = [f for f in folder.iterdir() if f.is_file()]
    
    if not files:
        print(f"No files found in {folder_path}")
        return
    
    processed_count = 0
    citation_regex = r'(?<![\d])(?<=\.)1(?=\s)'
    
    for file_path in files:
        try:
            # Skip files that are already cleaned
            if "_cleaned" in file_path.stem:
                continue
                
            # Create output filename with "_cleaned" suffix
            output_name = f"{file_path.stem}_cleaned{file_path.suffix}"
            output_path = file_path.parent / output_name
            
            # Process the file
            remove_citations_from_file(file_path, output_path)
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nProcessed {processed_count} files in {folder_path}")
    print(f"Regex used: {citation_regex}")

if __name__ == '__main__':
    # Path to the folder containing files to process
    folder_to_process = '/Users/mayankbambal/Desktop/Job Search/portfolio/mayankbambal.github.io/super_sql_guide/level_2/Chapter1/'
    
    remove_citations_from_folder(folder_to_process) 