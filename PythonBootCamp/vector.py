"""Vector module"""

class Vector(object):
    
    def __init__(self, x, y, z):
        """Contructor for vector, takes 3 cartesian coordinates"""
        self.x = x
        self.y = y
        self.z = z
        
    def norm(self):
        """Return the norm of the vector (magnitude)"""
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self):
        """Normalize vector (norm = 1)"""
        norm = self.norm()
        self.x /= norm
        self.y /= norm
        self.z /= norm
        
    def __str__(self):
        """Overload string attribute for printing Vector instance"""
        printout = ', '.join([str(self.x), str(self.y), str(self.z)])
        return(printout)