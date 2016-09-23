##Proyecto
#Andres Lopez-B43885
#Jose Pablo Vargas -B37275
#Gramatica para crear partituras

#imports
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
from xml.dom import minidom
#------------------------------------------------------------------------#
#Un archivo MusicXML sigue la siguiente estructura base
'''
<?xml version="1.0"?>
    <score-partwise>
        <part-list>
            <score-part id="P1">
                <part-name>Voice 1</part-name>
            </score-part>
        </part-list>
        <part id="P1">
            <measure number="1">
                <attributes>
                    <time>
                        <beats>4</beats>
                        <beat-type>4</beat-type>
                    </time>
                    <clef>
                        <sign>G</sign>
                        <line>2</line>
                    </clef>
                </attributes>
                <note>
                    <pitch>
                        <step>C</step>
                        <octave>4</octave>
                    </pitch>
                    <duration>3</duration>
                    <type>half</type>
                </note>
            </measure>
        </part>
    </score-partwise>
'''
#crea la etiqueta <score-partwise>
#retorna la etiqueta 
def setScorePartWise():
    scorePartWise = Element("score-partwise")
    return scorePartWise

#crea la etiqueta <part-list>
#recibe <score-partwise> como padre
#retorna la etiqueta
def setPartList(scorePartWise):
    partList = SubElement(scorePartWise, "part-list")
    return partList

#crea la etiqueta <score-part>
#recibe <part-list> como padre
#recibe partId = ID del instrumento
def setScorePart(partId, partList):
    scorePart = SubElement(partList, "score-part")
    scorePart.set("id", partId)
    partName = SubElement(scorePart, "part-name")
    partName.text = "Voice {0}".format(partId[1]) 

#crea la etiqueta <part>
#recibe <score-partwise> como padre
#recibe idV = ID del instrumento
#retorna la etiqueta   
def setPart(idV, scorePartWise):
    part = SubElement(scorePartWise, "part")
    part.set("id", idV)
    return part

#crea la etiqueta <measure>
#recibe <part> como padre
#recibe number = numero de compas
#retorna la etiqueta
def setMeasure(number, part):
    measure = SubElement(part, "measure")
    measure.set("number", number)
    return measure

#convierte el tiempo de la nota a formato MusicXML
#TODO hacerlo con diccionario
#recibe t = duracion de la nota
#retorna la nota en formato MusicXML
def typeNote(t):
    if(t == "w"):
        return "whole"
    elif( t == "h"):
        return "half"
    elif( t == "q"):
        return "quarter"
    elif( t == "e"):
        return "eighth"
    elif( t == "s"):
        return "16th"
    
#crea la etiqueta <attributes>
#recibe <measure> como padre
#retorna la etiqueta
def setAttributes(measure):
    attributes = SubElement(measure, "attributes")
    return attributes

#crea la etiqueta <clef>,<sign>,<line>
#recibe <atributes> como padre
#recibe ClefV = valor de la clave
def setClef(clefV, attributes):
    clef = SubElement(attributes,"clef")
    sign = SubElement( clef, "sign")
    sign.text = clefV[0]
    line = SubElement( clef, "line")
    line.text = clefV[1]

#crea la etiqueta <time>,<beats>,<beat-type>
#recibe <atributes> como padre
#recibe timeV = valor de la medida    
def setTime(timeV, attributes):
    time = SubElement(attributes,"time")
    beats = SubElement(time, "beats")
    beats.text = timeV[0]
    beatType = SubElement(time, "beat-type")
    beatType.text = timeV[2:]
    
#crea la etiqueta <note>,<pitch>,<step>,<octave>,<duration>,<type>,</rest>
#recibe <measure> como padre
#recibe noteVal = valor de la nota
#recibe durationVal = duracion de la nota
def setNote(noteVal, durationVal, measure):
    note = SubElement(measure, "note" )
    #si la nota es rest(silencio), se utiliza la etiqueta </rest>
    if(noteVal[0]=="R"):
        rest = SubElement(note, "rest")
        duration = SubElement(note, "duration")
        duration.text = durationVal[0]
    #de lo contrario se utilizan <pitch>,<step>,<octave>,<type>
    else:
        pitch = SubElement(note, "pitch")
        step = SubElement(pitch, "step")
        step.text = noteVal[0];
        octave = SubElement(pitch, "octave")
        octave.text = noteVal[1:]
        duration = SubElement(note, "duration")
        duration.text = durationVal[0]
        typeN = SubElement(note, "type")
        typeN.text = typeNote(durationVal[1])
    
#crea una hilera que contiene el xml en formato con tabulados
#recibe la raiz del XML generado
#retorna la hilera en formato "lindo"
def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

#agrega una nota nueva al XML
#recibe measure =<measure> al que se le desea agregar la nota
#recibe noteVal = valor de la nota
#recibe durationVal = duracion de la nota 
def agregarNota(measure, noteVal, durationVal):
    setNote(noteVal, durationVal, measure)

#llama a agregarNota()
#recibe measure =<measure> al que se le desea agregar la nota
#recibe noteVal = valor de la nota
#recibe durationVal = duracion de la nota     
def crearXml(measure, noteVal, durationVal):
    agregarNota(measure, noteVal, durationVal)

#imprime el XML a un archivo
#recibe fileName = nombre de archivo.xml
#recibe scorePartWise = raiz del xml con la etiqueta <score-partwise>
def imprimir(fileName, scorePartWise):
    partitura = prettify(scorePartWise)
    with open(fileName, "w") as f:
        f.write(partitura)
    #tree = ElementTree(scorePartWise)
    #tree.write("C:/Users/Andy/Desktop/prueba.xml", encoding = "utf-8", xml_declaration = True) 
    #print(tostring(scorePartWise, method = "xml"))

