import numpy as np
import re
import argparse 
from fractions import Fraction as F
from itertools import permutations as P

def add(a,b):
	'''Adds two numbers and returns the result.'''
	return a+b

def sub(a,b):
	'''Subtracts two numbers and returns the result.''' 
	return a-b

def mul(a,b):
	'''Multiplies two numbers and returns the result.''' 
	return a*b

def div(a,b):
	'''Divides two numbers and returns the result as a Fraction (or False if ZeroDivisionError).'''
	try:
		return F(a,b)
	except ZeroDivisionError:
		return None

class twenty_four_game:
	''' 
	A class to solve the 24 game.

	Args:
		stop (int):	the number of solutions to give
	'''

	def __init__(self, stop):
		self.ops = [add, add, add, sub, sub, sub, mul, mul, mul, div, div, div]
		self.parens = [self.A, self.B, self.C, self.D, self.E]
		self.iter_ops = list(P(self.ops, 3))
		self.def_stop = stop

		symbols = ("+", "-", "*", "/")
		for i in range(4):
			setattr(self.ops[i*3], "n", symbols[i])

	def set_def_stop(self, n):
		'''
		Sets the number of solutions to give.

		Args:
			n (int): the number of solutions to give
		'''
		self.def_stop = n


	def check_input(self, val):
		'''Checks if user input is a valid number. If valid, return True. Else, return False.'''
		try:
			int(val)
			return True
		except ValueError:
			return False

	def get_user_inputs(self):
		'''Gets the 24 game numbers from the user using raw_input and calls check_input to make sure they're valid values.'''
		ordinals = ["first", "second", "third", "fourth"]
		nums = []

		for ordinal in ordinals:
			user_input = raw_input("what is the {} number? ".format(ordinal) ) 
			if self.check_input(user_input):
				nums.append(int(user_input))
			else:
				return None

		return nums

	def order(self, rem_paren, sol):
		'''
		If two numbers are being multiplied or added, this function will make sure that they are in ascending numerical order in the solution string (sol) and return the resulting solution string.

		Args:
			rem_paren (str): the solution description without parenthesis
			sol (str): the solution description with parentheses
		''' 
		rem_paren_arr = rem_paren.split(" ")
		paren_holder = re.sub(r"[+\-*\/0-9]", "{}", sol)
		for ind in range(1,6,2):
			if rem_paren_arr[ind]=="+" or rem_paren[ind]=="*":
				if int(rem_paren_arr[ind-1]) > int(rem_paren_arr[ind+1]):
					rem_paren_arr[ind-1], rem_paren_arr[ind+1] = rem_paren_arr[ind+1], rem_paren_arr[ind-1]
		return paren_holder.format(*rem_paren_arr)
		

	def remove_duplicates(self, sols):
		'''This function takes in a solution description string (sols) and removes solutions that are effectively duplicates of other solutions.'''
		no_parens_dict = {}
		for sol in sols:
			rem_paren = re.sub(r"\(|\)", "", sol) 
			if no_parens_dict.has_key(rem_paren):
				no_parens_dict[rem_paren].append(sol)
			else:
				no_parens_dict[rem_paren] = [self.order(rem_paren, sol)]
		no_dupl = []
		for val in no_parens_dict.values():
			no_dupl.append(val[0])
		no_dupl = list(set(no_dupl))
		return no_dupl		

	def run_game_manual(self, nums):
		'''Runs the 24 game solver manually (i.e. non-interactive mode, so the user must input the numbers manually into the function instead of being prompted for them).'''
		iter_nums = list(P(nums))

		sols = self.run_game(iter_nums)

		return sols

	def run_game_interactive(self):
		'''Runs the interactive version of the 24 game solver. The user is prompted to enter the 24 game numbers, is given solutions, and is prompted to enter more 24 game numbers. The user can exit this mode at any time by entering a non-numerical value.'''
		print "you have entered interactive mode"
		print "enter a non-numerical value at any time to stop running"

		while(True):	
			nums = self.get_user_inputs()

			if nums is None:
				print "leaving 24 game"
				break

			iter_nums = list(P(nums))
			sols = self.run_game(iter_nums)

			if len(sols) > 0:
				for sol in sols:
					print sol
			else:
				print "Sorry, no solutions could be found."

	def run_game(self, iter_nums):
		'''This function generates the solutions for the 24 game solver. It is called by run_game_manual and run_game_interactive.'''
		SOLS = []

		for ops in self.iter_ops:
			for nums in iter_nums:
				for par in self.parens:
					result, str_rep = par(nums, ops)	
					if result is not None:
						if float(result)==24:
							SOLS.append(str_rep)

		SOLS = self.remove_duplicates(SOLS)

		if self.def_stop != None:
			stop = min(self.def_stop, len(SOLS))
			return SOLS[:stop]

		return SOLS

	def A(self, nums, ops):
		'''
		Calculates a value given an array of four numbers and an array of three operations and parenthesis scheme A.

		Args:
			nums (int arr): numbers to perform calculations on
			ops (func arr): operations to perform

		Returns:
			(n1 op1 n2) op2 (n3 op3 n4)
		'''
		op0, op1, op2 = ops
		n1, n2, n3, n4 = nums
		str_rep = "({} {} {}) {} ({} {} {})".format(n1, op0.n, n2, op1.n, n3, op2.n, n4)
		try:
			val = op1( op0(n1, n2), op2(n3, n4) )
			return (val, str_rep)
		except TypeError:
			return (None, None)

	def B(self, nums, ops):
		'''
		Calculates a value given an array of four numbers and an array of three operations and parenthesis scheme A.

		Args:
			nums (int arr): numbers to perform calculations on
			ops (func arr): operations to perform

		Returns:
			((n1 op1 n2) op2 n3) op3 n4
		'''
		op0, op1, op2 = ops
		n1, n2, n3, n4 = nums
		str_rep = "(({} {} {}) {} {}) {} {}".format(n1, op0.n, n2, op1.n, n3, op2.n, n4)
		try:
			val = op2( op1( op0(n1, n2), n3), n4)
			return (val, str_rep)
		except TypeError:
			return (None, None)

	def C(self, nums, ops):
		'''
		Calculates a value given an array of four numbers and an array of three operations and parenthesis scheme A.

		Args:
			nums (int arr): numbers to perform calculations on
			ops (func arr): operations to perform

		Returns:
			n1 op1 (n2 op2 (n3 op3 n4))
		'''
		op0, op1, op2 = ops
		n1, n2, n3, n4 = nums
		str_rep = "{} {} ({} {} ({} {} {}))".format(n1, op0.n, n2, op1.n, n3, op2.n, n4)
		try:
			val = op0( n1, op1( n2, op2(n3, n4) ) )
			return (val, str_rep)
		except TypeError:
			return (None, None)

	def D(self, nums, ops):
		'''
		Calculates a value given an array of four numbers and an array of three operations and parenthesis scheme A.

		Args:
			nums (int arr): numbers to perform calculations on
			ops (func arr): operations to perform

		Returns:
			(n1 op1 (n2 op2 n3)) op3 n4
		'''
		op0, op1, op2 = ops
		n1, n2, n3, n4 = nums
		str_rep = "({} {} ({} {} {})) {} {}".format(n1, op0.n, n2, op1.n, n3, op2.n, n4)
		try:
			val = op2( op0( n1, op1(n2, n3) ), n4)
			return (val, str_rep)
		except TypeError:
			return (None, None)

	def E(self, nums, ops):
		'''
		Calculates a value given an array of four numbers and an array of three operations and parenthesis scheme A.

		Args:
			nums (int arr): numbers to perform calculations on
			ops (func arr): operations to perform

		Returns:
			n1 op1 ((n2 op2 n3) op3 n4)
		'''
		op0, op1, op2 = ops
		n1, n2, n3, n4 = nums
		str_rep = "{} {} (({} {} {}) {} {})".format(n1, op0.n, n2, op1.n, n3, op2.n, n4)
		try:
			val = op0(n1, op2( op1(n2, n3), n4) )
			return (val, str_rep)
		except TypeError:
			return (None, None)

# get terminal arguments
parser = argparse.ArgumentParser(description='Solve the 24 game.')

parser.add_argument('--nums', default=[0,0,0,0], nargs=4, 
	metavar=('N1', 'N2', 'N3', 'N4'), type=int, help='24 game card numbers')

parser.add_argument('--max_sols', default=10, nargs=1, metavar='S', 
                   help='number of solutions to display (default=10)')

parser.add_argument('--no_max_sols', help='show all solutions', action='store_true')

args = parser.parse_args()

if args.no_max_sols:
	max_sols = None
else:
	max_sols = args.max_sols

game = twenty_four_game(max_sols)

if args.nums == [0,0,0,0]:
	game.run_game_interactive()
else:
	sols = game.run_game_manual(args.nums)
	if len(sols) > 0:
		for sol in sols:
			print sol
	else:
		print "Sorry, no solutions could be found."
