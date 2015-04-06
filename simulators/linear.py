from simulators import BaseSimulator, PIDController, Trapezium

def LinearSimulator(prop_getter, order_getter):
    class _LinearSimulator(BaseSimulator):
        def __init__(self, max_vel, max_acc,
                kp, ki, kd,
                integrator_min=0, integrator_max=1,
                value=0, derivator=0, integrator=0):
            self.controller = PIDController(kp, ki, kd,
                    integrator_min, integrator_max, derivator, integrator)
            self.trapezium = Trapezium(max_vel, max_acc, value, derivator)

        def update(self, client):
            value = prop_getter(client)
            order = order_getter(client)

            x = value.get()
            ox = order.get()
            self.controller.set_order(ox,
                    self.controller.derivator,
                    self.controller.integrator)
            dx = self.controller.update(x)

            self.trapezium.update(x + dx)
            value.set(self.trapezium.value)

    return _LinearSimulator
