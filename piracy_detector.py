#IMPORTS  
  
import torrent_parser as tp  
import hashlib  
from pathlib import Path  
import argparse  
from tqdm import tqdm  
  
#ARGUMENTS  
parser = argparse.ArgumentParser()  
parser.add_argument('torrent_file', type=str)  
parser.add_argument('base_path', type=str)  
  
#Two Arguments   
 1) Torrent file  
 2) Folder containing the files on disk  

args = parser.parse_args()  
torrentfile = tp.parse_torrent_file(args.torrent_file)  
  
piecelength = torrentfile["info"]["piece length"]  
hashes = torrentfile["info"]["pieces"]  
files = torrentfile["info"]["files"]  
  
remaining_bytes = b""  
counter = 0  
hash_index = 0  
  
for f in tqdm(files):  
    path = Path(args.base_path).joinpath(*f["path"])      
    file = open(str(path), 'rb')  
    bytes_read = file.read()  
    bytes_read = remaining_bytes + bytes_read  
      
    #Checking Hash  
      
    for i in tqdm(range (len(bytes_read)//piecelength)):  
        block=bytes_read[piecelength*i:piecelength*(i+1)]      
        hash = hashlib.sha1()  
        hash.update(block)  
        counter+=1 if hash.hexdigest()==hashes[hash_index] else 0  
        hash_index+=1    
    remaining_bytes = bytes_read[piecelength * (len(bytes_read) // piecelength):]  
  
if remaining_bytes!=b"":  
    hash = hashlib.sha1()  
    hash.update(remaining_bytes)  
    counter+=1 if hash.hexdigest()==hashes[-1] else 0  
