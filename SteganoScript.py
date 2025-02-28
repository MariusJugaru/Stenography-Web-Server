from PIL import Image

def encPix(pix, message):
    binMessage = []
        
    for i in message:
        # Obtinem valoarea Ascii a caracterului pe care o transformam in format de 8 biti
        # apoi o anexam listei
        binMessage.append(format(ord(i), '08b')) 
                
    lenMessage = len(binMessage)
        
    for i in range(lenMessage):
        # Extragem cate 3 pixeli
        pixGroup = pix[i * 3: i * 3 + 3]
        pixList = [item for t in pixGroup for item in t]
                
        # Valoarea R, G, B din pixel devine impar pentru 1 si par pentru 0
        for j in range(0, 8):
            if (binMessage[i][j] == '0' and pixList[j] % 2 != 0):
                pixList[j] -= 1

            elif (binMessage[i][j] == '1' and pixList[j] % 2 == 0):
                if(pixList[j] != 0):
                    pixList[j] -= 1
                else:
                    pixList[j] += 1

        #Ultima valoare din set determina daca citirea continua
        # 0 - se citeste; 1 - se opreste
        if (i == lenMessage - 1):
            if (pixList[8] % 2 == 0):
                if(pixList[8] != 0):
                    pixList[8] -= 1
                else:
                    pixList[8] += 1
        else:
            if (pixList[8] % 2 != 0):
                pixList[8] -= 1
				
        pixList = tuple(pixList)
        yield pixList[0:3]
        yield pixList[3:6]
        yield pixList[6:9]

def encode():
    imgName = input("Nume imagine cu extensie: ")
    image = Image.open(imgName, 'r')

    message = input("Mesaj secret: ")
    newImg = image.copy()
	
    width, height = newImg.size
    (x, y) = (0, 0)
	
    for pixel in encPix(list(newImg.getdata()), message):
        # Se modifica pixelii din imagine
        newImg.putpixel((x, y), pixel)
        if (x == width - 1):
            x = 0
            y += 1
        else:
            x += 1
        if (y == height - 1):
            break

    newImgName = input("Nume imagine noua cu extensie: ")
    newImg.save(newImgName, str(newImgName.split(".")[1].upper()))

def decode():
    imgName = input("Nume imagine cu extensie: ")
    image = Image.open(imgName, 'r')

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

choice = int(input("1. Cripteaza\n2. Decripteaza\n"))
if (choice == 1):
    encode()
elif (choice == 2):
    print("Cuvant decriptat : " + decode())