import json


# Save Status
def save_status(savefile):
    with open("status.json", "w") as fp:
        json.dump(savefile, fp, indent=4)
