from math import *
from Delivery import *

class Country :

    def __init__(self, name, n, S0, R0, U0, N0, A0, D0, x, p, q, a, k, h, m = 0) :
        # self.delta = {
        #     'S' : lambda v : - self.x * v['S'] / self.n * (v['N']+v['A']),
        #     'U' : lambda v : self.x * v['S'] / self.n * (v['N']+v['A']) - self.p * v['U'],
        #     'N' : lambda v : self.p * v['U'] - self.q * v['N'],
        #     'A' : lambda v : self.q * v['N'] - self.a * v['A'],
        #     'D' : lambda v : self.a * v['A'],
        # }
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
        # print 'delta4 row40 h,m,n = ', self.h, self.m, self.v['N']
        # raw_input()
        # if self.h > self.m :
        #     self.h = self.m
        #     # print 'delta4 row42 h,m,n = ', self.h, self.m, self.v['N']
        #     # raw_input()
        # if self.h >= v['N'] :
        #     self.h = v['N']
        #     # print 'delta4 row46 h,m = ', self.h, self.m, self.v['N']
        #     # raw_input()
        dS = - self.x1 * (1-(v['N']+v['A'])/self.k) *v['S'] / self.n * (v['N']+v['A'])
        dR = self.h - self.x2 * (v['N']+v['A']) * v['R'] / self.n * (1 - (v['N']+v['A']) / self.k)
        # dU = (self.x1 * (v['N']+v['A']) * v['S'] / self.n + self.x2 * (v['N']+v['A']) * v['R'] / self.n) * (1-(v['N']+v['A']) / self.k)
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
        # print dS, dR, dU, dN, dA, dD
        self.death += int(dD)
        self.m += -self.h
        # print 'delta4 updated 61row : h=', self.h
        # print 'delta4 updated 61row : m=', self.m
        # # raw_input()
        if self.m < 1:
            self.m = 0
            self.has_cure = False
            # print 'row70 if m<1 h,m = ', self.h, self.m
            # raw_input()
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
        # print dA, dD, dN, dS, dR, dU
        self.death += int(dD)
        return self.v

    def update(self) :
        # for var, value in self.v.items() :
        #     self.v[var] += self.delta[var](self.v)
        if not self.has_cure :
            # self.h = 0
            # print 'M = ', self.m
            # print 'Enter Model 3'
            # raw_input()

            self.delta3(self.v)
        if self.has_cure :
            # print 'M = ', self.m
            # print 'Enter Model 4'
            # raw_input()
            self.delta4(self.v)
        
        for stage, num in self.v.items() :
            if self.v[stage] < 0:
                self.v[stage] = 0

        # if :
        #     self.claim()

        self.t += 1

    def add_medicine(self, amount) :
        # print 'N = ', self.v['N']
        # print 'add_medicine,' , amount
        # raw_input()
        self.m      += amount
        self.m_ct   += amount
        self.fly_ct += 1
        if self.m > 0 :
            self.has_cure = True
        # print 'At day %d, %s gets %d cure!' % (self.t, self.name, amount)

    def claim(self) :
        self.claim = self.n - self.v['S'] - self.v['D'] - self.v['R']
        return [self.t, self.claim, self.name]

    def check_stop(self) :
        if self.v['A'] < 1 and self.v['N'] < 1 and self.v['U'] < 1 :
            # print 'first_perc%     :', frac
            # print 'first_day       :', first_day
            # print 'Total Amount    :', (self.m_ct - self.m)
            # print 'Total flight    :', self.fly_ct
            # print 'Current Storage :', self.m
            # print 'Speed           :', speed
            # print 'delta_t         :', delta_t
            # print 'The final assessment score is: ', (0.2*(self.m_ct - self.m) + 0.2* self.fly_ct + 0.6*self.t)
            print frac
            print first_day
            print (self.m_ct - self.m)
            print self.fly_ct
            print self.m
            print speed
            print delta_t
            print (0.1*(self.m_ct - self.m) + 0.1* self.fly_ct + 0.3* self.death + 0.5*self.t)
            print self.t
            print self.death
            return True
        return False


if __name__ == '__main__':
    # for frac in range(50,101,10):
    # for fd in range(1,10):
    for delta_t in range(53, 54):
        # __init__(self, name, n, S0, R0, U0, N0, A0, D0, x, p, q, a, k, h, m = 0)

        # L = Country('Liberia', 3441790, 3432156, 0, 2582, 1687, 2553, 2812, 0.00669021, 0.00602125, 0.00937902, 0.00349354, 0.0015, 1000, 0) # t = 975, m = 6416
        # L = Country('Guinea', 10057975, 10054955, 0, 1583, 208, 1612, 1142, 0.0611324, 0.11949, 0.582564, 0.00409383, 0.001, 1000, 0) # t = 635, m = 21228
        L = Country('SLE', 6440053, 6433516, 0, 766, 1179, 4523, 1169, 0.00378024, 0.0223951, 0.0547557, 0.00360921, 0.0007, 1000, 0) # t = 945, m = 3060

        frac            = 100
        L.m_ct          = 0
        L.fly_ct        = 0
        L.death         = 0
        speed           = 1000
        medicine_needed = (L.v['N']) - L.m
        first_day       = frac * medicine_needed / speed / 100 + 1
        # delta_t         = 27

        print 't  h    u   n   a   m  total'
        # num = 0
        while not L.check_stop():
            # if num > 20:
                # break
            # print 'new day check:'
            # print 'day', L.t
            # print 'first_day', first_day
            # raw_input()
            medicine_needed = (L.v['N']+L.v['U']) - L.m
            if L.t == first_day:
                L.add_medicine(min((frac * medicine_needed / 100), (speed * L.t)))
                # print 'if1: day = ', L.t
                # print 'if1: medicine_needed = ', medicine_needed
            if (L.t > first_day) and (L.t % delta_t == 0) and (medicine_needed > 0):
                # print 'if2: day = ', L.t
                # print 'if2: medicine_needed = ', medicine_needed
                L.add_medicine(medicine_needed)

            L.update()
            # num += 1
            
            print L.t, L.h, L.v['U'], L.v['N'], L.v['A'], L.m, L.m_ct
            # raw_input()
            # print 'medicine: ', L.m
        print 'Ebola has been eradicated in %d days!\n' % L.t
    print '==================================================='
