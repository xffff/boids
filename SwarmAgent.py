# modified from BoidRoids in the max examples by Cycling '74
import random

class Swarm:
    agents        = []
    numboids      = 0
    avgvelocity_x = 0
    avgvelocity_y = 0
    centroid_x    = 0
    centroid_y    = 0
    agentcount    = 0
    friction      = 0.5
    gravity       = 0.1
    gravpoint_x   = 0
    gravpoint_y   = 0
    mode          = "normal"

    def __init__(self, numboids):
        self.numboids = numboids
        for i in xrange(self.numboids):
            a = Agent(random.random(),
                      random.random(),
                      (random.random() - 0.5) * 0.1,
                      (random.random() - 0.5) * 0.1)
            self.agents.append(a)
            
    def getBoids(self):
        cx  = 0
        cy  = 0
        cvx = 0
        cvy = 0
        for i in xrange(self.numboids):
            self.tick(i)
            cx  = cx + self.agents[i].x
            cy  = cy + self.agents[i].y
            cvx = cvx + self.agents[i].vx
            cvy = cvy + self.agents[i].vy

        self.centroid_x = cx/self.numboids
        self.centroid_y = cy/self.numboids
        self.avgvelocity_x = cvx/self.numboids
        self.avgvelocity_y = cvy/self.numboids

        if self.mode == "normal":
            return [[a.x for a in self.agents],
                    [a.y for a in self.agents],
                    [a.vx for a in self.agents],
                    [a.vy for a in self.agents]]
        elif self.mode == "average":
            return [self.centroid_x,
                    self.centroid_y,
                    self.avgvelocity_x,
                    self.avgvelocity_y]
        else:
            print "ERROR: BoidRoids can be either mode normal or average"
            
    def tick(self, a):
        px = self.agents[a].vx
        py = self.agents[a].vy

        self.separate(a)
        self.align(a)
        self.cohere(a)
        self.gravitate(a)

        #inertia
        self.agents[a].vx = (px*self.agents[a].inertia) + \
                            (self.agents[a].vx*(1-self.agents[a].inertia))
        self.agents[a].vy = (py*self.agents[a].inertia) + \
                            (self.agents[a].vy*(1-self.agents[a].inertia))

        #velocity
        self.agents[a].vx = self.clip(-self.agents[a].maxvel,
                                      self.agents[a].vx,
                                      self.agents[a].maxvel)
        self.agents[a].vy = self.clip(-self.agents[a].maxvel,
                                      self.agents[a].vy,
                                      self.agents[a].maxvel)

        #friction
        self.agents[a].x = self.agents[a].x + (self.agents[a].vx*(1-self.friction))
        self.agents[a].y = self.agents[a].y + (self.agents[a].vy*(1-self.friction))

    def separate(self, a):
        for i in xrange(self.numboids):
            if(a != i):
                dx = self.agents[i].x - self.agents[a].x
                dy = self.agents[i].y - self.agents[a].y

                if dx > 0.5    : dx = dx - 1
                elif dx < -0.5 : dx = dx + 1
                if dy > 0.5    : dy = dy - 1
                elif dy < -0.5 : dy = dy + 1

                if abs(dx) > 0.0001 and abs(dy) > 0.0001 : mag = dx*dx + dy*dy
                else                                     : mag = 0.01
                    
                if mag < self.agents[a].septhresh:
                    if mag < 0.0001 : proxscale = 8
                    else            : proxscale = self.agents[a].septhresh / \
                                    (self.agents[a].septhresh - (self.agents[a].septhresh-mag))
                    self.agents[a].vx = self.agents[a].vx - \
                                        (dx*self.agents[a].separation*proxscale);
                    self.agents[a].vy = self.agents[a].vy - \
                                        (dy*self.agents[a].separation*proxscale);

    def align(self, a):
        # conform to velocities towards average velocity
        dvx = self.avgvelocity_x - self.agents[a].vx;
        dvy = self.avgvelocity_y - self.agents[a].vy;        
        self.agents[a].vx = self.agents[a].vx + (dvx*self.agents[a].alignment);
        self.agents[a].vy = self.agents[a].vy + (dvy*self.agents[a].alignment);
                    
    def cohere(self, a):
        # move towards center of mass
        dx = self.centroid_x - self.agents[a].x;
        dy = self.centroid_y - self.agents[a].y;
        self.agents[a].vx = self.agents[a].vx + (dx*self.agents[a].coherence);
        self.agents[a].vy = self.agents[a].vy + (dy*self.agents[a].coherence);

    def gravitate(self, a):
        dx = self.gravpoint_x - self.agents[a].x;
        dy = self.gravpoint_y - self.agents[a].y;
        self.agents[a].vx = self.agents[a].vx + (dx*self.gravity);
        self.agents[a].vy = self.agents[a].vy + (dy*self.gravity);
                    
    def clip(self, lo, x, hi):
        return lo if x <= lo else hi if x >= hi else x

class Agent:
    x             = 0
    y             = 0
    vx            = 0
    vy            = 0
    separation    = 0.2
    alignment     = 0.05
    coherence     = 0.02
    inertia       = 0.4
    maxvel        = 0.3
    septhresh     = 0.2
    
    def __init__(self, x, y, vx, vy):
        self.x  = x
        self.y  = y
        self.vx = vx
        self.vy = vy
