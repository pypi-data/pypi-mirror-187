from . import errors
import typing
import struct

class FileBuffer:
	MAGIC_NUMBER = b'CPTN\n'

	def create_new(self, content: str, caption: str, filename: typing.Optional[str]):
		'''Fill the FileBUffer with some'''
		if filename is None:
			filename = ''
		filename_size = len(filename)
		caption_size = len(caption)

		self.filename_size = filename_size
		self.caption_size = caption_size

		self.filename = filename
		self.caption = caption
		self.content = content

		if filename_size >= 2**8:
			raise errors.SizeOverflow(f"Filename size must be under {2**8} bytes")
		if caption_size >= 2**16:
			raise errors.SizeOverflow(f"Caption size must be less than {2**16} bytes")

		header = bytes()
		header += struct.pack('>5s', self.MAGIC_NUMBER)
		header += struct.pack('>B', filename_size)
		header += struct.pack('>H', caption_size)
		self.header = header

	def read_from_bytes(self, buffer: bytes, get_header: typing.Optional[bool] = False):
		magic_number = struct.unpack(">5s", buffer[:5])[0]
		if magic_number != self.MAGIC_NUMBER:
			raise errors.NoMagicNumber("Expected magic number 0x4350544E0A in the beginning of the buffer provided")
		
		filename_size, caption_size = struct.unpack(">BH", buffer[5:8])

		filename, caption, content = struct.unpack(f"{filename_size}s {caption_size}s {len(buffer)-8-filename_size-caption_size}s", buffer[8:])

		output = {
			"body": {
				"filename": filename,
				"caption": caption,
				"content": content
			}
		}

		self.header = buffer[:8]

		self.filename_size = filename_size
		self.caption_size = caption_size

		self.filename = filename
		self.caption = caption
		self.content = content

		if get_header:
			output["header"] = {
				 "filename_size": filename_size,
				 "caption_size": caption_size
			}
		
		return output

	def get_bytes(self) -> bytes:
		'''Get bytes object to be written to file'''
		return self.header+b''.join(
			data.encode("UTF-8") for data in (self.filename, self.caption, self.content)
		)