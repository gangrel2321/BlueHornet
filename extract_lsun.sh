echo "Obtaining $1.zip..."
wget "dl.yf.io/lsun/objects/$1.zip" 
tar -xvf "$1.zip"
python3 data.py export $1 --out_dir data
mogrify -format JPEG -path data '*.webp'

