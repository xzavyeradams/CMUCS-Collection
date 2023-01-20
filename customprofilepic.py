# https://replit.com/@xzavyeratschool/CMU-Profile-Picture-Changer#main.py
# This isn't from the sandbox, but you can actually set your profile picture to any 400x400 image. It's dated when I made it.

# Xzavyer Adams
# 3/18/22
import os
import requests
from io import BytesIO
from PIL import Image
from base64 import b64encode
from colorama import init, Fore, Style
init()


size = os.get_terminal_size().columns
print(Fore.WHITE + Style.BRIGHT)
print(Fore.MAGENTA + "Xzavyer's CMU PFP Changer Tool".center(size))

session = requests.Session()

# prompt 1
while True:
  choice = input(Fore.WHITE + "Do you know how to obtain your CMU auth. token? [y/n]: ")
  if choice in ['n', 'N', 'no']:
    print("Step 1: Log into CMU.\nStep 2: Press CTRL+SHIFT+I\nStep 3: Go to the 'Application' tab\n* If you do not see this, drag the inpect menu's left side to the left.\nStep 4: Click 'Local Storage' under the 'Storage' section\nStep 5: Click on the box that appeared with the CMU url in it.\nStep 6: Copy the string of letters and numbers in the big box at the bottom.\n* MAKE SURE THE TOP BOX THAT IS HIGHLIGHTED IS 'cs-academy-token' AND NOT SOMETHING ELSE!\n")
    print(Fore.RED + "**DO NOT SHARE THIS TOKEN! IT COULD GIVE MALICIOUS PEOPLE ACCESS TO YOUR ACC.**" + Fore.WHITE)
    print("This program is open-sourced for your safety, and trust.")
    break
  elif choice in ['y', 'Y', 'yes']:
    break
  else:
    print(Fore.RED + "Please enter a valid option (y/n)")


token = "Token " + input("Token: ")

# image prompt, converts image data to base64 for processing
print("(You can find an image's URL by right clicking & pressing 'Copy Image Address')")
while True:
  imageUrl = input(Fore.WHITE + "Image URL: ")
  if "https://" not in imageUrl:
    print(Fore.RED + "That is not a valid link!")
  elif ".jpg" not in imageUrl:
    print(Fore.RED + "Please ensure you're using a DIRECT LINK to the image, or make sure the image is a .jpg")
  else:
    # image processing
    print("Downloading image...")
    data = session.get(imageUrl).content
    encode = b64encode(data)
    dimensions = Image.open(BytesIO(data))
    h, w = dimensions.size
    if h != 400 or w != 400:
      print(Fore.RED + f'Your image MUST be 400x400px. Your image was {h}x{w}px.')
    else:
      break


print("Setting your PFP...")
res = session.post("https://backend.academy.cs.cmu.edu/api/v0/users/avatar/", json={"image": encode.decode('ascii')}, headers={"authorization": token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"})

if res.status_code == 200:
  print(Fore.GREEN + "Success!")
elif res.status_code == 401 or res.status_code == 403:
  print(Fore.RED + "Authentication Err! (Is your token correct?)")
else:
  print(Fore.RED + f"Oh no! {res.status_code}")
