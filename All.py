from math import *

class Country :

    def __init__(self, name, n, S0, R0, U0, N0, A0, D0, x, p, q, a, k, h, m = 0) :
        self.v = {
            'S' : S0,
            'R' : R0,
            'U' : U0,
            'N' : N0,
            'A' : A0,
            'D' : D0,
        }
        self.t           = 0
        self.x1          = x
        self.x2          = x/(10**8)
        self.p           = p
        self.q           = q
        self.a           = a
        self.n           = n
        self.k           = k * n
        self.m           = m
        self.h           = 0
        self.max_h       = h
        self.name        = name
        self.has_cure    = False
        self.claim       = self.n - self.v['S'] - self.v['D'] - self.v['R']
        self.arrive_time = None
        self.fly_ct      = 0
        self.m_ct        = 0
        self.death       = 0

    def delta4(self, v) :
        self.h = min(self.m, v['N'], self.max_h)
        dS = - self.x1 * (1-(v['N']+v['A'])/self.k) *v['S'] / self.n * (v['N']+v['A'])
        dR = self.h - self.x2 * (v['N']+v['A']) * v['R'] / self.n * (1 - (v['N']+v['A']) / self.k)
        dU = - dS - dR + self.h - self.p * v['U']
        dN = self.p * v['U'] - self.h - self.q * (v['N'] - self.h)
        dA = self.q * (v['N'] - self.h) - self.a * v['A']
        dD = self.a * v['A']
        self.v = {
            'S' : int(v['S'] + dS),
            'R' : int(v['R'] + dR),
            'U' : int(v['U'] + dU),
            'N' : int(v['N'] + dN),
            'A' : int(v['A'] + dA),
            'D' : int(v['D'] + dD),
        }
        self.death += int(dD)
        self.m += -self.h
        if self.m < 1:
            self.m = 0
            self.has_cure = False
        return self.v, self.m

    def delta3(self, v) :
        dS = - self.x1 * (1-(v['N']+v['A'])/self.k) * v['S'] / self.n * (v['N']+v['A'])
        dR = 0
        dU = (1-(v['N']+v['A']) / self.k) * self.x1 * v['S'] / self.n * (v['N']+v['A']) - self.p * v['U']
        dN = self.p * v['U'] - self.q * v['N']
        dA = self.q * v['N'] - self.a * v['A']
        dD = self.a * v['A']
        self.v = {
            'S' : int(v['S'] + dS),
            'R' : int(v['R'] + dR),
            'U' : int(v['U'] + dU),
            'N' : int(v['N'] + dN),
            'A' : int(v['A'] + dA),
            'D' : int(v['D'] + dD),
        }
        self.death += int(dD)
        return self.v

    def update(self) :
        if not self.has_cure :
            self.delta3(self.v)
        if self.has_cure :
            self.delta4(self.v)
        
        for stage, num in self.v.items() :
            if self.v[stage] < 0:
                self.v[stage] = 0

        self.t += 1

    def add_medicine(self, amount) :
        self.m      += amount
        self.m_ct   += amount
        self.fly_ct += 1
        if self.m > 0 :
            self.has_cure = True

    def claim(self) :
        self.claim = self.n - self.v['S'] - self.v['D'] - self.v['R']
        return [self.t, self.claim, self.name]

    def check_stop(self) :
        if self.v['A'] < 1 and self.v['N'] < 1 and self.v['U'] < 1 :
            print 'first_perc%     :', frac
            print 'first_day       :', first_day
            print 'Total Amount    :', (self.m_ct - self.m)
            print 'Total flight    :', self.fly_ct
            print 'Current Storage :', self.m
            print 'Speed           :', speed
            print 'delta_t         :', delta_t
            print 'The final assessment score is: ', (0.2*(self.m_ct - self.m) + 0.2* self.fly_ct + 0.6*self.t)
            return True
        return False


if __name__ == '__main__':
    for frac in range(50,101,10):
        for fd in range(1,11):
            for delta_t in range(1, 51):
                # __init__(self, name, n, S0, R0, U0, N0, A0, D0, x, p, q, a, k, h, m = 0)

                L = Country('Liberia', 3441790, 3432156, 0, 2582, 1687, 2553, 2812, 0.00669021, 0.00602125, 0.00937902, 0.00349354, 0.0015, 1000, 0) # t = 975, m = 6416
                G = Country('Guinea', 10057975, 10054955, 0, 1583, 208, 1612, 1142, 0.0611324, 0.11949, 0.582564, 0.00409383, 0.001, 1000, 0) # t = 635, m = 21228
                S = Country('SLE', 6440053, 6433516, 0, 766, 1179, 4523, 1169, 0.00378024, 0.0223951, 0.0547557, 0.00360921, 0.0007, 1000, 0) # t = 945, m = 3060

                for country in (L, G, S):
                    country.m_ct          = 0
                    country.fly_ct        = 0
                    country.death         = 0
                    speed           = 1000
                    medicine_needed = (country.v['N']) - country.m
                    first_day       = frac * medicine_needed / speed / 100 + fd

                    while not country.check_stop():
                        medicine_needed = (country.v['N']+country.v['U']) - country.m
                        if country.t > 13 and (country.t % delta_t == 0) and (medicine_needed > 0):
                            country.add_medicine(medicine_needed)

                        country.update()
                    # print country.t, country.h, country.v['U'], country.v['N'], country.v['A'], country.m, country.m_ct
                    print 'Ebola has been eradicated in %d days!\n' % country.t
                print '==================================================='
