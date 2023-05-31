import os, json, sys, shutil, urllib.request, re, argparse, random, string

colorama = None


parser = argparse.ArgumentParser(description="Converts .xnb files to .png files")
parser.add_argument("--nocolor", "--nocolour", action="store_true", help="Disables colorama")

args = parser.parse_args()


random_uid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def deps():
    global colorama
    try:
        import colorama as _colorama

        colorama = _colorama
        colorama.just_fix_windows_console()

    except ImportError:
        print("Installing colorama...")
        os.system("py -m pip install colorama")
        
        deps()

def colour(text, colour=None):
    if args.nocolor:
        return text
    

    if text.startswith("[INFO]"):
        info = f"[{colorama.Fore.BLUE}INFO{colorama.Fore.RESET}]"
        return info + text[6:]
    elif text.startswith("Success "):
        success = f"[{colorama.Fore.GREEN}Success{colorama.Fore.RESET}]"
        return success + text[7:]
    elif text.startswith("Fail "):
        fail = f"[{colorama.Fore.RED}Fail{colorama.Fore.RESET}]"
        return fail + text[4:]
    else:
        return colour + text + colorama.Fore.RESET



def folders():
    if os.path.exists("xnbcli"):
        shutil.rmtree("xnbcli")

    if os.path.exists("xnbcli.zip"):
        os.remove("xnbcli.zip")

    if not os.path.exists("unpacked_input"):
        os.makedirs("unpacked_input")
    else:
        shutil.rmtree("unpacked_input")
        os.makedirs("unpacked_input")
    
    if not os.path.exists("output"):
        os.makedirs("output")
    else:
        shutil.rmtree("output")
        os.makedirs("output")


def conv():

    input_files = os.listdir("input")
    
    if not len([x for x in input_files if x.endswith(".xnb")]) == 0:
        return print("Error: loose .xnb files found in input folder. Please sort them into folders as if in content first.")
    
    if os.name == "nt":
        #check if x64 or x86
        if sys.maxsize > 2**32:
            url = "https://github.com/LeonBlade/xnbcli/releases/download/v1.0.7/xnbcli-windows-x64.zip"
        else:
            url = "https://github.com/LeonBlade/xnbcli/releases/download/v1.0.7/xnbcli-windows-x86.zip"

    else:
        print("Non-windows is in progress")
        return
    
    print("Downloading xnbcli...")
    urllib.request.urlretrieve(url, "xnbcli.zip")
    
    print("Unpacking xnbcli...")
    shutil.unpack_archive("xnbcli.zip", "xnbcli")

    print("Converting files...")

    output = os.popen('"xnbcli/xnbcli.exe" unpack input unpacked_input')
    #get output while it's running
    while True:
        line = output.readline()
        if not line:
            break
        line = line.strip()
        
        valid_re_1 = re.compile(r"^\[INFO\] (Reading|Output|) file (.*)")
        valid_re_2 = re.compile(r"^(Success|Fail) \d+$")
        if valid_re_1.match(line) or valid_re_2.match(line):
            print(colour(line))

    print("")



    print(colour("Removing .json files...", colour=colorama.Fore.GREEN))
    for root, dirs, files in os.walk("unpacked_input"):
        for file in files:
            if file.endswith(".json"):
                #print("Removing " + file)
                os.remove(os.path.join(root, file))


    output_json = {
        "Format": "1.28.0",
        "Changes": []
    }

    for root, dirs, files in os.walk("unpacked_input"):
        for file in files:
            if file.endswith(".png"):
                path = os.path.join(root, file).replace("unpacked_input\\", "").replace("\\", "/")
                change = {
                    'Action': 'Load',
                    'Target': path,
                    'FromFile': 'assets/' + path
                }

                output_json["Changes"].append(change)


    print(colour("Writing content.json...", colour=colorama.Fore.GREEN))
    
    with open("output/content.json", "w") as f:
        json.dump(output_json, f, indent=4)

    print(colour("Writing manifest.json...", colour=colorama.Fore.GREEN))
    with open("output/manifest.json", "w") as f:
        json.dump({
            "Name": "Content Patcher Conversion",
            "Author": "Unspecified, converted by XNB2CP",
            "Version": "1.0.0",
            "Description": "A content pack for Stardew Valley.",
            "UniqueID": "XNB2CP_" + random_uid,
            "ContentPackFor": {
                "UniqueID": "Pathoschild.ContentPatcher"
            }
        }, f, indent=4)


    print(colour("Copying files...", colour=colorama.Fore.GREEN))
    shutil.copytree("unpacked_input", "output/assets")

    print(colour("Cleaning up...", colour=colorama.Fore.GREEN))
    shutil.rmtree("unpacked_input")
    shutil.rmtree("xnbcli")
    os.remove("xnbcli.zip")

    print(colour("Converted!", colour=colorama.Fore.GREEN))
    print(colour("Please change the manifest to reflect the original mod.", colour=colorama.Fore.GREEN))
    print(colour("Your mod can be found in the output folder.", colour=colorama.Fore.GREEN))


    




def main():
    deps()
    folders()
    conv()



if __name__ == "__main__":
    main()