class Logic : 
	"""Implementation des portes logiques"""
	def nand(a,b) :
		"""Retourne A NAND B
		params : 
			a : int ; le premier bit
			b : int ; le deuxième bit
		return : bool ; le NAND
		"""
		return bool(not ( a and b))

	def nor(a,b) : 
		"""Retourne A NOR B
		params : 
			a : int ; le premier bit
			b : int ; le deuxième bit
		return : bool ; le NOR
		"""
		return bool(not (a or b))
	def xor(a,b) : 
		"""Retourne A XOR B
		params : 
			a : int ; le premier bit
			b : int ; le deuxième bit
		return : bool ; le XOR
		"""
		return bool((a and not b) or (not a and b))

class Utils : 
	"""Regroupement de fonctions facilitant la manipulation des nombres dans différentes bases"""
	OCTETS = 1 # Le nombre d'octets sur lequel nous travaillereons dans tout le programme

	BIN_DICT = {"0" : 0,"1" : 1} # Un dictionnaire permettant la conversion de texte en binaire
	BIN_DICT_REVERSED = {0 : "0", 1 : "1"} # Un dictionnaire permettant la conversion de binaire en texte 

	# Un dictionnaire permettant la conversion de texte en hexadecimal
	HEX_DICT = {"0":0, "1":1, "2":2,"3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15}
	# Un dictionnaire permettant la conversion d'hexadecimal en texte
	HEX_DICT_REVERSED = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

	
	def Nis_valid(int_,base) : 
		"""Verifie si le nombre entier naturel int_ est encodable sur Utils.OCTETS dans la base base
		params : 
			int_ : int ; le nombre a verifier
			base : int ; la base de int_
		return : bool ; True si le nombre est valide sinon False
		"""
		return bool(int_ < base ** (Utils.OCTETS *8))

	def format_entry(entry,base) : 
		"""Convertit une entrée texte en liste exploitable par le reste des fonctions
		params : 
			entry : str ; la valeur a normaliser
			base : int ; la base de entry
		return : list ; entry normalise
		"""
		type_ = type(entry)
		if type_ == int :
			return [entry]
		elif type_ == list : 
			return entry
		elif type_ == str : 
			if base == 2 : 
				return [BIN_DICT[x] for x in entry]
			elif base == 16 : 
				return [HEX_DICT[x] for x in entry]
			else : 
				return [x for x in entry]
		else : 
			raise TypeError("Le type de l'entree n'est pas supportee.")

	def _Nbase10_to_anybase(int_,out_base) : 
		"""Convertit un nombre entier naturel en base 10 en n'importe qelle autre base
		params : 
			int_ : int ; le nombre en base 10
			out_base : int ; la base de sortie souhaitee
		return : 
			response : list ; le nombre converti
		"""
		bits = Utils.OCTETS * 8
		response = [0] * int(bits)
		for i in range(len(response)) : 
			response[i] = int_ % out_base
			int_ //= out_base
		response.reverse()
		return response

	def _Nanybase_to_base10(list_,in_base) : 
		"""Convertit un nombre entier naturel en n'importe quelle base en base 10
		params : 
			int_ : int ; le nombre en n'importe quelle base
			in_base : int ; la base de int_
		return : 
			response : list ; le nombre converti
		"""
		power = len(list_)-1
		response = 0
		for i in list_ : 
			response += i * in_base ** power
			power -= 1
		return response

	def Nanybase_to_anybase(list_,in_base,out_base) :
		"""Convertit un nombre entier naturel en n'importe quelle en n'importe qelle autre base
		params : 
			int_ : int ; le nombre en n'importe quelle base
			in_base : int ; la base de int_
			out_base : int ; la base de sortie souhaitee
		return : 
			anybase_ : list ; le nombre converti
		"""
		base10 = Utils._Nanybase_to_base10(list_,in_base)
		anybase_ = Utils._Nbase10_to_anybase(base10,out_base)
		return anybase_

class NaturalBinaryNumber(object) : 
	"""Implementation des nombres binaires entiers naturels sous forme d'objets"""
	def __init__(self,origin_value, origin_base = 10) :
		"""Initialisation de la classe"""

		#on vérifie que le nombre est valide et on le stocke en binaire
		cache = Utils.format_entry(origin_value,origin_base) 
		cache10 = Utils._Nanybase_to_base10(cache,origin_base)
		if not Utils.Nis_valid(cache10,2) : raise ValueError("Valeur entree trop grande.")

		self.data = Utils.Nanybase_to_anybase(list_ = cache,in_base = origin_base,out_base = 2)

	@property
	def value(self) : 
		"""renvoyer la valeur de self.data soous une forme lisible"""
		response = str()
		for elem in self.data : 
			response += Utils.BIN_DICT_REVERSED[elem]
		return response

	def __repr__(self) :
		"""appel lors de print afin d'afficher une valeur comprehensible""" 
		return self.value

	def __add__(self,b) : 
		"""appel lors de l'utilisation de +, additioner deux nombres binaires sans passer par le decimal"""
		assert isinstance(b,NaturalBinaryNumber),"Impossible d'additionner un nombre non-binaire."
		d1 = self.data
		d2 = b.data
		d1.reverse()
		d2.reverse()

		carry = int()
		response = list()

		for i in range((Utils.OCTETS*8)) : 
			#s = a xor b xor carry
			#carry = (a or b) and (a or carry) and (b or carry)
			a = d1[i]
			b = d2[i]
			s = Logic.xor(Logic.xor(a,b),carry)
			carry = (a or b) and (a or carry) and (b or carry)
			response.append(s)
		response.reverse()
		return NaturalBinaryNumber(response,2)

	def __sub__(self,b) : 
		"""appel lors de l'utilisation de -, retrancher deux nombres binaires sans passer par le decimal"""
		assert isinstance(b,NaturalBinaryNumber),"Impossible d'additionner un nombre non-binaire."
		d1 = self.data
		d2 = b.data
		d1.reverse()
		d2.reverse()

		response = list()
		borrow = 0
		for i in range(Utils.OCTETS * 8) : 
		 	#s = a xor (b xor borrow)
		 	#borrow = ((not a) and b) or (b and borrow) or ((not a) and borrow)
		 	a = d1[i]
		 	b = d2[i]
		 	s = Logic.xor(a,Logic.xor(b,borrow))
		 	borrow = ((not a) and b) or (b and borrow) or ((not a) and borrow)
		 	response.append(s)
		response.reverse()
		return NaturalBinaryNumber(response,2)

	def __mul__(self,b) : 
		"""appel lors de l'utilisation de *, multiplier deux nombres binaires sans passer par le decimal"""
		assert isinstance(b,NaturalBinaryNumber),"Impossible d'additionner un nombre non-binaire."
		d1 = self.data
		d2 = b.data
		d1.reverse()
		d2.reverse()

		response = NaturalBinaryNumber(0)
		partial_response = list()

		for i in range(Utils.OCTETS * 8) : 
			part_response = list()
			cache1 = d1[i]
			for cache2 in d2 : 
				part_response.append(int(cache1 and cache2))
			part_response.extend([0] * i)
			part_response.reverse()
			partial_response.append(part_response)

		for elem in partial_response : 
			print(elem," ::::::: ",i)
			response = response.__add__(NaturalBinaryNumber(elem,origin_base = 2))
			print(response)
			print("_" * 50)

		return response







n1 = NaturalBinaryNumber(10)
n2 = NaturalBinaryNumber(5)
n3 = n2 * n1
print(n3)
print(bin(50))


