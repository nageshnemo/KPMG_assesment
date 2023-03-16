"""
aws-metadata-json
What it does
Query the metadata of an ec2 instance within AWS and provide a json formatted output.
Retrieve the value of a particular data key.

  Create an EC2 Linux instance on AWS
SSH into the instance
Install Python 3 and git on your instance
sudo yum install python3 git
Clone this repository
git clone this repo
Install pipenv
sudo pip3 install pipenv
Open the repository on your instance
cd aws-metadata-json
Install project dependancies
pipenv install
    How to run
Open the src folder
cd aws-metadata-json/src
Run whichever script you need:
python3 get_metadata.py

"""







import requests
import json

metadata_url = 'http://169.254.169.254/latest/'


def expand_tree(url, arr):
    output = {}
    for item in arr:
        new_url = url + item
        r = requests.get(new_url)
        text = r.text
        if item[-1] == "/":
            list_of_values = r.text.splitlines()
            output[item[:-1]] = expand_tree(new_url, list_of_values)
        elif is_json(text):
            output[item] = json.loads(text)
        else:
            output[item] = text
    return output


def get_metadata():
    initial = ["meta-data/"]
    result = expand_tree(metadata_url, initial)
    return result


def get_metadata_json():
    metadata = get_metadata()
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    return metadata_json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    print(get_metadata_json())
    
    
    
