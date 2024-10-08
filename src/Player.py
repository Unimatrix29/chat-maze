class Player:
    """
    Player class represents a ChatGPT
    character on a play field.
    
    Attributes
    -----------
        currentPosition : [int, int] = [0, 0]
            The point of a maze the player's standing on.
        name : str = ""
            The name of the chosen ChatGPT role to be displayed in chat.
        isHidden : bool = False
            A flag to switch visibility while rendering.
            
    Methods
    -----------
        **move** (vector)
            Adds a vector to player's currentPosition.
        **set_position** (point)
            Sets player's currentPosition to a point.
        **get_rotated_position** (count)
            Returns player's currentPosition after rotating it <count> times.
        **hide** (request)
            Changes player's render visibility.
        **change_name** (newName)
            Changes player's name to a new one.
    """
    
    def __init__(self, startPosition: list[int] = [0, 0], name: str = ""):
        """
        The constructor of the Player class.
        
        Parameters
        ----------
            startPosition : [int, int] = [0, 0]
                The start point of a maze.
            name : str = ""
                The name of a player/ChatGPT role.
        """
        self.currentPosition = list(startPosition)
        self.name = name
        self.isHidden = False
        
    def move(self, mVector: list[int]):
        """
        Moves the player towards given vector.
        
        Parameters
        ----------
            mVector : [int, int]
                The moving vector to be added to player's currentPosition.
                
        Returns:
            None : Doesn't return any value.
        """
        self.currentPosition[0] += mVector[0]
        self.currentPosition[1] += mVector[1]
        
    def set_position(self, point: list[int]):
        """
        Sets currentPosition to a given point.
        
        Parameters
        ----------
            point : [int, int]
                The point of a maze to place the player onto.
                
        Returns:
            None : Doesn't return any value.
        """
        self.currentPosition[0] = int(point[0])
        self.currentPosition[1] = int(point[1])
        
    def get_rotated_position(self, count: int = 1) -> list[int]:
        """
        Calculates currentPosition of the player
        as if the maze would get rotated <count> times.

        Parameters
        ----------
            count : int = 1
                The amount of applied rotations to use in calculation.
                
        Returns
        ----------
            rotatedPosition : [int, int]
                The position in <count> rotated maze.
        """
        rotatedPosition = [int(self.currentPosition[0]), int(self.currentPosition[1])]
        for i in range(count):
            rotatedPosition = [int(rotatedPosition[1]), 15 - int(rotatedPosition[0])]
            
        return rotatedPosition
    
    def hide(self, request: bool):
        """
        Changes player's visibility flag to <request>.
        
        Parameters
        ----------
            request : bool
                The value to set the visibility flag onto.
                True = the player is hidden, False = the player is visible.
                
        Returns:
            None : Doesn't return any value.
        """
        self.isHidden = request
        
    def change_name(self, newName: str):
        """
        Changes player's name.
        
        Parameters
        ----------
            newName : str
                The new name of the player.
                
        Returns:
            None : Doesn't return any value.
        """
        self.name = newName