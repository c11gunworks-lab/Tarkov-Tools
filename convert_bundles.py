import json
import sys

def parse_bundle_dependencies(input_filepath, output_filepath):
    manifest =[]
    current_bundle = None

    try:
        with open(input_filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # Clean leading and trailing whitespace
                stripped_line = line.strip()

                # 1. Check if the line defines a new Bundle
                if stripped_line.startswith('Bundle:'):
                    # Extract the full path after 'Bundle: ' and keep it as the key
                    bundle_key = stripped_line.split('Bundle:', 1)[1].strip()
                    
                    # Initialize the dictionary for this bundle
                    current_bundle = {
                        "key": bundle_key,
                        "dependencyKeys":[]
                    }
                    manifest.append(current_bundle)

                # 2. Check if the line is a dependency item
                # It will start with '-' and we must already be tracking a bundle
                elif stripped_line.startswith('-') and current_bundle is not None:
                    # Extract the string after the hyphen
                    dependency = stripped_line[1:].strip()
                    current_bundle["dependencyKeys"].append(dependency)
                    
                # Note: "Dependencies: None" is naturally ignored and leaves the list empty
                
    except FileNotFoundError:
        print(f"Error: Could not find '{input_filepath}'. Make sure the file is in the same directory.")
        sys.exit(1)

    # Wrap our list in the root "manifest" object
    output_data = {"manifest": manifest}

    # Write the formatted data to the output JSON file
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, indent=2)
        
    print(f"Success! Converted '{input_filepath}' to '{output_filepath}'.")
    print(f"Total bundles processed: {len(manifest)}")

if __name__ == "__main__":
    # Specify the input and output filenames
    input_file = "BundleDependencies.txt"
    output_file = "bundles.json"
    
    parse_bundle_dependencies(input_file, output_file)