import sys
import time
import os
from skip_list import SkipList

# ANSI Colors
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_skip_list(sl, current_node=None, found=False):
    if not sl.root:
        print("Empty Skip List")
        return

    # Traverse to the bottom-most list to find all unique column values
    bottom = sl.root
    while bottom.bottom:
        bottom = bottom.bottom

    columns = []
    curr = bottom
    while curr:
        columns.append(curr.data)
        curr = curr.next

    # Calculate required display width for each column (content length + padding)
    col_widths = {val: len(str(val)) + 4 for val in columns}

    print("-" * 50)
    # Start drawing from the top-most level
    curr_row = sl.root
    level = sl.height

    while curr_row:
        # Print level label
        print(f"L{level:<2} ", end="")
        
        curr_node = curr_row
        
        for val in columns:
            width = col_widths[val]
            if curr_node and curr_node.data == val:
                # Node exists in this column at this level
                is_highlighted = (current_node is not None and curr_node == current_node)
                
                color = RESET
                if is_highlighted:
                    color = GREEN if found else YELLOW
                
                val_str = f"[{color}{curr_node.data}{RESET}]"
                
                # Visual length adjustment because ANSI codes add hidden characters
                visible_len = len(str(curr_node.data)) + 2
                dash_count = width - visible_len
                print(val_str + "-" * dash_count, end="")
                curr_node = curr_node.next
            else:
                # No node in this column, draw the passing link
                print("-" * width, end="")
        print() # Newline for the next level
        
        curr_row = curr_row.bottom
        level -= 1
    print("-" * 50)

def simulate_search(sl, data):
    if not sl.root:
        print("Empty Skip List")
        return

    cur = sl.root
    
    while cur:
        clear_screen()
        print(f"Searching for '{data}'...")
        draw_skip_list(sl, current_node=cur, found=False)
        time.sleep(0.5)

        while cur.next and cur.next.data < data:
            cur = cur.next
            clear_screen()
            print(f"Searching for '{data}'...")
            draw_skip_list(sl, current_node=cur, found=False)
            time.sleep(0.5)

        if cur.next and cur.next.data == data:
            # Found it!
            cur = cur.next
            clear_screen()
            print(f"Searching for '{data}'... {GREEN}Found!{RESET}")
            draw_skip_list(sl, current_node=cur, found=True)
            return

        cur = cur.bottom
        
    clear_screen()
    print(f"Searching for '{data}'... {RED}Not Found!{RESET}")
    draw_skip_list(sl, current_node=None, found=False)

def parse_value(v):
    try:
        # Try to parse as integer first
        return int(v)
    except ValueError:
        # Fallback to string
        return v

def print_help():
    print("Commands:")
    print("  insert <value>  (or i <value>)")
    print("  delete <value>  (or d <value>)")
    print("  search <value>  (or s <value>)")
    print("  quit            (or q)")

def main():
    sl = SkipList(maxLevels=5)
    
    clear_screen()
    print("Welcome to the Interactive Skip List!\n")
    print_help()
    print()
    draw_skip_list(sl)

    while True:
        try:
            user_input = input("\nEnter command: ").strip().split(maxsplit=1)
            if not user_input:
                continue
                
            cmd = user_input[0].lower()
            
            if cmd in ('quit', 'q', 'exit'):
                print("Exiting...")
                break
                
            if len(user_input) < 2:
                print("Error: Missing value. Please provide a value.")
                continue
                
            val = parse_value(user_input[1])
            
            if cmd in ('insert', 'i'):
                sl.insert(val)
                clear_screen()
                print(f"=> Inserted '{val}'\n")
                print_help()
                print()
                draw_skip_list(sl)
            elif cmd in ('delete', 'd'):
                sl.delete(val)
                clear_screen()
                print(f"=> Deleted '{val}'\n")
                print_help()
                print()
                draw_skip_list(sl)
            elif cmd in ('search', 's'):
                simulate_search(sl, val)
                print()
                print_help()
            else:
                print(f"\nError: Unknown command '{cmd}'")
                continue
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError occurred: {e}")

if __name__ == "__main__":
    # For windows to enable ANSI escape colors
    if os.name == 'nt':
        os.system('color')
    main()
