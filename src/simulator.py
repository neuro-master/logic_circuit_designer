from logic_gate_wire import LogicGate, Wire
import pygame
import math


wireOnClr = (225, 200, 30)
wireOffClr = (0, 0, 0)
inputCellActivatableRadius = 15     # Same as OUTPUT_CELL's display radius


def AllInputsUpdated(logicGate):
    for wire in logicGate.inputWires:
        if wire != None and wire.updatedThisStep == False:
            return False
    return True


class StateSimulator:

    def __init__(self):
        self.logicGates = []
        self.wires = []
    
    def AddLogicGate(self, logicGateType : str, position : tuple[float, float]):
        self.logicGates.append(LogicGate(logicGateType, position))
    
    def AddConnection(self, logicGate1, logicGate2, LG2_inputPinIndex):
        if logicGate1.outputWire == None:
            # Create Wire
            self.wires.append(Wire())
            wire = self.wires[len(self.wires) - 1]
            logicGate1.outputWire = wire
            logicGate2.inputWires[LG2_inputPinIndex] = wire
        else:
            # Add to existing wire
            logicGate2.inputWires[LG2_inputPinIndex] = logicGate1.outputWire
    
    def Step(self, mouseClicked: bool):
        # Reset all wire's 'updated' value
        for wire in self.wires:
            wire.updatedThisStep = False
        
        # Change value if INPUT_CELL clicked
        for logicGate in self.logicGates:
            mouseOnCell = math.dist(pygame.mouse.get_pos(), logicGate.position) < inputCellActivatableRadius
            if logicGate.type == 'INPUT_CELL' and mouseClicked and mouseOnCell:
                logicGate.inputCellValue = not logicGate.inputCellValue

        # First update all inputCell's outputWire (if it exists)
        for logicGate in self.logicGates:
            if logicGate.type == 'INPUT_CELL' and logicGate.outputWire != None:
                logicGate.outputWire.state = logicGate.inputCellValue
                logicGate.outputWire.updatedThisStep = True
        
        # Keep updating the logic gates whose all inputWires (if any) are updated
        while [(wire.updatedThisStep) for wire in self.wires] != [True] * len(self.wires):
            for logicGate in self.logicGates:
                if AllInputsUpdated(logicGate) and logicGate.outputWire != None:
                    logicGate.UpdateOutputWire()
                    logicGate.outputWire.updatedThisStep = True
    
    def Draw(self, screen):
        # Draw the wires
        for wire in self.wires:
            wireColor = wireOnClr if wire.state == True else wireOffClr
            for positionPair in wire.positionPairs:
                pygame.draw.line(screen, wireColor, positionPair[0], positionPair[1], 5)
        
        # Draw Logic Gates (both images and pins)
        for logicGate in self.logicGates:
            logicGate.Draw(screen)
        
        # Draw I/O Cell Circles
        for logicGate in self.logicGates:
            if logicGate.type == 'INPUT_CELL':
                circleClr = wireOnClr if logicGate.inputCellValue == True else wireOffClr
                pygame.draw.circle(screen, circleClr, logicGate.position, inputCellActivatableRadius)

            if logicGate.type == 'OUTPUT_CELL':
                outputCellValue = False if logicGate.inputWires[0] == None else logicGate.inputWires[0].state
                circleClr = wireOnClr if outputCellValue == True else wireOffClr
                pygame.draw.circle(screen, circleClr, logicGate.position, inputCellActivatableRadius)
