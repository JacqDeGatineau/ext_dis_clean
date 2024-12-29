if duplicates:
    with open(output_file, "w") as file:
        print(f"{len(duplicates)} duplicates found")
        file.write(f"Found {len(duplicates)} duplicate files: \n\n")
        for duplicate in duplicates:
            print(f"File: {duplicate[0]}\nDuplicate: {duplicate[1]}")
            file.write(f"File: {duplicate[0]}\nDuplicate: {duplicate[1]}\n\n")
    remove_duplicates(to_remove)