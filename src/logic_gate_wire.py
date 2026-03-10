import pygame


def getInputPinPos(LG_Type : str, position : tuple[float, float], pinIndex : int) -> tuple[float, float]:
    if LG_Type == 'INPUT_CELL':
        return None
    
    xOffsets = {
        'OUTPUT_CELL' : -23, 'NOT' : -35, 'AND' : -43, 'OR' : -35,
                'NAND': -54, 'NOR' : -45, 'XOR' : -43, 'XNOR' : -49
    }

    yOffset = 20
    yOffset = -yOffset if pinIndex == 0 else yOffset
    yOffset = 0 if LG_Type == 'NOT' or LG_Type == 'OUTPUT_CELL' else yOffset

    return (xOffsets[LG_Type] + position[0],  + yOffset + position[1])

def getOutputPinPos(LG_Type : str, position : tuple[float, float]) -> tuple[float, float]:
    if LG_Type == 'OUTPUT_CELL':
        return None
    
    xOffsets = {
        'INPUT_CELL' : 23, 'NOT' : 40, 'AND' : 50, 'OR' : 50,
        'NAND': 57, 'NOR' : 58, 'XOR' : 53, 'XNOR' : 65
    }

    return (xOffsets[LG_Type] + position[0], position[1])


class Wire:
    def __init__(self):
        self.state = False
        self.updatedThisStep = False    # Reset to False each sim step
        self.positionPairs = []     # Each element contains a tuple of 2 elements i.e. (startPos, endPos)


class LogicGate:

    def __init__(self, type, position):
        self.type = type
        self.inputWires = []    # List elements reference the wire objects
        self.outputWire = None  # References the wire object

        # Graphics related
        self.image = pygame.image.load("logic_gate_images/" + type + ".png")
        self.position = position

        # I/O Pin's Positions
        self.inputPinPositions = [getInputPinPos(type, position, 0), getInputPinPos(type, position, 1)]
        self.outputPinPosition = getOutputPinPos(type, position)

        # Exception: InputCell needs custom value setting
        if (type == "INPUT_CELL"):
            self.inputCellValue = False

        # Initialize pins based on type of LogicGate
        if type == "INPUT_CELL":
            self.inputWires = []
            self.inputPinPositions = []
        elif type == "NOT" or type == "OUTPUT_CELL":
            self.inputPinPositions = [ getInputPinPos(type, position, 0) ]
            self.inputWires = [None]
        else:
            self.inputWires = [None, None]
    

    def UpdateOutputWire(self):
        if self.outputWire == None:
            return
        
        inputVals = [(False if inputWire == None else inputWire.state) for inputWire in self.inputWires]

        if self.type == "INPUT_CELL":
            self.outputWire.state = self.inputCellValue
        elif self.type == "NOT":
            self.outputWire.state = not inputVals[0]
        elif self.type == "AND":
            self.outputWire.state = inputVals[0] and inputVals[1]
        elif self.type == "OR":
            self.outputWire.state = inputVals[0] or inputVals[1]
        elif self.type == "XOR":
            self.outputWire.state = (inputVals[0] and not inputVals[1]) or (not inputVals[0] and inputVals[1])
        elif self.type == "NAND":
            self.outputWire.state = not (inputVals[0] and inputVals[1])
        elif self.type == "NOR":
            self.outputWire.state = not (inputVals[0] or inputVals[1])
        elif self.type == "XNOR":
            self.outputWire.state = (inputVals[0] and inputVals[1]) or (not inputVals[0] and not inputVals[1])
    

    def Draw(self, screen):
        # Draw Logic Gate Image
        rect = self.image.get_rect()
        rect.center = self.position
        screen.blit(self.image, rect)

        # Draw the pins (if they exist)
        for inputPinPos in self.inputPinPositions:
            if inputPinPos != None:
                pygame.draw.circle(screen, (0, 0, 0), inputPinPos, 6)

        if self.outputPinPosition != None:
            pygame.draw.circle(screen, (0, 0, 0), self.outputPinPosition, 6)
