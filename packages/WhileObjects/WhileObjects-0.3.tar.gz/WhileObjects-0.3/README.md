## OBJECT ORIENTED WHILE LOOPS (WhileObjects)

Interface for the While class to subclass and make your own Object Oriented While Loops

## DESCRIPTION

While objects are are a new data structure in which we retain reference to our loop indefinitely,
you can pick up the iteration where you left off much later in the script, or instantiate a new loop and not even run it at first

## Installation

`pip install WhileObjects`

## Usage

 i: The current iteration value
 first: The starting value of the loop
 end: The end value of the loop
 op: The operater used to do comparison if the loop should continue
 increment: The value by which the loop should increment/decrement
 calc: The calculated value of the current iteration

 The class While has the following methods:
    isFinished: Returns False if there are still iterations left to be done.
    start: Runs the full loop. The user should implement their calculation in a subclass.
    step: Steps through one iteration of the loop. The user should implement their calculation in a subclass.
    clear: Clears the stored work unit/other data.

example usage:
`loop = While(i=0,end=10)`
`while not loop.isFinished():`
`loop.step()`

subclass from While to override your implementation of loop.calc

class customLoop(While):

    def step(self):
        if self.op == "<" or self.op == "<=":`
            if not self.isFinished():`
                self.calc += self.i
                self.i += self.increment
        elif self.op == ">" or self.op == ">=":
            if not self.isFinished():
                self.calc += self.i
                self.i -= self.increment            
        return self.i


## Contributing

Homepage: https://github.com/James-Sorrow/ObjectWhileLoop

## License

MIT