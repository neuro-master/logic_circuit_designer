from simulator import StateSimulator, LogicGate
from logic_gates_menu import LogicGatesMenu
import pygame
import math

pinClickingThresholdDist = 6

class PlacementSystem:

    def __init__(self):
        # State variables
        self.placingLG = False
        self.currentPlacingLG_Type = None
        self.currentPlacingLG_Image = None

        self.placingWire = False
        self.currentPlacingWire_LG1 = None
        self.inputPinIndex = None
        self.prevWirePos = None  # Form of tuple of 2 floats i.e. (x, y)
        self.tempPositionPairs = []

        # Graphics
        logicGateTypes = ['INPUT_CELL', 'OUTPUT_CELL', 'NOT', 'AND', 'OR', 'NAND', 'NOR', 'XOR', 'XNOR']
        self.logicGatesMenu = LogicGatesMenu(logicGateTypes)

        self.consolasFont = pygame.font.SysFont('Consolas', 35)
    

    def CleanupPlacingLG_Variables(self):
        self.placingLG = False
        self.currentPlacingLG_Type = None
        self.currentPlacingLG_Image = None
    
    def CleanupPlacingWireVariables(self):
        self.placingWire = False
        self.currentPlacingWire_LG1 = None
        self.inputPinIndex = None
        self.prevWirePos = None
        self.tempPositionPairs = []
    
    def CleanupFullSimulation(self, simulator : StateSimulator):
        self.CleanupPlacingLG_Variables()
        self.CleanupPlacingWireVariables()
        simulator.logicGates = []
        simulator.wires = []
    

    def GetLG_IfMouseOnInputPin(self, simulator : StateSimulator) -> tuple[LogicGate, int]:
        for logicGate in simulator.logicGates:
            for i in range(len(logicGate.inputPinPositions)):
                inputPinPos = logicGate.inputPinPositions[i]
                mousePos = pygame.mouse.get_pos()
                mouseOnPin = math.dist(mousePos, inputPinPos) < pinClickingThresholdDist

                if mouseOnPin:
                    return (logicGate, i)
        else:
            return (None, None)

    def GetLG_IfMouseOnOutputPin(self, simulator : StateSimulator) -> LogicGate:
        for logicGate in simulator.logicGates:
            if logicGate.type != 'OUTPUT_CELL':
                mousePos = pygame.mouse.get_pos()
                mouseOnPin = math.dist(mousePos, logicGate.outputPinPosition) < pinClickingThresholdDist
                
                if mouseOnPin:
                    return (logicGate)
        else:
            return None


    def HandleLogicGatePlacement(self, simulator : StateSimulator, mouseClicked : bool):
        if self.placingWire:
            return
        
        mousePos = pygame.mouse.get_pos()

        # Start placing Logic Gate
        menuLG_Clicked, menuLG_Type = self.logicGatesMenu.isClicked(mouseClicked)

        if menuLG_Clicked and self.placingLG == False:
            self.placingLG = True
            self.currentPlacingLG_Type = menuLG_Type
            self.currentPlacingLG_Image = pygame.image.load("LogicGateImages/" + menuLG_Type + ".png")
        
        # Finish placing Logic Gate
        isPlacingPointValid = mousePos[0] < 1050
        if mouseClicked and self.placingLG and isPlacingPointValid:
            simulator.AddLogicGate(self.currentPlacingLG_Type, mousePos)
            self.CleanupPlacingLG_Variables()
            if self.currentPlacingLG_Type == 'INPUT_CELL':
                simulator.logicGates[-1].inputCellValue = 0

        # Cancel placing Logic Gate
        if self.placingLG and (pygame.key.get_pressed())[pygame.K_x]:
            self.CleanupPlacingLG_Variables()


    def HandleWirePlacement(self, simulator : StateSimulator, mouseClicked : bool, keyX_Clicked : bool):
        mousePos = pygame.mouse.get_pos()
        validPosition = mousePos[0] < 1050

        if self.placingLG:
            return

        # Start Placing Wire (Check if any output pin clicked)
        if mouseClicked and validPosition and (self.placingWire == False):
            logicGate = self.GetLG_IfMouseOnOutputPin(simulator)

            if logicGate != None:
                self.placingWire = True
                self.currentPlacingWire_LG1 = logicGate
                self.prevWirePos = mousePos
        
        # Extend wire that is drawn
        if mouseClicked and validPosition and self.placingWire:
            inputPinClickedLG, i = self.GetLG_IfMouseOnInputPin(simulator)
            outputPinClickedLG = self.GetLG_IfMouseOnOutputPin(simulator)

            if inputPinClickedLG == None and outputPinClickedLG == None:
                positionPair = ( (self.prevWirePos), (mousePos) )
                self.tempPositionPairs.append(positionPair)
                self.prevWirePos = mousePos

        # Finish Placing Wire (Check if any input pin clicked)
        if mouseClicked and validPosition and self.placingWire:
            logicGate, inputPinIndex = self.GetLG_IfMouseOnInputPin(simulator)

            if logicGate != None and logicGate.inputWires[inputPinIndex] == None:
                simulator.AddConnection(self.currentPlacingWire_LG1, logicGate, inputPinIndex)
                self.tempPositionPairs.append( ((self.prevWirePos), (mousePos)) )
                logicGate.inputWires[inputPinIndex].positionPairs.extend(self.tempPositionPairs)

                self.CleanupPlacingWireVariables()
        
        # Cancel/Undo placing wire
        if keyX_Clicked and self.placingWire:
            if len(self.tempPositionPairs) > 1:
                self.prevWirePos = self.tempPositionPairs[-1][0]
                self.tempPositionPairs.pop()
            else:
                self.CleanupPlacingWireVariables()


    def Update(self, simulator : StateSimulator, mouseClicked : bool, keyX_Clicked : bool, keyC_Clicked : bool):
        self.HandleLogicGatePlacement(simulator, mouseClicked)
        self.HandleWirePlacement(simulator, mouseClicked, keyX_Clicked)

        # Clear/Delete everything
        if keyC_Clicked:
            self.CleanupFullSimulation(simulator)


    def Draw(self, screen, simulator : StateSimulator):
        mousePos = pygame.mouse.get_pos()

        # Draw the Logic Gate Menu
        self.logicGatesMenu.Draw(screen)

        # Draw the temporary logic gate image (if we're currently placing a LG)
        if self.placingLG:
            rect = self.currentPlacingLG_Image.get_rect()
            rect.center = mousePos
            screen.blit(self.currentPlacingLG_Image, rect)
        
        # Draw the temporary wire(s) (if currently placing a wire)
        if self.placingWire:
            for positionPair in self.tempPositionPairs:
                pygame.draw.line(screen, (0, 0, 0), positionPair[0], positionPair[1], 5)
                
            if len(self.tempPositionPairs) > 0:
                pygame.draw.line(screen, (0, 0, 0), self.tempPositionPairs[-1][1], mousePos, 5)
            else:
                pygame.draw.line(screen, (0, 0, 0), self.currentPlacingWire_LG1.outputPinPosition, mousePos, 5)
        
        # Draw the 'Hints' Text
        hintTextStr = ''
        if (self.placingLG):
            hintTextStr = 'Press X to cancel placing the Logic Gate'
        elif (self.placingWire):
            hintTextStr = 'Press X to cancel/undo placing of wire'
        elif (len(simulator.logicGates) > 0):
            hintTextStr = 'Press C to clear everything'

        hintText = self.consolasFont.render(hintTextStr, True, (15, 15, 15))
        screen.blit(hintText, (15, 760))
