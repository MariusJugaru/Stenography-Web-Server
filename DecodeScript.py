from PIL import Image

def decode(imgName):
    image = Image.open("Uploads/" + imgName, 'r')

    Message = ''
    imgMessage = list(image.getdata())
    
    i = 0
    while (True):
        pixGroup = imgMessage[i * 3: i * 3 + 3]
        pixList = [item for t in pixGroup for item in t]

        # string binar
        binstr = ''

        for j in pixList[:8]:
            if (j % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
		
        Message += chr(int(binstr, 2))
        i = i + 1
        if (pixList[8] % 2 != 0):
            return Message