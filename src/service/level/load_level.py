import os
import json

def load_level_from_json(directory="./levels/data"):
    """"""
    
    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    if not json_files:
        print("No JSON files found in the directory.")
        return None
    
    # Display the menu
    print("""\n
                                                                        =                          
                                                                        **                          
                                                                         +                          
                                                                         =+                         
                                                                         :*                   +     
  +++============-----:::::::::::::::::.::::::::::::::::::::::::::::....-=-@@@%%@%%%+#*####*+==##   
 ++++++++++++===========================================================++*@@@@@@@@%******#*+*+##   
    @%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*+#%@   @@          % +     
                                                                        @*                          
                                                                         =                          
                                                                         *                          
                                                                         +                          
    WELCOME TO THE DUNGEONS OF AJENTIA | SELECT A LEVEL BELOW TO BEGIN!!!
    """)
    print("-" * 40)
    for i, filename in enumerate(json_files, 1):
        print(f"{i}. {filename}")
    print("-" * 40)
    
    # Get user selection
    while True:
        try:
            choice = input("\nEnter the number of the file to load (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                return None
            
            choice = int(choice)
            
            if 1 <= choice <= len(json_files):
                selected_file = json_files[choice - 1]
                filepath = os.path.join(directory, selected_file)
                
                # Load and return the JSON data
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                print(f"\n✓ Loaded: {selected_file}")
                return data
            else:
                print(f"Please enter a number between 1 and {len(json_files)}")
        
        except ValueError as e:
            raise e
            print("Invalid input. Please enter a number.")
        except json.JSONDecodeError:
            print(f"Error: {selected_file} is not a valid JSON file.")
        except Exception as e:
            print(f"Error loading file: {e}")
