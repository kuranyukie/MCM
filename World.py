from Country import *
from Delivery import *

class World :
    countries = []

    def __init__(self, n) :
        # for Country() for _ in range(n)
        self.di = di()
        country.name

    def simulate(sefl, max_day = 49) :
        for t in range(max_day) :
            for country in self.cities :
                country.simulate_one_day()
            if self.check_ebola_stopped(self):
                print 'ok'

    def check_ebola_stopped(self) :
        for country in self.cities() :
            if not country.check_ebola_stopped() :
                return False
        return True