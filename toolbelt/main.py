import pathchanger, capitalize, papagaaienwerk, zaklamp, folder_maker
import sys, json


with open("toolbelt setup.json") as setupFile:
    setup = json.load(setupFile)
name = setup["name"]
# welcome menu
print("                .__                               \n",
"__  _  __ ____ |  |   ____  ____   _____   ____  \n",
"\ \/ \/ // __ \|  | _/ ___\/  _ \ /     \_/ __ \ \n",
" \     /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ \n",
"  \/\_/  \___  >____/\___  >____/|__|_|  /\___  >\n",
"             \/          \/            \/     \/ \n",
"\n",
"___________________   ________  .____   _____________________.____  ___________\n",
"\__    ___/\_____  \  \_____  \ |    |  \______   \_   _____/|    | \__    ___/\n",
"  |    |    /   |   \  /   |   \|    |   |    |  _/|    __)_ |    |   |    |   \n",
"  |    |   /    |    \/    |    \    |___|    |   \|        \|    |___|    |   \n",
"  |____|   \_______  /\_______  /_______ \______  /_______  /|_______ \____|   \n",
"                   \/         \/        \/      \/        \/         \/        \n\n",
"#" * 60,
"\n hello %s\n" % name,
"#" * 60)
callNumbers = [1,2,3,4,5]
callPrograms = [pathchanger, capitalize, papagaaienwerk, zaklamp, folder_maker]
while True:
    print("-" * 60)
    print("\n\n1. pathchanger\n2. capitalizer\n3. papagaaienwerk\n4. zaklamp\n5. folder maker")
    prompt = input(">>> ")
    if prompt == "<<<" or prompt.lower() == "exit":
        sys.exit()
    try:
        prompt = int(prompt)
    except ValueError:
        continue
    if prompt not in callNumbers:
        continue
    callPrograms[prompt - 1].run()
    
        
    

