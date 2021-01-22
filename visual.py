class Color:
  def __init__(self, blue, green, red):
    self.blue = blue
    self.green = green
    self.red = red
  
  def solve(self) -> tuple:
    return (self.blue, self.green, self.red)