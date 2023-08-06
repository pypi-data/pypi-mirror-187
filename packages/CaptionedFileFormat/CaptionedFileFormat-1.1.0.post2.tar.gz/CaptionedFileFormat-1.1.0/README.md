# Captioned File

This is a Python wrapper for the CPTN (CaPTioNed file) file format. For more info about the format  check <https://github.com/Oakchris1955/Captioned-File>

## Usage

To write bytes:

```py
from cptf import Buffer

# Create a new bytes object
data = Buffer()
data.create_new("Some content...", "Caption 1234") 
# This will change the caption of our data to "Caption 1234" and the content "Some content..."

# Let's get the raw bytes now and write them to "test.cptn"
with open("test.cptn", "wb") as f:
    f.write(data.get_bytes())
```

To read bytes:

```py
from cptf import Buffer

# Create a new bytes object
data = Buffer()

# Read bytes from file and decode them
with open("test.cptn", "rb") as f:
    # Note: read_from_bytes also outputs a dictionary contaning the caption, the content and the filename. However, it still writes those data to the Buffer object
    
    data.read_from_bytes(f.read()) # The function can take one optional argument, get_header which is a bool. If this is supplied and is True, the result dictionary will also include the caption, filename and content text size in bytes (although you could also use a len())

print(f"Filename: {data.filename}, Caption: {data.caption}, Content: {data.content}")
```
