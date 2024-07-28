import io

def one():
    return open("seek_file.txt", "r+")

def two(file: io.TextIOWrapper) -> list:
    count = 0
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'the' in line:
            count += 1
            if count == 27:
                lines[i] = line.replace("the", "it")
                return lines
        

    

def main():
    try:
        file = one()
    except FileNotFoundError as e:
        print(e)
        return
    
    two(file)
    
    file.close()
    

if __name__ == "__main__":
    main()