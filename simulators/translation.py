from simulators import BaseSimulator, PIDController

class Translation(BaseSimulator): # FIXME only updates X
    def __init__(self, vm=5, kp=0.5, ki=0, kd=0.2, integrator_min=0, integrator_max=1):
        self.controller = PIDController(kp, ki, kd, integrator_min, integrator_max)
        self.vm = vm
        self.speed = 0, 0, 0

    def update(self, client):
        position = client.position()
        position_order = client.position_order()

        x, y, a = position.get()
        vx, vy, va = self.speed
        ox = position_order.get()[0]

        self.controller.set_order(ox, vx)
        dx = self.controller.update(x)

        # trapezium by threshold
        t = 1#self.rate
        vx = dx / t
        vx = max(min(vx, self.vm), -self.vm)
        dx = vx * t
        x += dx

        # reflect changes on the server
        position.set((x, y, a))
        self.speed = x, vy, va
