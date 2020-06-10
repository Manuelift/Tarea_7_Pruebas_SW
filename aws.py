import boto3
from time import gmtime, strftime

def normalizar(s):
    reemplazos = (("á", "a"),("é", "e"),("í", "i"),("ó", "o"),("ú", "u"))
    abc = 'abcdefghijklmnopqrstuvwxyz0123456789@'
    for c, r in reemplazos:
        s = s.replace(c, r).replace(c.lower(), r.lower())

    s = s.lower()
    s = s.replace(" ","")
    cadena = ""
    for c in s:
        if c in abc:
            cadena +=c
    return cadena

def obtenerTexto(image):
    bucket = 'manuelift-testing'
    client = boto3.client('rekognition')
    print("\nObteniendo texto de ",image)
    response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':image}})
    textDetections = response['TextDetections']
    palabras_detectadas = []
    for text in textDetections:
            #print ('Detected text:' + text['DetectedText'])
            #print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            if float(text['Confidence']) > 97:
                strings = text['DetectedText'].strip().split(" ")
                for s in strings:
                    p = normalizar(s)
                    if p not in palabras_detectadas:
                        palabras_detectadas.append(p)
    print ("Palabras detectadas : ",palabras_detectadas)
    return palabras_detectadas

def comparar(control, test, file):
    palabras_test = obtenerTexto(test)
    time_test = strftime("%d/%b/%Y %H:%M:%S", gmtime())
    for string in control:
        if string not in palabras_test:
            print("FALSE:  NO se encontro la totalidad del texto")
            file.write(f"[{time_test}]\n")
            file.write("Palabras en imagen de control: ")
            for palabra in control:
                file.write(f"{palabra}, ")

            file.write(f"\nPalabras en imagen de prueba ({test}): ")
            for palabra in palabras_test:
                file.write(f"{palabra}, ")
            file.write("\nFALSE:  NO se encontro la totalidad del texto\n")
            file.write(f"---------------------------------------------------------------------------------------------------------------------\n")
            return
    print ("TRUE:  SI se encontro la totalidad del texto")
    file.write(f"[{time_test}]\n")
    file.write("Palabras en imagen de control: ")
    for palabra in control:
        file.write(f"{palabra}, ")

    file.write(f"\nPalabras en imagen de prueba ({test}): ")
    for palabra in palabras_test:
        file.write(f"{palabra}, ")
    file.write("\nTRUE:  SI se encontro la totalidad del texto\n")
    file.write(f"---------------------------------------------------------------------------------------------------------------------\n")


def main():
    control_image = obtenerTexto("control.png")
    test_images = ["test-1.png","test-2.png","test-3.png","test-4.png","test-5.png","test-6.png","test-7.png","test-8.png","test-9.png","test-10.png","test-11.png","test-12.png","test-13.png","test-14.png","test-15.png"]
    fp = open("log.txt","w")
    fp.write(f"---------------------------------------------------------------------------------------------------------------------\n")
    for test_image in test_images:
        comparar(control_image,test_image,fp)
    fp.close()

if __name__ == "__main__":
    main()
