# polynomial.py
# by James Fulford
# deals with single variable polynomial objects

import copy
import cmath


class Polynomial(object):
    """
    mathematics.polynomial.Polynomial
    Is an object that simulates a single-variable polynomial.
    """
    def __init__(self, coefficients, descending=False):
        """ note: polynomial is in *ASCENDING* order: c + bx + ax^2
        """
        self.coefficients = copy.deepcopy(coefficients)
        if(descending):
            self.coefficients.reverse()
        self.simplify()

    # Basic Operations

    def evaluate(self, plug):
        result = 0
        for i in range(len(self.coefficients)):
            result += self[i] * (plug ** i)
        return(result)

    def degree(self):
        self.simplify()
        return(len(self.coefficients) - 1)

    def mult_by_x(self, power):
        return(Polynomial([0, 1]).exp(power).mult(self))

    # Basic Algebra

    def exp(self, exponent):
        if(exponent is 0):
            return Polynomial([1])
        result = self.copy()
        for i in range(exponent - 1):
            result = result.mult(self)
        return(result)

    def mult(self, poly):
        result = []
        for entry in range(len(self.coefficients) + len(poly.coefficients) - 1):
            result.append(0)
        for i in range(len(self.coefficients)):
            for j in range(len(poly.coefficients)):
                addby = (self[i] * poly[j])
                result[i + j] += addby
        return(Polynomial(result))


    def add(self, poly):
        result = []
        for i in range(max(len(self.coefficients), len(poly.coefficients))):
            try:
                result.append(self[i] + poly[i])
            except IndexError:
                if(len(self.coefficients) > len(poly.coefficients)):
                    result.append(self[i])
                else:
                    result.append(poly[i])
        return(Polynomial(result))

    # Yucky Algebra

    def replace(self, poly):
        result = []
        end_degree = self.degree() + poly.degree()
        for i in range(end_degree):
            result.append(0)
        for i in range(end_degree):
            term = Polynomial([self[i]]) * (poly ** i)
            for j in range(len(term.coefficients)):
                result[j] += term.coefficients[j]
        return(Polynomial(result))

    def simplify(self):
        try:
            while(self.leading_term() is 0):
                self.coefficients.pop()
        except IndexError:
            self.coefficients = [0]

    def leading_term(self):
        return(self.coefficients[len(self.coefficients) - 1])

    def remove_root(self, root):  # might not work...
        assert abs(self(root)) < 0.00001  # it has to be a root
        temp = self.copy()
        answer = Polynomial([0])
        for i in range(self.degree()):  # divide by x - root
            index = self.degree() - i
            multiplicand = temp[index]  # identify m
            adder = Polynomial([multiplicand * root, -multiplicand]).mult_by_x(index-1)
            # now, make -mx^index-1 + mx^index-2
            temp = temp + adder  # so the first term -mx^index-1 cancells out with correct x term
            answer = answer + Polynomial([multiplicand]).mult_by_x(index - 1)
        return(answer)



    # Calculus

    def derivative(self, times=1):
        result = self.copy()
        for deriv in range(times):
            result.coefficients.remove(result.coefficients[0])
            for i in range(len(result.coefficients)):
                result[i] *= (i + 1)
        result.simplify()
        return(result)

    def antiderivative(self, times=1, constants=[0]):
        assert len(constants) is times
        result = self.copy()
        for antideriv in range(times):
            for i in range(len(result.coefficients)):
                result[i] /= (i + 1)
            result.coefficients.insert(0, constants[antideriv])
        result.simplify()
        return(result)

    def integral(self, a, b):
        antiderivative = self.antiderivative(1, [0])  # coefficients don't matter
        return(antiderivative(b) - antiderivative(a))

    # Roots

    def count_roots(self):
        """ Descartes' Rule of Signs
        """
        roots = {
            "positive": 0,
            "negative": 0,
            "complex": 0
        }
        pos = self[0] > 0
        neg = pos
        for i in range(1, len(self.coefficients)):
            if(abs(self[i]) < 0.00001):
                continue
            if(pos is not(self[i] > 0)):
                roots["positive"] += 1
                pos = not pos
            if(neg is not((self[i] * ((-1) ** i)) > 0)):
                roots["negative"] += 1
                neg = not neg
        roots["complex"] = self.degree() - roots["positive"] - roots["negative"]
        return(roots)

    def roots(self):
        if(self.degree() is 2):
            return self._quad_root()
        elif(self.degree() is 3):  # "elif" means else if
            return self._cubic_root()
        raise NotImplementedError

    def _cubic_root(self):  # presumes polynomial equals 0
        assert self.degree() is 3  # Can't take cubic roots of non cubics!
        this = self.copy()
        roots = []
        this = this * Polynomial([1. / this.leading_term()])  # Divide everything by a
        repl = this.replace(Polynomial([-this[2] / 3.0, 1]))  # transform into:
        # t^3 + pt + q = 0 ; use Cardano's formula
        descriminant = ((repl[0] / 2.) ** 2) + ((repl[1] / 3.) ** 3)
        print("        descriminant (d): " + str(descriminant))
        print
        u = ((-repl[0] / 2) + cmath.sqrt(descriminant)) ** (1. / 3.)
        v = ((-repl[0] / 2) - cmath.sqrt(descriminant)) ** (1. / 3.)
        roots.append(u + v)  # is root of repl polynomial.
        roots[0] = roots[0] - (this[2] / 3.)  # is now root of this polynomial

        # m_and_n = Polynomial([1, 1, 1]).roots()
        # m = m_and_n[0]
        # n = m_and_n[1]
        # root2 = (m*u) + (n*v)
        # root3 = (n*u) + (m*v)

        # hack: divide out root
        remains = this.remove_root(roots[0])
        for root in remains.roots():  # quadratic equation
            roots.append(root)
        for root in roots:  # check my work!
            assert abs(this(root)) < 0.00001
        return(roots)

    def _quad_root(self):
        assert self.degree() is 2
        descrim = (self[1] ** 2) - (4 * self[2] * self[0])
        root1 = (-self[1] + cmath.sqrt(descrim)) / (2 * self[2])
        root2 = (-self[1] - cmath.sqrt(descrim)) / (2 * self[2])
        return(root1, root2)

    # Conveniences

    def __getitem__(self, value):
        return self.coefficients[value]

    def __setitem__(self, key, val):
        self.coefficients[key] = val

    def __str__(self):
        self.simplify()
        result = str(self[0])
        for i in range(1, len(self.coefficients)):
            result += " + " + str(self[i]) + "x^" + str(i)
        return(result)

    def copy(self):
        return Polynomial(copy.deepcopy(self.coefficients))

        # Built in operator support:
    __pow__ = exp
    __mul__ = mult
    __add__ = add
    __call__ = evaluate
